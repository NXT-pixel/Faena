"""
Agent Persona Registry and Matcher for Faena.
"""
from __future__ import annotations
import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class AgentPersona:
    name: str
    category: str  # 'coding' or 'design'
    description: str
    file_path: Optional[str] = None
    system_prompt: str = ""
    tools: List[str] = field(default_factory=list)


class AgentRegistry:
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.agents: Dict[str, AgentPersona] = {}
        self._load_agents()

    def _parse_frontmatter(self, content: str) -> tuple[Dict[str, str], str]:
        """Simple YAML-like frontmatter parser without third-party dependencies."""
        if not content.startswith("---"):
            return {}, content

        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}, content

        front_text = parts[1]
        body = parts[2].strip()

        meta = {}
        for line in front_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("\"'")

        return meta, body

    def _load_agents(self):
        """Scans workspace for agent files in agents/ or .cursor/agents/."""
        search_dirs = [
            self.workspace_root / "agents",
        ]

        for base in search_dirs:
            if not base.exists():
                continue

            for md_file in base.rglob("*.md"):
                try:
                    with open(md_file, "r", encoding="utf-8", errors="replace") as f:
                        text = f.read()

                    meta, body = self._parse_frontmatter(text)
                    name = meta.get("name") or md_file.stem
                    description = meta.get("description") or f"Specialized agent: {name}"
                    category = "design" if "design" in str(md_file.parent) else "coding"

                    self.agents[name.lower()] = AgentPersona(
                        name=name,
                        category=category,
                        description=description,
                        file_path=str(md_file),
                        system_prompt=body or text,
                    )
                except Exception:
                    continue

    def get_agent(self, name: str) -> Optional[AgentPersona]:
        return self.agents.get(name.lower())

    def list_agents(self) -> List[AgentPersona]:
        return sorted(self.agents.values(), key=lambda a: (a.category, a.name))

    def match_agent_for_phase(
        self,
        phase: str,
        tech_hint: str = "",
        task_desc: str = "",
    ) -> AgentPersona:
        """
        Intelligently matches a task to the best specialized agent persona.
        """
        combined = f"{phase} {tech_hint} {task_desc}".lower()

        # 1. TRD / Architecture phase
        if "trd" in combined or "architecture" in combined or "spec" in combined:
            if "dotnet" in combined or ".net" in combined or "c#" in combined:
                if "dotnet-architect" in self.agents:
                    return self.agents["dotnet-architect"]
            if "software-architecture" in self.agents:
                return self.agents["software-architecture"]

        # 2. Context phase
        if "context" in combined:
            if "project-context-analyst" in self.agents:
                return self.agents["project-context-analyst"]

        # 3. RED / Testing phase
        if "red" in combined or "test" in combined:
            if "pytest" in combined or "python" in combined:
                if "pytest-tester" in self.agents:
                    return self.agents["pytest-tester"]
            if "jest" in combined or "typescript" in combined or "javascript" in combined or "node" in combined:
                if "jest-tester" in self.agents:
                    return self.agents["jest-tester"]
            if "xunit" in combined or "dotnet" in combined or ".net" in combined:
                if "xunit-tester" in self.agents:
                    return self.agents["xunit-tester"]
            if "integration" in combined and "integration-tester" in self.agents:
                return self.agents["integration-tester"]

        # 4. GREEN / Implementation phase
        if "green" in combined or "setup" in combined or "implement" in combined:
            if "fastapi" in combined or ("python" in combined and "api" in combined):
                if "fastapi-backend" in self.agents:
                    return self.agents["fastapi-backend"]
            if "angular" in combined and "angular-developer" in self.agents:
                return self.agents["angular-developer"]
            if "aspnet" in combined or ("dotnet" in combined and "backend" in combined):
                if "aspnet-webapi-backend" in self.agents:
                    return self.agents["aspnet-webapi-backend"]
            if "typescript" in combined and "typescript-pro" in self.agents:
                return self.agents["typescript-pro"]
            if "sql" in combined and "sqlserver-database-specialist" in self.agents:
                return self.agents["sqlserver-database-specialist"]

        # 5. Default fallbacks
        if "red" in combined or "test" in combined:
            for candidate in ["jest-tester", "pytest-tester"]:
                if candidate in self.agents:
                    return self.agents[candidate]
            return AgentPersona(
                name="TDD Test Engineer",
                category="coding",
                description="Expert Test-Driven Development engineer writing failing tests first.",
                system_prompt="You are an expert TDD Test Engineer. Your mission in the RED phase is to write comprehensive, cleanly failing unit/integration tests that specify requirements precisely.",
            )

        for candidate in ["typescript-pro", "fastapi-backend", "aspnet-webapi-backend"]:
            if candidate in self.agents:
                return self.agents[candidate]

        return AgentPersona(
            name="Senior Software Engineer",
            category="coding",
            description="Senior full-stack software engineer.",
            system_prompt="You are a Senior Software Engineer responsible for implementing clean, robust, and tested code following strict TDD standards.",
        )
