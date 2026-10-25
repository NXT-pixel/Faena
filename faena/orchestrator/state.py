"""
State management and checkpointing for Faena Factory runs.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class TaskItem:
    id: str
    number: int
    phase: str  # 'setup', 'red', 'green', 'verify'
    title: str
    file_path: str
    status: str = "pending"  # 'pending', 'running', 'completed', 'failed'
    agent: str = ""
    error_message: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class TicketSessionState:
    ticket_id: str
    ticket_title: str
    workspace_dir: str
    created_at: str
    updated_at: str
    status: str = "initialized"  # 'initialized', 'trd_ready', 'tasks_ready', 'executing', 'completed', 'failed'
    current_phase: str = "planning"
    trd_file: Optional[str] = None
    test_spec_file: Optional[str] = None
    task_dir: Optional[str] = None
    tasks: List[TaskItem] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> TicketSessionState:
        tasks_data = data.pop("tasks", [])
        tasks = [TaskItem(**t) for t in tasks_data]
        return cls(tasks=tasks, **data)

    def save(self, filepath: Path):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        self.updated_at = datetime.now(timezone.utc).isoformat()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, filepath: Path) -> TicketSessionState:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
