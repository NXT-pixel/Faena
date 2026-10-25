"""
Review & Resilience Engine: Automated Code Review, Security Auditing, and Continuous Learning.
Inspired by ECC (Enterprise Coding Companion) orchestration.
"""
from __future__ import annotations
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from faena.providers.base import LLMProvider, Message, Role
from faena.agents.registry import AgentRegistry


REVIEW_SYSTEM_PROMPT = """You are a Principal Security Engineer and Senior Code Reviewer.
Your role is to perform an adversarial, high-rigor review of the newly implemented code changes.

Review Dimensions:
1. SECURITY (OWASP Top 10):
   - Hardcoded secrets, API keys, passwords, or tokens (CRITICAL).
   - SQL Injection, Command Injection, or unescaped query parameters (CRITICAL).
   - SSRF, Path Traversal, Unvalidated Redirects (HIGH).
   - Authentication bypass, missing role/permission checks (CRITICAL).
   - Insecure deserialization or untrusted data handling (HIGH).

2. CODE QUALITY & RESILIENCE:
   - Null-pointer / undefined access hazards.
   - Resource leaks (unclosed streams, unhandled async cancellations).
   - Silent exception swallowing (`catch {}` or empty `except:`).
   - Race conditions or non-thread-safe state.

3. CONFIDENCE-BASED FILTERING:
   - ONLY report issues you are >80% confident represent genuine defects or security vulnerabilities.
   - Cite the exact file name and line number for each finding.
   - Do NOT complain about purely aesthetic style preferences.

Output Format:
You MUST structure your response into:
# Code & Security Review Report
## Verdict: [APPROVED | CHANGES_REQUESTED]
## Security Findings (CRITICAL / HIGH / MEDIUM / LOW)
- [Severity] `path/to/file:line` - Finding description and failure scenario.
## Code Quality & Resilience Findings
- [Severity] `path/to/file:line` - Description.
## Key Learnings & Project Conventions (for long-term memory)
- Bullet points of project conventions or edge-case behaviors discovered.
"""


class ReviewEngine:
    def __init__(
        self,
        workspace_root: Path,
        provider: LLMProvider,
        registry: AgentRegistry,
        target_dir: Optional[Path] = None,
    ):
        self.workspace_root = workspace_root.resolve()
        self.target_dir = target_dir.resolve() if target_dir else self.workspace_root
        self.provider = provider
        self.registry = registry

    def get_git_diff(self) -> str:
        """Captures local unstaged and staged git diffs."""
        try:
            res = subprocess.run(
                ["git", "diff", "HEAD"],
                cwd=str(self.target_dir),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()

            # Fallback to unstaged diff
            res2 = subprocess.run(
                ["git", "diff"],
                cwd=str(self.target_dir),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            return res2.stdout.strip()
        except Exception:
            return ""

    def run_review(self, task_dir: Path, ticket_title: str) -> Dict[str, Any]:
        diff_text = self.get_git_diff()
        if not diff_text:
            diff_text = "(No git diff detected. Reviewing implemented task files and recent modifications.)"

        prompt = f"""# CODE REVIEW & SECURITY AUDIT FOR TICKET:
Ticket: {ticket_title}
Target Directory: {self.target_dir.relative_to(self.workspace_root) if self.target_dir != self.workspace_root else '.'}

## Unified Diff of Changes:
```diff
{diff_text[:12000]}
```

Perform the security and quality review now.
"""

        sec_agent = self.registry.get_agent("security-reviewer")
        sys_prompt = REVIEW_SYSTEM_PROMPT
        if sec_agent:
            sys_prompt += f"\n\nSecurity Persona Baseline:\n{sec_agent.system_prompt[:1500]}"

        response = self.provider.generate(
            messages=[Message(role=Role.USER, content=prompt)],
            system_prompt=sys_prompt,
            temperature=0.1,
            max_tokens=4000,
        )

        content = response.content

        # Determine verdict
        verdict = "APPROVED"
        if "Verdict: CHANGES_REQUESTED" in content or "CHANGES_REQUESTED" in content[:300]:
            verdict = "CHANGES_REQUESTED"

        # Save Review Report
        report_file = task_dir / "REVIEW-REPORT.md"
        report_file.write_text(content, encoding="utf-8")

        # Save continuous learnings to tasks/context/learnings.md
        self._record_learnings(content, ticket_title)

        return {
            "verdict": verdict,
            "report_file": str(report_file),
            "content": content,
        }

    def _record_learnings(self, review_content: str, ticket_title: str):
        """Extracts learnings and saves them to tasks/context/learnings.md."""
        if "Key Learnings & Project Conventions" not in review_content:
            return

        try:
            learnings_section = review_content.split("Key Learnings & Project Conventions")[1].strip()
            # Clean up trailing sections if any
            if "#" in learnings_section:
                learnings_section = learnings_section.split("#")[0].strip()

            if not learnings_section or learnings_section == "- None" or len(learnings_section) < 10:
                return

            learnings_file = self.workspace_root / "tasks" / "context" / "learnings.md"
            learnings_file.parent.mkdir(parents=True, exist_ok=True)

            now = datetime.now(timezone.utc).isoformat()
            entry = f"\n\n### 💡 Ticket Learning: {ticket_title} ({now})\n{learnings_section}"

            if not learnings_file.exists():
                learnings_file.write_text("# Project Memory & Continuous Learnings\n" + entry, encoding="utf-8")
            else:
                with open(learnings_file, "a", encoding="utf-8") as f:
                    f.write(entry)
        except Exception:
            pass
