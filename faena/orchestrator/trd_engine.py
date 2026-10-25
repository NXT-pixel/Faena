"""
TRD Engine: Generates Technical Requirements Document & Test Spec from a Ticket.
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, Tuple
from faena.providers.base import LLMProvider, Message, Role
from faena.agents.registry import AgentRegistry


TRD_SYSTEM_PROMPT = """You are a Principal Software Architect and Technical Requirements Specialist.
Your mission is to analyze the user's ticket and produce a clear, authoritative Technical Requirements Document (TRD) and Test Specification.

Guidelines:
1. Adhere strictly to Test-Driven Development (TDD).
2. Clearly identify all modules and files to create/modify.
3. Define exact function/class signatures and responsibilities.
4. Provide Given-When-Then test specifications with concrete assertions and edge cases.
5. Provide a sequential task breakdown grouped into atomic phases:
   - Setup tasks (if new project setup or dependencies needed)
   - RED tasks (writing failing unit/integration tests)
   - GREEN tasks (implementing code to pass tests + VERIFY quality gate)

You MUST structure your response into TWO clearly separated markdown sections:
---DOCUMENT 1: TRD---
[Full TRD Markdown Content including Mermaid Architecture Diagram and Task Breakdown Section]
---DOCUMENT 2: TEST SPEC---
[Full Test Specification Markdown Content with Given-When-Then scenarios]
"""


class TRDEngine:
    def __init__(self, workspace_root: Path, provider: LLMProvider, registry: AgentRegistry):
        self.workspace_root = workspace_root.resolve()
        self.provider = provider
        self.registry = registry

    def _slugify(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s_-]+", "-", text)
        return text[:40].strip("-") or "feature"

    def generate_trd(
        self,
        ticket_title: str,
        ticket_content: str,
        project_context: str,
    ) -> Tuple[Path, Path]:
        slug = self._slugify(ticket_title)
        task_dir = self.workspace_root / "tasks" / f"task-{slug}"
        task_dir.mkdir(parents=True, exist_ok=True)

        user_prompt = f"""# TICKET TO ARCHITECT:
Title: {ticket_title}

## Description & Requirements:
{ticket_content}

---
## PROJECT CONTEXT:
{project_context}

---
Please produce the TRD and Test Specification documents for this ticket following the specified format.
"""

        messages = [
            Message(role=Role.USER, content=user_prompt)
        ]

        # Use architect persona if available
        architect = self.registry.match_agent_for_phase("trd", task_desc=ticket_content)
        sys_prompt = f"{TRD_SYSTEM_PROMPT}\n\nPersona Expertise:\n{architect.system_prompt}"

        response = self.provider.generate(
            messages=messages,
            system_prompt=sys_prompt,
            temperature=0.2,
            max_tokens=6000,
        )

        raw_output = response.content

        # Split output into TRD and Test Spec
        trd_content = raw_output
        test_spec_content = "# Test Specification\n\nSee TRD for details."

        if "---DOCUMENT 1: TRD---" in raw_output and "---DOCUMENT 2: TEST SPEC---" in raw_output:
            parts = raw_output.split("---DOCUMENT 2: TEST SPEC---")
            trd_part = parts[0].replace("---DOCUMENT 1: TRD---", "").strip()
            test_spec_part = parts[1].strip()
            trd_content = trd_part
            test_spec_content = test_spec_part
        elif "# Test Specification" in raw_output:
            parts = raw_output.split("# Test Specification", 1)
            trd_content = parts[0].strip()
            test_spec_content = "# Test Specification\n" + parts[1].strip()

        trd_file = task_dir / f"trd-{slug}.md"
        test_spec_file = task_dir / f"test-spec-{slug}.md"

        trd_file.write_text(trd_content, encoding="utf-8")
        test_spec_file.write_text(test_spec_content, encoding="utf-8")

        return trd_file, test_spec_file
