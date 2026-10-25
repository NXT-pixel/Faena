"""
File operations tools for Faena autonomous agents.
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Dict, Any, Optional


def read_file(path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
    """Read the contents of a file, optionally between start_line and end_line (1-indexed)."""
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if p.is_dir():
        raise IsADirectoryError(f"Path is a directory: {path}")

    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        raise IOError(f"Could not read file {path}: {e}")

    total_lines = len(lines)
    start = max(1, start_line or 1) - 1
    end = min(total_lines, end_line or total_lines)

    selected_lines = lines[start:end]
    numbered = [f"{i + start + 1}: {line}" for i, line in enumerate(selected_lines)]
    header = f"[{path} ({start + 1}-{end} of {total_lines} lines)]\n"
    return header + "".join(numbered)


def write_file(path: str, content: str, overwrite: bool = True) -> str:
    """Create or overwrite a file with given content."""
    p = Path(path).resolve()
    if p.exists() and not overwrite:
        raise FileExistsError(f"File already exists and overwrite is False: {path}")

    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Successfully wrote {len(content)} characters to {path}"


def edit_file(path: str, target: str, replacement: str) -> str:
    """Replace an exact string in a file with replacement content."""
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(p, "r", encoding="utf-8", errors="replace") as f:
        data = f.read()

    if target not in data:
        raise ValueError(f"Target string not found in {path}. Make sure whitespace and formatting match exactly.")

    count = data.count(target)
    new_data = data.replace(target, replacement)

    with open(p, "w", encoding="utf-8") as f:
        f.write(new_data)

    return f"Successfully replaced {count} occurrence(s) in {path}"


def list_dir(path: str = ".", recursive: bool = False, max_depth: int = 2) -> str:
    """List contents of a directory."""
    root = Path(path).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {path}")
    if not root.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")

    items = []
    if recursive:
        for p in root.rglob("*"):
            # skip .git, node_modules, __pycache__, .venv
            parts = p.parts
            if any(x in parts for x in (".git", "node_modules", "__pycache__", ".venv", ".mypy_cache")):
                continue
            rel = p.relative_to(root)
            if len(rel.parts) <= max_depth:
                t = "[DIR] " if p.is_dir() else "[FILE]"
                items.append(f"{t} {rel}")
    else:
        for p in root.iterdir():
            if p.name in (".git", "node_modules", "__pycache__", ".venv"):
                continue
            t = "[DIR] " if p.is_dir() else "[FILE]"
            items.append(f"{t} {p.name}")

    items.sort()
    return f"Directory listing for {path} ({len(items)} items):\n" + "\n".join(items)


def file_exists(path: str) -> str:
    """Check if a file exists."""
    p = Path(path)
    return "true" if p.exists() else "false"
