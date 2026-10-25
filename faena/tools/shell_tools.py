"""
Shell execution tools for Faena autonomous agents.
"""
from __future__ import annotations
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional


def run_command(command: str, cwd: Optional[str] = None, timeout: int = 90) -> str:
    """
    Run a terminal command (e.g. tests, linters, builds, git status) and return the output.
    """
    work_dir = Path(cwd).resolve() if cwd else Path.cwd()
    if not work_dir.exists():
        return f"Error: Working directory does not exist: {cwd}"

    # Use PowerShell on Windows if available, otherwise default shell
    if sys.platform == "win32":
        shell_cmd = ["powershell", "-NoProfile", "-NonInteractive", "-Command", command]
    else:
        shell_cmd = ["/bin/bash", "-c", command]

    try:
        proc = subprocess.run(
            shell_cmd,
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        out = proc.stdout.strip()
        err = proc.stderr.strip()
        code = proc.returncode

        res = [f"Exit code: {code}"]
        if out:
            res.append(f"STDOUT:\n{out}")
        if err:
            res.append(f"STDERR:\n{err}")
        if not out and not err:
            res.append("(No output produced)")

        return "\n\n".join(res)
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds: {command}"
    except Exception as e:
        return f"Error executing command: {e}"
