"""
Sync Engine: Compares, updates, and just-in-time (JIT) imports agents and skills from ECC.
Supports both local ECC clone and direct remote GitHub fallback (https://github.com/affaan-m/ECC).
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import shutil
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# Known mapping of technology keywords to ECC skills and agents
TECH_ECOSYSTEM_MAP: Dict[str, Dict[str, List[str]]] = {
    "react": {
        "skills": ["react-patterns", "react-testing"],
        "agents": ["react-reviewer.md", "react-build-resolver.md"],
    },
    "nextjs": {
        "skills": ["react-patterns", "nextjs-turbopack"],
        "agents": ["react-reviewer.md"],
    },
    "next.js": {
        "skills": ["react-patterns", "nextjs-turbopack"],
        "agents": ["react-reviewer.md"],
    },
    "vue": {
        "skills": ["vue-patterns"],
        "agents": ["vue-reviewer.md"],
    },
    "nuxt": {
        "skills": ["nuxt4-patterns"],
        "agents": ["vue-reviewer.md"],
    },
    "django": {
        "skills": ["django-patterns", "django-tdd"],
        "agents": ["django-reviewer.md", "django-build-resolver.md"],
    },
    "spring": {
        "skills": ["springboot-patterns", "springboot-tdd"],
        "agents": ["java-reviewer.md", "java-build-resolver.md"],
    },
    "springboot": {
        "skills": ["springboot-patterns", "springboot-tdd"],
        "agents": ["java-reviewer.md", "java-build-resolver.md"],
    },
    "golang": {
        "skills": ["golang-patterns", "golang-testing"],
        "agents": ["go-reviewer.md", "go-build-resolver.md"],
    },
    "go": {
        "skills": ["golang-patterns", "golang-testing"],
        "agents": ["go-reviewer.md", "go-build-resolver.md"],
    },
    "rust": {
        "skills": ["rust-patterns", "rust-testing"],
        "agents": ["rust-reviewer.md", "rust-build-resolver.md"],
    },
    "kubernetes": {
        "skills": ["kubernetes-patterns"],
        "agents": [],
    },
    "k8s": {
        "skills": ["kubernetes-patterns"],
        "agents": [],
    },
    "docker": {
        "skills": ["docker-patterns"],
        "agents": [],
    },
    "postgres": {
        "skills": ["postgres-patterns"],
        "agents": ["database-reviewer.md"],
    },
    "postgresql": {
        "skills": ["postgres-patterns"],
        "agents": ["database-reviewer.md"],
    },
    "redis": {
        "skills": ["redis-patterns"],
        "agents": [],
    },
    "prisma": {
        "skills": ["prisma-patterns"],
        "agents": [],
    },
    "nestjs": {
        "skills": ["nestjs-patterns"],
        "agents": ["typescript-reviewer.md"],
    },
    "graphql": {
        "skills": ["api-connector-builder"],
        "agents": [],
    },
    "flutter": {
        "skills": ["dart-flutter-patterns"],
        "agents": ["flutter-reviewer.md", "dart-build-resolver.md"],
    },
    "dart": {
        "skills": ["dart-flutter-patterns"],
        "agents": ["dart-build-resolver.md"],
    },
    "laravel": {
        "skills": ["laravel-patterns", "laravel-tdd"],
        "agents": ["php-reviewer.md"],
    },
    "php": {
        "skills": ["laravel-patterns"],
        "agents": ["php-reviewer.md"],
    },
    "rails": {
        "skills": ["rails-patterns"],
        "agents": ["ruby-reviewer.md"],
    },
    "ruby": {
        "skills": ["rails-patterns"],
        "agents": ["ruby-reviewer.md"],
    },
    "e2e": {
        "skills": ["e2e-testing"],
        "agents": ["e2e-runner.md"],
    },
    "playwright": {
        "skills": ["e2e-testing"],
        "agents": ["e2e-runner.md"],
    },
    "cypress": {
        "skills": ["e2e-testing"],
        "agents": ["e2e-runner.md"],
    },
    "kotlin": {
        "skills": ["kotlin-patterns", "kotlin-testing"],
        "agents": ["kotlin-reviewer.md", "kotlin-build-resolver.md"],
    },
    "swift": {
        "skills": ["swiftui-patterns"],
        "agents": ["swift-reviewer.md", "swift-build-resolver.md"],
    },
}


class ECCSyncEngine:
    DEFAULT_LOCAL_ECC_PATH = Path(r"C:\Users\santi\Documents\GitHub\ECC")
    REMOTE_GITHUB_RAW = "https://raw.githubusercontent.com/affaan-m/ECC/main"
    REMOTE_GITHUB_API = "https://api.github.com/repos/affaan-m/ECC/contents"

    def __init__(self, workspace_root: Path, ecc_path: Optional[Path] = None):
        self.workspace_root = workspace_root.resolve()
        self.ecc_path = (ecc_path or self.DEFAULT_LOCAL_ECC_PATH).resolve()

    def is_local_ecc_available(self) -> bool:
        return self.ecc_path.exists() and (self.ecc_path / "agents").exists()

    def _file_hash(self, path: Path) -> str:
        if not path.exists() or not path.is_file():
            return ""
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _dir_hash(self, dir_path: Path) -> str:
        if not dir_path.exists() or not dir_path.is_dir():
            return ""
        hasher = hashlib.sha256()
        for p in sorted(dir_path.rglob("*")):
            if p.is_file():
                hasher.update(p.name.encode())
                hasher.update(p.read_bytes())
        return hasher.hexdigest()

    def fetch_remote_file(self, relative_path: str) -> Optional[bytes]:
        """Fetches a file from GitHub repository raw content."""
        clean_path = relative_path.replace("\\", "/").lstrip("/")
        url = f"{self.REMOTE_GITHUB_RAW}/{clean_path}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Faena-AI-Factory"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read()
        except Exception:
            return None

    def fetch_remote_directory(self, remote_dir_path: str, target_dir: Path) -> bool:
        """Fetches directory contents recursively using GitHub API or fallback."""
        clean_path = remote_dir_path.replace("\\", "/").lstrip("/")
        url = f"{self.REMOTE_GITHUB_API}/{clean_path}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Faena-AI-Factory"})
            with urllib.request.urlopen(req, timeout=25) as resp:
                items = json.loads(resp.read().decode("utf-8"))

            target_dir.mkdir(parents=True, exist_ok=True)
            for item in items:
                name = item.get("name", "")
                itype = item.get("type", "")
                ipath = item.get("path", "")
                if itype == "file":
                    file_bytes = self.fetch_remote_file(ipath)
                    if file_bytes:
                        (target_dir / name).write_bytes(file_bytes)
                elif itype == "dir":
                    self.fetch_remote_directory(ipath, target_dir / name)
            return True
        except Exception:
            # Fallback: at least fetch SKILL.md
            skill_bytes = self.fetch_remote_file(f"{clean_path}/SKILL.md")
            if skill_bytes:
                target_dir.mkdir(parents=True, exist_ok=True)
                (target_dir / "SKILL.md").write_bytes(skill_bytes)
                return True
            return False

    def update_agent(self, agent_name: str) -> bool:
        """Updates or imports a specific agent from local ECC or remote GitHub."""
        name = agent_name if agent_name.endswith(".md") else f"{agent_name}.md"

        # Determine target file in Faena
        target_file = None
        for p in (self.workspace_root / "agents").rglob("*.md"):
            if p.name == name and "project" not in p.parts:
                target_file = p
                break
        if not target_file:
            target_file = self.workspace_root / "agents" / "coding" / name

        target_file.parent.mkdir(parents=True, exist_ok=True)

        # 1. Try local ECC
        if self.is_local_ecc_available():
            local_src = self.ecc_path / "agents" / name
            if local_src.exists():
                shutil.copy2(local_src, target_file)
                return True

        # 2. Fallback to remote GitHub
        remote_bytes = self.fetch_remote_file(f"agents/{name}")
        if remote_bytes:
            target_file.write_bytes(remote_bytes)
            return True

        return False

    def update_skill(self, skill_name: str) -> bool:
        """Updates or imports a specific skill from local ECC or remote GitHub."""
        clean_name = skill_name.strip("/\\")
        target_dir = self.workspace_root / "skills" / clean_name

        # 1. Try local ECC
        if self.is_local_ecc_available():
            local_dir = self.ecc_path / "skills" / clean_name
            if local_dir.exists() and local_dir.is_dir():
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.copytree(local_dir, target_dir)
                return True

        # 2. Fallback to remote GitHub
        if target_dir.exists():
            shutil.rmtree(target_dir)
        return self.fetch_remote_directory(f"skills/{clean_name}", target_dir)

    def compare_agents(self) -> Dict[str, List[Dict[str, Any]]]:
        results = {
            "outdated": [],
            "up_to_date": [],
            "available_in_ecc": [],
            "faena_custom": [],
        }

        if not self.is_local_ecc_available():
            return results

        ecc_agents_dir = self.ecc_path / "agents"
        ecc_agents = {f.name: f for f in ecc_agents_dir.glob("*.md")}

        faena_agents: Dict[str, Path] = {}
        for p in (self.workspace_root / "agents").rglob("*.md"):
            if "project" in p.parts:
                continue
            faena_agents[p.name] = p

        for name, fpath in sorted(faena_agents.items()):
            if name in ecc_agents:
                f_hash = self._file_hash(fpath)
                e_hash = self._file_hash(ecc_agents[name])
                item = {"name": name, "faena_path": fpath, "ecc_path": ecc_agents[name]}
                if f_hash == e_hash:
                    results["up_to_date"].append(item)
                else:
                    results["outdated"].append(item)
            else:
                results["faena_custom"].append({"name": name, "path": fpath})

        for name, epath in sorted(ecc_agents.items()):
            if name not in faena_agents:
                results["available_in_ecc"].append({"name": name, "ecc_path": epath})

        return results

    def compare_skills(self) -> Dict[str, List[Dict[str, Any]]]:
        results = {
            "outdated": [],
            "up_to_date": [],
            "available_in_ecc": [],
            "faena_custom": [],
        }

        if not self.is_local_ecc_available():
            return results

        ecc_skills_dir = self.ecc_path / "skills"
        ecc_skills = {d.name: d for d in ecc_skills_dir.iterdir() if d.is_dir()}

        faena_skills_dir = self.workspace_root / "skills"
        faena_skills = {d.name: d for d in faena_skills_dir.iterdir() if d.is_dir() and d.name != "project"}

        for name, fdir in sorted(faena_skills.items()):
            if name in ecc_skills:
                f_hash = self._dir_hash(fdir)
                e_hash = self._dir_hash(ecc_skills[name])
                item = {"name": name, "faena_dir": fdir, "ecc_dir": ecc_skills[name]}
                if f_hash == e_hash:
                    results["up_to_date"].append(item)
                else:
                    results["outdated"].append(item)
            else:
                results["faena_custom"].append({"name": name, "dir": fdir})

        for name, edir in sorted(ecc_skills.items()):
            if name not in faena_skills:
                results["available_in_ecc"].append({"name": name, "ecc_dir": edir})

        return results

    def sync_tracked(self) -> Tuple[List[str], List[str]]:
        updated_agents = []
        updated_skills = []

        agent_comparison = self.compare_agents()
        for item in agent_comparison["outdated"]:
            if self.update_agent(item["name"]):
                updated_agents.append(item["name"])

        skill_comparison = self.compare_skills()
        for item in skill_comparison["outdated"]:
            if self.update_skill(item["name"]):
                updated_skills.append(item["name"])

        return updated_agents, updated_skills

    def auto_discover_and_import(self, ticket_content: str) -> Dict[str, List[str]]:
        """
        Scans ticket content for required technologies.
        If Faena does not have the corresponding skills or agents, it automatically imports
        them Just-In-Time (JIT) from ECC (local or remote GitHub).
        """
        imported_skills: List[str] = []
        imported_agents: List[str] = []

        lower_content = ticket_content.lower()

        # Existing skills in Faena
        existing_skills: Set[str] = set()
        skills_dir = self.workspace_root / "skills"
        if skills_dir.exists():
            existing_skills = {d.name.lower() for d in skills_dir.iterdir() if d.is_dir()}

        # Existing agents in Faena
        existing_agents: Set[str] = set()
        agents_dir = self.workspace_root / "agents"
        if agents_dir.exists():
            existing_agents = {p.name.lower() for p in agents_dir.rglob("*.md")}

        # Check technologies from TECH_ECOSYSTEM_MAP
        for keyword, mappings in TECH_ECOSYSTEM_MAP.items():
            pattern = rf"\b{re.escape(keyword)}\b"
            if re.search(pattern, lower_content):
                for sname in mappings.get("skills", []):
                    if sname.lower() not in existing_skills:
                        if self.update_skill(sname):
                            imported_skills.append(sname)
                            existing_skills.add(sname.lower())

                for aname in mappings.get("agents", []):
                    if aname.lower() not in existing_agents:
                        if self.update_agent(aname):
                            imported_agents.append(aname)
                            existing_agents.add(aname.lower())

        return {
            "skills": imported_skills,
            "agents": imported_agents,
        }
