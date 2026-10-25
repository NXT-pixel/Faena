"""
Central tool registry for Faena agents.
"""
from __future__ import annotations
import json
from typing import Any, Callable, Dict, List
from faena.providers.base import ToolDefinition
from faena.tools.file_tools import read_file, write_file, edit_file, list_dir, file_exists
from faena.tools.shell_tools import run_command
from faena.tools.search_tools import search_code, find_files


TOOL_SCHEMAS: List[ToolDefinition] = [
    ToolDefinition(
        name="read_file",
        description="Reads the contents of a file, optionally between start_line and end_line (1-indexed).",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative or absolute path to the file to read."},
                "start_line": {"type": "integer", "description": "Optional start line number (1-based)."},
                "end_line": {"type": "integer", "description": "Optional end line number (inclusive)."},
            },
            "required": ["path"],
        },
    ),
    ToolDefinition(
        name="write_file",
        description="Creates or overwrites a file with the given content.",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file to write."},
                "content": {"type": "string", "description": "Full file content to write."},
                "overwrite": {"type": "boolean", "description": "Whether to overwrite if file exists (default: true)."},
            },
            "required": ["path", "content"],
        },
    ),
    ToolDefinition(
        name="edit_file",
        description="Replaces an exact text snippet in a file with replacement content.",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file to edit."},
                "target": {"type": "string", "description": "Exact text string to find and replace."},
                "replacement": {"type": "string", "description": "Replacement text string."},
            },
            "required": ["path", "target", "replacement"],
        },
    ),
    ToolDefinition(
        name="list_dir",
        description="Lists the files and folders inside a directory.",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory path to list (default: current directory '.')."},
                "recursive": {"type": "boolean", "description": "Whether to list subdirectories recursively."},
                "max_depth": {"type": "integer", "description": "Maximum directory depth if recursive (default: 2)."},
            },
            "required": [],
        },
    ),
    ToolDefinition(
        name="run_command",
        description="Executes a shell command (tests, builds, linters, git commands) and returns stdout/stderr and exit code.",
        parameters={
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command line to execute."},
                "cwd": {"type": "string", "description": "Optional working directory for execution."},
                "timeout": {"type": "integer", "description": "Timeout in seconds (default: 90)."},
            },
            "required": ["command"],
        },
    ),
    ToolDefinition(
        name="search_code",
        description="Searches for a string pattern across files in the codebase.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Text query or regex to search for."},
                "path": {"type": "string", "description": "Base directory to search in (default: '.')."},
                "case_sensitive": {"type": "boolean", "description": "Case-sensitive search (default: false)."},
            },
            "required": ["query"],
        },
    ),
    ToolDefinition(
        name="find_files",
        description="Finds files matching a glob pattern (e.g. '*.py', '*.ts', 'test_*').",
        parameters={
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Glob pattern to match."},
                "path": {"type": "string", "description": "Base directory to search in (default: '.')."},
            },
            "required": ["pattern"],
        },
    ),
    ToolDefinition(
        name="file_exists",
        description="Checks if a file or directory exists.",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to test."},
            },
            "required": ["path"],
        },
    ),
]


TOOL_FUNCTIONS: Dict[str, Callable[..., Any]] = {
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "list_dir": list_dir,
    "run_command": run_command,
    "search_code": search_code,
    "find_files": find_files,
    "file_exists": file_exists,
}


def get_default_tools() -> List[ToolDefinition]:
    return list(TOOL_SCHEMAS)


def execute_tool(name: str, args: Dict[str, Any]) -> str:
    """Executes a tool by name with arguments and returns string output."""
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return f"Error: Tool '{name}' not found. Available tools: {list(TOOL_FUNCTIONS.keys())}"

    try:
        res = func(**args)
        return str(res)
    except Exception as e:
        return f"Error executing tool '{name}': {e}"
