"""
Task Engine: Generates atomic RED-GREEN-VERIFY task files from an approved TRD.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import List, Dict, Any
from faena.providers.base import LLMProvider, Message, Role
from faena.orchestrator.state import TaskItem


TASK_GENERATOR_PROMPT = """You are a Task Decomposition Specialist.
Your job is to read an approved Technical Requirements Document (TRD) and Test Specification, and split them into atomic, sequential TDD task files following strict phase separation:

Phases:
1. SETUP (if needed): Project setup, dependencies, scaffolding.
2. RED: Write tests only. Tests MUST fail. Specifying expected assertions, mocks, input/output.
3. GREEN + VERIFY: Implementation of code to make tests pass, followed by quality gate verification commands.

You MUST output a valid JSON array of objects representing the task files to generate:
```json
[
  {
    "number": 1,
    "phase": "setup",
    "filename": "task01-setup-dependencies.md",
    "title": "Setup project dependencies and directory structure",
    "agent_hint": "project-bootstrapper",
    "content": "... full markdown content of the task file ..."
  },
  {
    "number": 2,
    "phase": "red",
    "filename": "task02-red-user-service-tests.md",
    "title": "Write unit tests for UserService",
    "agent_hint": "jest-tester",
    "content": "... full markdown content including Given-When-Then test specs and test run command ..."
  },
  {
    "number": 3,
    "phase": "green",
    "filename": "task03-green-user-service-impl.md",
    "title": "Implement UserService logic and verify quality gates",
    "agent_hint": "typescript-pro",
    "content": "... full markdown content including implementation goals, references to task02 tests, and quality gate commands ..."
  }
]
```

CRITICAL: Return ONLY the JSON code block without any conversational filler.
"""


class TaskEngine:
    def __init__(self, workspace_root: Path, provider: LLMProvider):
        self.workspace_root = workspace_root.resolve()
        self.provider = provider

    def generate_tasks(
        self,
        trd_file: Path,
        test_spec_file: Path,
    ) -> List[TaskItem]:
        task_dir = trd_file.parent
        trd_content = trd_file.read_text(encoding="utf-8", errors="replace")
        test_spec_content = test_spec_file.read_text(encoding="utf-8", errors="replace")

        user_prompt = f"""# APPROVED TECHNICAL REQUIREMENTS (TRD):
{trd_content}

---
# TEST SPECIFICATION:
{test_spec_content}

Please decompose this TRD and Test Spec into sequential RED-GREEN-VERIFY task files formatted as a JSON array.
"""

        response = self.provider.generate(
            messages=[Message(role=Role.USER, content=user_prompt)],
            system_prompt=TASK_GENERATOR_PROMPT,
            temperature=0.1,
            max_tokens=6000,
        )

        text = response.content.strip()

        # Extract JSON
        json_str = ""
        if "```json" in text:
            parts = text.split("```json")
            json_str = parts[1].split("```")[0].strip()
        elif "```" in text:
            parts = text.split("```")
            json_str = parts[1].split("```")[0].strip()
        else:
            json_str = text

        try:
            tasks_data = json.loads(json_str)
        except Exception:
            # Fallback regex search for array
            match = re.search(r"\[.*\]", text, re.DOTALL)
            if match:
                tasks_data = json.loads(match.group(0))
            else:
                raise ValueError(f"Could not parse tasks JSON from LLM response: {text[:300]}")

        created_items: List[TaskItem] = []
        readme_lines = [
            f"# Implementation Tasks: {task_dir.name}",
            "",
            "## Task Progress",
            "",
        ]

        for idx, t in enumerate(tasks_data, 1):
            num = t.get("number", idx)
            phase = t.get("phase", "green").lower()
            fname = t.get("filename") or f"task{num:02d}-{phase}.md"
            title = t.get("title") or f"Task {num}"
            content = t.get("content") or f"# {title}\n\nPhase: {phase}"
            agent_hint = t.get("agent_hint") or ""

            target_file = task_dir / fname
            target_file.write_text(content, encoding="utf-8")

            item = TaskItem(
                id=f"task_{num:02d}",
                number=num,
                phase=phase,
                title=title,
                file_path=str(target_file),
                status="pending",
                agent=agent_hint,
            )
            created_items.append(item)
            readme_lines.append(f"- [ ] **Task {num:02d} [{phase.upper()}]**: [{title}]({fname})")

        readme_lines.append("\n## Execution Protocol")
        readme_lines.append("1. **RED Phase**: Run test -> verify it fails as expected.")
        readme_lines.append("2. **GREEN Phase**: Write code -> run test -> verify it passes.")
        readme_lines.append("3. **VERIFY Phase**: Run full quality gate suite.")

        readme_file = task_dir / "README.md"
        readme_file.write_text("\n".join(readme_lines), encoding="utf-8")

        return created_items
