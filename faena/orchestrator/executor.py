"""
Autonomous Task Execution Engine with Tool-Use and TDD Verification Loops.
"""
from __future__ import annotations
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional
from faena.providers.base import LLMProvider, Message, Role, ToolResult
from faena.tools.registry import get_default_tools, execute_tool
from faena.agents.registry import AgentRegistry, AgentPersona
from faena.orchestrator.state import TaskItem


TDD_RULES_HEADER = """
# MANDATORY TDD PROTOCOL
You are operating in an autonomous AI Factory execution loop.
Follow these rules strictly:
1. Always inspect existing project files and structure before writing new code.
2. If this is a RED phase task:
   - Write the required unit/integration tests using `write_file` or `edit_file`.
   - Execute the test command using `run_command`.
   - VERIFY that the test fails (RED). A failing test validates that the test is actually checking for missing behavior!
   - Once verified failing, declare the RED phase complete.
3. If this is a GREEN phase task:
   - Implement the code to fulfill the test requirements.
   - Run the test suite via `run_command`.
   - If tests fail, inspect the error output, fix the code, and re-run until all tests PASS.
   - Run the verification quality gate command (e.g. linter, typecheck, or build).
   - Once everything passes, summarize your changes and declare task complete.
"""


class TaskExecutor:
    def __init__(
        self,
        workspace_root: Path,
        provider: LLMProvider,
        registry: AgentRegistry,
        max_turns: int = 15,
        target_dir: Optional[Path] = None,
        on_log: Optional[Callable[[str], None]] = None,
    ):
        self.workspace_root = workspace_root.resolve()
        self.target_dir = target_dir.resolve() if target_dir else self.workspace_root
        self.provider = provider
        self.registry = registry
        self.max_turns = max_turns
        self.on_log = on_log or (lambda msg: print(msg, flush=True))

    def _log(self, message: str):
        self.on_log(message)

    def execute_task(self, task: TaskItem, task_dir: Path) -> bool:
        """
        Executes a single atomic task using autonomous tool calling.
        Returns True if successful, False otherwise.
        """
        task_file = Path(task.file_path)
        if not task_file.exists():
            task.status = "failed"
            task.error_message = f"Task file not found: {task.file_path}"
            return False

        task_content = task_file.read_text(encoding="utf-8", errors="replace")

        # Select agent persona
        agent = self.registry.match_agent_for_phase(
            phase=task.phase,
            tech_hint=task.agent,
            task_desc=task.title + " " + task_content[:200],
        )

        self._log(f"\n🚀 [FAENA WORKER] Starting Task {task.number:02d} [{task.phase.upper()}]: {task.title}")
        self._log(f"   Assigned Agent: {agent.name} ({agent.category})")

        task.status = "running"
        task.started_at = datetime.now(timezone.utc).isoformat()
        task.agent = agent.name

        tools = get_default_tools()
        system_prompt = f"{TDD_RULES_HEADER}\n\n## AGENT PERSONA:\n{agent.system_prompt}"

        initial_user_prompt = f"""# EXECUTE TASK FILE: {task_file.name}
Phase: {task.phase.upper()}
Task Title: {task.title}
Target Working Directory: {self.target_dir}

## Task Specifications:
{task_content}

---
You have access to filesystem and terminal tools (`read_file`, `write_file`, `edit_file`, `run_command`, `list_dir`, `search_code`, `find_files`).
Commands executed with `run_command` run by default in the target working directory: `{self.target_dir}`.
Execute the task end-to-end following the TDD rules. Start by reviewing existing code and then performing the necessary operations.
"""

        conversation: List[Message] = [
            Message(role=Role.USER, content=initial_user_prompt)
        ]

        turn = 0
        success = False

        while turn < self.max_turns:
            turn += 1
            self._log(f"   ⚡ Turn {turn}/{self.max_turns}...")

            try:
                response = self.provider.generate(
                    messages=conversation,
                    system_prompt=system_prompt,
                    tools=tools,
                    temperature=0.2,
                )
            except Exception as e:
                self._log(f"   ❌ LLM Generation error: {e}")
                task.error_message = str(e)
                task.status = "failed"
                return False

            if response.content:
                # Log snippet
                first_line = response.content.strip().splitlines()[0] if response.content.strip() else ""
                if first_line:
                    self._log(f"   🤖 Agent: {first_line[:90]}")

            # Append assistant message
            conversation.append(
                Message(
                    role=Role.ASSISTANT,
                    content=response.content,
                    tool_calls=response.tool_calls,
                )
            )

            # Check if agent called tools
            if response.has_tool_calls:
                tool_results: List[ToolResult] = []
                for tc in response.tool_calls:
                    args = dict(tc.arguments)
                    if tc.name == "run_command" and not args.get("cwd"):
                        args["cwd"] = str(self.target_dir)
                    self._log(f"   🔧 Tool Call: {tc.name}({args})")
                    output = execute_tool(tc.name, args)
                    # Log preview of output
                    preview = output.strip().splitlines()[0] if output.strip() else "done"
                    self._log(f"      ↪ Result: {preview[:100]}")

                    tool_results.append(
                        ToolResult(
                            call_id=tc.id,
                            name=tc.name,
                            content=output,
                            is_error=output.startswith("Error:"),
                        )
                    )

                # Append tool results as user / tool turn
                conversation.append(
                    Message(
                        role=Role.TOOL,
                        tool_results=tool_results,
                    )
                )
            else:
                # No more tools called; agent believes task is done
                self._log("   ✅ Agent finished turn sequence.")
                success = True
                break

        if success or turn <= self.max_turns:
            task.status = "completed"
            task.completed_at = datetime.now(timezone.utc).isoformat()
            self._mark_task_completed_in_readme(task_dir, task.number)
            self._log(f"🎉 Task {task.number:02d} completed successfully!")
            return True
        else:
            task.status = "failed"
            task.error_message = f"Exceeded maximum turns ({self.max_turns})"
            self._log(f"❌ Task {task.number:02d} failed: Max turns exceeded.")
            return False

    def _mark_task_completed_in_readme(self, task_dir: Path, task_number: int):
        readme_file = task_dir / "README.md"
        if not readme_file.exists():
            return

        try:
            content = readme_file.read_text(encoding="utf-8")
            pattern = rf"- \[ \] \*\*Task {task_number:02d}"
            replacement = f"- [x] **Task {task_number:02d}"
            new_content = re.sub(pattern, replacement, content)
            readme_file.write_text(new_content, encoding="utf-8")
        except Exception:
            pass
