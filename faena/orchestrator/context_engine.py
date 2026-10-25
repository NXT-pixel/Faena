"""
Context Engine: Analyzes codebase, sub-repositories in Proyecto/, and manages tasks/context/ documents.
"""
from __future__ import annotations
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from faena.providers.base import LLMProvider


class ContextEngine:
    def __init__(self, workspace_root: Path, provider: Optional[LLMProvider] = None, project_dir_name: str = "Proyecto"):
        self.workspace_root = workspace_root.resolve()
        self.context_dir = self.workspace_root / "tasks" / "context"
        self.provider = provider
        self.project_dir = self.workspace_root / project_dir_name
        if not self.project_dir.exists():
            alt = self.workspace_root / "projects"
            if alt.exists():
                self.project_dir = alt

    def ensure_context_dir(self):
        self.context_dir.mkdir(parents=True, exist_ok=True)

    def _inspect_directory(self, dir_path: Path) -> Dict[str, Any]:
        """Detects language, framework, build tools, and git info for a given directory."""
        info = {
            "path": str(dir_path.relative_to(self.workspace_root)),
            "technologies": [],
            "package_managers": [],
            "git_branch": "unknown",
            "git_remote": "",
            "git_commit": "unknown",
            "detected_files": [],
        }

        # Check git info
        try:
            res = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=str(dir_path),
                capture_output=True,
                text=True,
            )
            if res.returncode == 0:
                info["git_branch"] = res.stdout.strip()

            res2 = subprocess.run(
                ["git", "log", "-1", "--oneline"],
                cwd=str(dir_path),
                capture_output=True,
                text=True,
            )
            if res2.returncode == 0:
                info["git_commit"] = res2.stdout.strip()

            res3 = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=str(dir_path),
                capture_output=True,
                text=True,
            )
            if res3.returncode == 0:
                info["git_remote"] = res3.stdout.strip()
        except Exception:
            pass

        indicators = [
            ("package.json", "Node.js / TypeScript / JavaScript", "npm"),
            ("pnpm-lock.yaml", "pnpm", "pnpm"),
            ("yarn.lock", "yarn", "yarn"),
            ("pyproject.toml", "Python", "pip/poetry"),
            ("requirements.txt", "Python", "pip"),
            ("Cargo.toml", "Rust", "cargo"),
            ("go.mod", "Go", "go modules"),
            ("pom.xml", "Java", "maven"),
            ("build.gradle", "Java/Kotlin", "gradle"),
        ]

        for fname, tech, pm in indicators:
            if (dir_path / fname).exists():
                info["technologies"].append(tech)
                info["package_managers"].append(pm)
                info["detected_files"].append(fname)

        cs_files = list(dir_path.glob("*.sln")) + list(dir_path.glob("**/*.csproj"))
        if cs_files:
            info["technologies"].append(".NET / C#")
            info["package_managers"].append("dotnet")
            info["detected_files"].extend([f.name for f in cs_files[:3]])

        return info

    def detect_all_repositories(self) -> Dict[str, Any]:
        """Discovers and inspects all repositories inside the Proyecto/ directory and workspace root."""
        sub_repos = []
        if self.project_dir.exists() and self.project_dir.is_dir():
            for child in sorted(self.project_dir.iterdir()):
                if child.is_dir() and not child.name.startswith("."):
                    sub_info = self._inspect_directory(child)
                    sub_repos.append(sub_info)

        root_info = self._inspect_directory(self.workspace_root)
        return {
            "root": root_info,
            "project_dir": str(self.project_dir.name),
            "sub_repositories": sub_repos,
        }

    def build_initial_context(self) -> Dict[str, Path]:
        """Creates or refreshes the foundational context files."""
        self.ensure_context_dir()
        now = datetime.now(timezone.utc).isoformat()
        repo_data = self.detect_all_repositories()

        created_files = {}

        # 1. Tech Context
        tech_file = self.context_dir / "tech-context.md"
        sub_repos = repo_data["sub_repositories"]

        lines = [
            "# Technical Context",
            f"**Created**: {now}",
            f"**Last Updated**: {now}",
            "",
            f"## Workspace Project Folder: `{repo_data['project_dir']}/`",
        ]

        if sub_repos:
            lines.append(f"Discovered **{len(sub_repos)}** client/company repository(ies) in `{repo_data['project_dir']}/`:\n")
            for sr in sub_repos:
                techs = ", ".join(set(sr["technologies"])) or "Generic / Undetermined"
                pms = ", ".join(set(sr["package_managers"])) or "None"
                remote = f" ({sr['git_remote']})" if sr["git_remote"] else ""
                lines.append(f"### 📦 Repo: `{sr['path']}`{remote}")
                lines.append(f"- **Branch**: `{sr['git_branch']}` | **Commit**: `{sr['git_commit']}`")
                lines.append(f"- **Tech Stack**: {techs}")
                lines.append(f"- **Package Manager**: {pms}")
                lines.append(f"- **Config Files**: {', '.join(sr['detected_files']) or 'None'}\n")
        else:
            lines.append(f"No sub-repositories currently cloned in `{repo_data['project_dir']}/`.")
            lines.append("Clone the client or company repos into this folder to enable automated multi-repo detection.\n")

        tech_file.write_text("\n".join(lines), encoding="utf-8")
        created_files["tech-context"] = tech_file

        # 2. Project Structure
        struct_file = self.context_dir / "project-structure.md"
        struct_lines = [
            "# Project Structure",
            f"**Created**: {now}",
            "",
            "## Architecture Layout",
            f"- `{repo_data['project_dir']}/`: Cloned repositories and target source code for this client/company",
            "- `rules/project/`: Company-specific standards and rules (highest priority)",
            "- `skills/project/`: Company-specific domain knowledge, internal SDKs, and patterns",
            "- `agents/project/`: Company-specific personas and custom roles",
            "- `tasks/tickets/`: Assigned client tickets, specs, and user stories",
            "- `tasks/context/`: Architecture, technology stack, and progress docs",
        ]
        if sub_repos:
            struct_lines.append(f"\n## Active Repositories in `{repo_data['project_dir']}/`:")
            for sr in sub_repos:
                struct_lines.append(f"- `{sr['path']}` (Branch: `{sr['git_branch']}`)")

        struct_file.write_text("\n".join(struct_lines), encoding="utf-8")
        created_files["project-structure"] = struct_file

        # 3. Progress Tracker
        prog_file = self.context_dir / "progress.md"
        if not prog_file.exists():
            prog_content = f"""# Project Progress
**Created**: {now}
**Status**: Ready to receive and execute tickets for this project.
"""
            prog_file.write_text(prog_content, encoding="utf-8")
            created_files["progress"] = prog_file

        # 4. System Patterns
        pattern_file = self.context_dir / "system-patterns.md"
        if not pattern_file.exists():
            pattern_content = f"""# System Patterns & Architecture
**Created**: {now}

## Core Design Principles
1. **Isolated Client Repos**: Cloned under `{repo_data['project_dir']}/`, keeping client code isolated from Faena harness.
2. **Custom Rules & Skills**: Rules in `rules/project/` and skills in `skills/project/` customize Faena specifically for this company.
3. **Strict TDD Cycle**: RED (test fails) -> GREEN (code passes) -> VERIFY (quality gates).
4. **Universal Multi-Provider**: Switch seamlessly between Claude, ChatGPT, Gemini, Ollama, etc.
"""
            pattern_file.write_text(pattern_content, encoding="utf-8")
            created_files["system-patterns"] = pattern_file

        return created_files

    def load_synthesized_context(self) -> str:
        """Loads context files + company rules and skills into a clean string for agent prompts."""
        if not self.context_dir.exists():
            self.build_initial_context()

        context_blocks = []

        # Load tasks/context/*.md
        for p in sorted(self.context_dir.glob("*.md")):
            try:
                content = p.read_text(encoding="utf-8", errors="replace")
                context_blocks.append(f"### Context File: {p.name}\n```markdown\n{content}\n```")
            except Exception:
                continue

        # Load project-specific rules if any
        project_rules_dir = self.workspace_root / "rules" / "project"
        if project_rules_dir.exists():
            rule_files = list(project_rules_dir.glob("*.mdc")) + list(project_rules_dir.glob("*.md"))
            for rf in rule_files:
                if rf.name == "README.md":
                    continue
                try:
                    c = rf.read_text(encoding="utf-8", errors="replace")
                    context_blocks.append(f"### MANDATORY COMPANY RULE: {rf.name}\n```markdown\n{c}\n```")
                except Exception:
                    continue

        # Load project-specific skills if any
        project_skills_dir = self.workspace_root / "skills" / "project"
        if project_skills_dir.exists():
            for sf in project_skills_dir.rglob("SKILL.md"):
                try:
                    c = sf.read_text(encoding="utf-8", errors="replace")
                    context_blocks.append(f"### COMPANY SKILL: {sf.parent.name}\n```markdown\n{c}\n```")
                except Exception:
                    continue

        if not context_blocks:
            return "No prior project context files found. Using fresh repository context."

        return "\n\n".join(context_blocks)
