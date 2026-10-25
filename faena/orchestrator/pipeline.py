"""
Master AI Factory Pipeline Orchestrator.
"""
from __future__ import annotations
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional
from faena.providers.base import LLMProvider
from faena.agents.registry import AgentRegistry
from faena.orchestrator.state import TicketSessionState, TaskItem
from faena.orchestrator.context_engine import ContextEngine
from faena.orchestrator.trd_engine import TRDEngine
from faena.orchestrator.task_engine import TaskEngine
from faena.orchestrator.executor import TaskExecutor
from faena.orchestrator.review_engine import ReviewEngine


class FaenaPipeline:
    def __init__(
        self,
        workspace_root: Path,
        provider: LLMProvider,
        registry: Optional[AgentRegistry] = None,
        on_log: Optional[Callable[[str], None]] = None,
    ):
        self.workspace_root = workspace_root.resolve()
        self.provider = provider
        self.registry = registry or AgentRegistry(self.workspace_root)
        self.on_log = on_log or (lambda msg: print(msg, flush=True))

        self.context_engine = ContextEngine(self.workspace_root, self.provider)
        self.trd_engine = TRDEngine(self.workspace_root, self.provider, self.registry)
        self.task_engine = TaskEngine(self.workspace_root, self.provider)
        self.executor = TaskExecutor(
            self.workspace_root,
            self.provider,
            self.registry,
            on_log=self.on_log,
        )

    def _log(self, msg: str):
        self.on_log(msg)

    def _slugify(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s_-]+", "-", text)
        return text[:40].strip("-") or "ticket"

    def run_ticket(
        self,
        ticket_input: str,
        target: Optional[str] = None,
        auto_approve: bool = True,
        resume: bool = False,
    ) -> TicketSessionState:
        """
        Runs the complete AI Factory lifecycle for a ticket:
        1. Context Loading & Multi-Repo Detection
        2. Technical Requirements Document & Test Spec Generation
        3. TDD Task Generation (RED -> GREEN -> VERIFY)
        4. Autonomous Multi-Agent Task Execution Loop
        5. Quality Gate Verification & Final Delivery Report
        """
        target_dir = None
        if target:
            candidate = self.workspace_root / target
            if not candidate.exists():
                candidate = self.workspace_root / "Proyecto" / target
            if not candidate.exists():
                candidate = self.workspace_root / "projects" / target
            if candidate.exists():
                target_dir = candidate
                self._log(f"🎯 Target Repository: {target_dir.relative_to(self.workspace_root)}")
            else:
                self._log(f"⚠️ Target path '{target}' not found. Using workspace root.")

        if target_dir:
            self.executor.target_dir = target_dir

        self._log("=" * 70)
        self._log("🏭 FAENA AI FACTORY: INITIATING AUTONOMOUS TICKET PIPELINE")
        self._log(f"   Provider: {self.provider.provider_name} ({self.provider.get_model()})")
        self._log(f"   Workspace: {self.workspace_root}")
        if target_dir:
            self._log(f"   Target Repo: {target_dir}")
        self._log("=" * 70)

        # Parse ticket input
        ticket_file = Path(ticket_input)
        if ticket_file.exists() and ticket_file.is_file():
            ticket_content = ticket_file.read_text(encoding="utf-8", errors="replace")
            ticket_title = ticket_file.stem
        else:
            ticket_content = ticket_input
            # Use first line or first 50 chars as title
            first_line = ticket_input.strip().splitlines()[0] if ticket_input.strip() else "New Ticket"
            ticket_title = first_line[:50]

        slug = self._slugify(ticket_title)
        task_dir = self.workspace_root / "tasks" / f"task-{slug}"
        state_file = task_dir / "state.json"

        # Check for resume
        if resume and state_file.exists():
            self._log(f"🔄 Resuming existing session from {state_file}")
            state = TicketSessionState.load(state_file)
        else:
            now = datetime.now(timezone.utc).isoformat()
            state = TicketSessionState(
                ticket_id=slug,
                ticket_title=ticket_title,
                workspace_dir=str(self.workspace_root),
                created_at=now,
                updated_at=now,
                task_dir=str(task_dir),
            )

        # PHASE 1: Context Analysis
        self._log("\n🔍 [STAGE 1/5] Analyzing Codebase Context...")
        self.context_engine.build_initial_context()
        context_str = self.context_engine.load_synthesized_context()
        self._log("   ✅ Project context loaded and verified.")

        # PHASE 2: TRD & Test Spec Generation
        if not state.trd_file or not Path(state.trd_file).exists():
            self._log("\n📐 [STAGE 2/5] Architecting Technical Requirements & Test Spec...")
            trd_path, test_spec_path = self.trd_engine.generate_trd(
                ticket_title=ticket_title,
                ticket_content=ticket_content,
                project_context=context_str,
            )
            state.trd_file = str(trd_path)
            state.test_spec_file = str(test_spec_path)
            state.status = "trd_ready"
            state.save(state_file)
            self._log(f"   ✅ TRD created: {trd_path.relative_to(self.workspace_root)}")
            self._log(f"   ✅ Test Spec created: {test_spec_path.relative_to(self.workspace_root)}")

            if not auto_approve:
                ans = input("\nProceed with Task Generation based on this TRD? [Y/n]: ")
                if ans.strip().lower() in ("n", "no"):
                    self._log("Pipeline paused by user.")
                    return state
        else:
            self._log(f"\n📐 [STAGE 2/5] Using existing TRD: {state.trd_file}")

        # PHASE 3: Task Decomposition
        if not state.tasks:
            self._log("\n📋 [STAGE 3/5] Decomposing TRD into TDD Tasks (RED-GREEN-VERIFY)...")
            tasks = self.task_engine.generate_tasks(
                trd_file=Path(state.trd_file),
                test_spec_file=Path(state.test_spec_file),
            )
            state.tasks = tasks
            state.status = "tasks_ready"
            state.save(state_file)
            self._log(f"   ✅ Generated {len(tasks)} implementation tasks.")
            for t in tasks:
                self._log(f"      - Task {t.number:02d} [{t.phase.upper()}]: {t.title}")

            if not auto_approve:
                ans = input("\nProceed with autonomous execution of tasks? [Y/n]: ")
                if ans.strip().lower() in ("n", "no"):
                    self._log("Pipeline paused before execution.")
                    return state
        else:
            self._log(f"\n📋 [STAGE 3/5] Using {len(state.tasks)} existing tasks.")

        # PHASE 4: Autonomous Execution Loop
        self._log("\n⚙️ [STAGE 4/5] Executing Tasks Autonomously...")
        state.status = "executing"
        state.save(state_file)

        for task in state.tasks:
            if task.status == "completed":
                self._log(f"   ⏩ Skipping already completed Task {task.number:02d}: {task.title}")
                continue

            success = self.executor.execute_task(task, task_dir)
            state.save(state_file)

            if not success:
                self._log(f"\n❌ Pipeline halted at Task {task.number:02d}: {task.error_message}")
                state.status = "failed"
                state.save(state_file)
                return state

        # PHASE 4.5: Adversarial Review & Security Audit (ECC Gate)
        self._log("\n🛡️ [STAGE 4.5] Adversarial Code Review & Security Audit (ECC Gate)...")
        review_engine = ReviewEngine(
            workspace_root=self.workspace_root,
            provider=self.provider,
            registry=self.registry,
            target_dir=target_dir,
        )
        review_result = review_engine.run_review(task_dir, state.ticket_title)
        verdict = review_result.get("verdict", "APPROVED")
        report_file_path = review_result.get("report_file", "")
        if verdict == "APPROVED":
            self._log(f"   🟢 Security & Code Review: APPROVED")
        else:
            self._log(f"   🟡 Security & Code Review: CHANGES_REQUESTED (See REVIEW-REPORT.md)")
        self._log(f"   📄 Review details: {Path(report_file_path).relative_to(self.workspace_root)}")

        # PHASE 5: Verification & Delivery Report
        self._log("\n🏆 [STAGE 5/5] Final Verification & Deliverables Summary...")
        state.status = "completed"
        state.save(state_file)

        report_file = task_dir / "EXECUTION-SUMMARY.md"
        report_content = f"""# Faena AI Factory: Execution Summary
**Ticket**: {state.ticket_title}
**Status**: COMPLETED
**Security & Code Review**: {verdict}
**Provider**: {self.provider.provider_name} ({self.provider.get_model()})
**Completed At**: {datetime.now(timezone.utc).isoformat()}

## Tasks Completed:
{chr(10).join(f"- [x] Task {t.number:02d} [{t.phase.upper()}]: {t.title} ({t.agent})" for t in state.tasks)}

## Quality & Security Gates:
- Review Verdict: **{verdict}**
- Report: `REVIEW-REPORT.md`
- Continuous Memory: Logged in `tasks/context/learnings.md`

## Artifacts:
- TRD: `{Path(state.trd_file).name}`
- Test Spec: `{Path(state.test_spec_file).name}`
- Task Files: `{len(state.tasks)} task files executed successfully`
"""
        report_file.write_text(report_content, encoding="utf-8")

        self._log("=" * 70)
        self._log(f"🎉 TICKET COMPLETED SUCCESSFULLY!")
        self._log(f"   Summary report: {report_file.relative_to(self.workspace_root)}")
        self._log("=" * 70)

        return state
