"""
Sync Engine: Compares and updates Faena agents and skills with ECC (Enterprise Coding Companion).
Protects project/ company customizations from being overwritten.
"""
from __future__ import annotations
import hashlib
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ECCSyncEngine:
    DEFAULT_ECC_PATH = Path(r"C:\Users\santi\Documents\GitHub\ECC")

    def __init__(self, workspace_root: Path, ecc_path: Optional[Path] = None):
        self.workspace_root = workspace_root.resolve()
        self.ecc_path = (ecc_path or self.DEFAULT_ECC_PATH).resolve()

    def is_ecc_available(self) -> bool:
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
        """Computes combined hash of all files in a directory."""
        if not dir_path.exists() or not dir_path.is_dir():
            return ""
        hasher = hashlib.sha256()
        for p in sorted(dir_path.rglob("*")):
            if p.is_file():
                hasher.update(p.name.encode())
                hasher.update(p.read_bytes())
        return hasher.hexdigest()

    def compare_agents(self) -> Dict[str, List[Dict[str, Any]]]:
        """Compares agents between Faena and ECC."""
        results = {
            "outdated": [],       # Exists in both, but content differs (ECC has update)
            "up_to_date": [],     # Content matches exactly
            "available_in_ecc": [], # Exists in ECC but not in Faena
            "faena_custom": [],   # Exists only in Faena (custom agent)
        }

        if not self.is_ecc_available():
            return results

        ecc_agents_dir = self.ecc_path / "agents"
        ecc_agents = {f.name: f for f in ecc_agents_dir.glob("*.md")}

        # Find all Faena agents across agents/coding and agents/design
        faena_agents: Dict[str, Path] = {}
        for p in (self.workspace_root / "agents").rglob("*.md"):
            if "project" in p.parts:
                continue  # Skip company-specific agents
            faena_agents[p.name] = p

        # Compare existing Faena agents
        for name, fpath in sorted(faena_agents.items()):
            if name in ecc_agents:
                f_hash = self._file_hash(fpath)
                e_hash = self._file_hash(ecc_agents[name])
                item = {
                    "name": name,
                    "faena_path": fpath,
                    "ecc_path": ecc_agents[name],
                }
                if f_hash == e_hash:
                    results["up_to_date"].append(item)
                else:
                    results["outdated"].append(item)
            else:
                results["faena_custom"].append({"name": name, "path": fpath})

        # Find ECC agents not in Faena
        for name, epath in sorted(ecc_agents.items()):
            if name not in faena_agents:
                results["available_in_ecc"].append({"name": name, "ecc_path": epath})

        return results

    def compare_skills(self) -> Dict[str, List[Dict[str, Any]]]:
        """Compares skills between Faena and ECC."""
        results = {
            "outdated": [],
            "up_to_date": [],
            "available_in_ecc": [],
            "faena_custom": [],
        }

        if not self.is_ecc_available():
            return results

        ecc_skills_dir = self.ecc_path / "skills"
        ecc_skills = {d.name: d for d in ecc_skills_dir.iterdir() if d.is_dir()}

        faena_skills_dir = self.workspace_root / "skills"
        faena_skills = {d.name: d for d in faena_skills_dir.iterdir() if d.is_dir() and d.name != "project"}

        for name, fdir in sorted(faena_skills.items()):
            if name in ecc_skills:
                f_hash = self._dir_hash(fdir)
                e_hash = self._dir_hash(ecc_skills[name])
                item = {
                    "name": name,
                    "faena_dir": fdir,
                    "ecc_dir": ecc_skills[name],
                }
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

    def update_agent(self, agent_name: str) -> bool:
        """Updates a specific agent from ECC to Faena."""
        ecc_agent = self.ecc_path / "agents" / agent_name
        if not ecc_agent.exists():
            return False

        # Find where it lives in Faena, or default to agents/coding/
        target_file = None
        for p in (self.workspace_root / "agents").rglob("*.md"):
            if p.name == agent_name and "project" not in p.parts:
                target_file = p
                break

        if not target_file:
            target_file = self.workspace_root / "agents" / "coding" / agent_name

        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ecc_agent, target_file)
        return True

    def update_skill(self, skill_name: str) -> bool:
        """Updates or imports a specific skill from ECC to Faena."""
        ecc_skill = self.ecc_path / "skills" / skill_name
        if not ecc_skill.exists() or not ecc_skill.is_dir():
            return False

        target_skill_dir = self.workspace_root / "skills" / skill_name
        if target_skill_dir.exists():
            shutil.rmtree(target_skill_dir)

        shutil.copytree(ecc_skill, target_skill_dir)
        return True

    def sync_tracked(self) -> Tuple[List[str], List[str]]:
        """
        Updates all tracked agents and skills that are outdated in Faena.
        Does NOT copy all 300+ ECC skills, only updates what Faena already uses!
        """
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
