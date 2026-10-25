"""
Search tools for codebase navigation.
"""
from __future__ import annotations
import os
import re
from pathlib import Path
from typing import List, Optional


def search_code(
    query: str,
    path: str = ".",
    extensions: Optional[List[str]] = None,
    case_sensitive: bool = False,
    max_results: int = 50,
) -> str:
    """
    Search for a text snippet or pattern across files in the codebase.
    """
    root = Path(path).resolve()
    if not root.exists():
        return f"Path not found: {path}"

    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        regex = re.compile(query, flags)
    except Exception:
        regex = re.compile(re.escape(query), flags)

    matches = []
    ignored_dirs = {".git", "node_modules", "__pycache__", ".venv", "dist", "build", ".mypy_cache"}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if extensions and ext not in extensions:
                continue

            fpath = Path(dirpath) / fname
            rel_path = fpath.relative_to(root)

            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line_idx, line in enumerate(f, 1):
                        if regex.search(line):
                            matches.append(f"{rel_path}:{line_idx}: {line.strip()[:140]}")
                            if len(matches) >= max_results:
                                break
            except Exception:
                continue

            if len(matches) >= max_results:
                break
        if len(matches) >= max_results:
            break

    if not matches:
        return f"No matches found for '{query}'"

    res = f"Found {len(matches)} match(es):\n" + "\n".join(matches)
    if len(matches) >= max_results:
        res += f"\n... (truncated at {max_results} results)"
    return res


def find_files(pattern: str, path: str = ".") -> str:
    """
    Find files matching a glob pattern (e.g. '*.py', '*service*', 'test_*.ts').
    """
    root = Path(path).resolve()
    if not root.exists():
        return f"Path not found: {path}"

    matches = []
    ignored = {".git", "node_modules", "__pycache__", ".venv", "dist", "build"}

    for p in root.rglob(pattern):
        if any(ign in p.parts for ign in ignored):
            continue
        rel = p.relative_to(root)
        matches.append(str(rel))
        if len(matches) >= 60:
            break

    if not matches:
        return f"No files matching '{pattern}' in {path}"

    matches.sort()
    return f"Matched {len(matches)} file(s):\n" + "\n".join(matches)
