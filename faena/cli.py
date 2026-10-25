"""
Faena Command Line Interface (CLI).
"""
from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from faena.config import load_env_file, load_config_file
from faena.providers.factory import (
    create_provider,
    auto_detect_provider,
    list_providers_status,
)
from faena.agents.registry import AgentRegistry
from faena.orchestrator.pipeline import FaenaPipeline
from faena.orchestrator.context_engine import ContextEngine
from faena.orchestrator.trd_engine import TRDEngine
from faena.orchestrator.task_engine import TaskEngine
from faena.orchestrator.executor import TaskExecutor
from faena.orchestrator.state import TicketSessionState


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="faena",
        description="🏭 Faena: Autonomous AI Factory for End-to-End Ticket Implementation.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run full pipeline on a ticket (from spec to verified code)")
    run_parser.add_argument("ticket", help="Path to ticket markdown file, issue description, or prompt text")
    run_parser.add_argument("--provider", "-p", help="LLM Provider: claude, chatgpt, gemini, ollama, deepseek, openrouter")
    run_parser.add_argument("--model", "-m", help="Specific model identifier to use")
    run_parser.add_argument("--api-key", help="API key for the chosen provider")
    run_parser.add_argument("--target", "-t", help="Target sub-repository inside Proyecto/ to execute tests and changes in")
    run_parser.add_argument("--interactive", "-i", action="store_true", help="Prompt for confirmation before each major phase")
    run_parser.add_argument("--resume", "-r", action="store_true", help="Resume an existing session if present")

    # Command: init
    init_parser = subparsers.add_parser("init", help="Initialize Faena AI Factory structure in current workspace")

    # Command: project
    subparsers.add_parser("project", help="List and inspect cloned repositories inside Proyecto/ and company rules")

    # Command: context
    ctx_parser = subparsers.add_parser("context", help="Analyze codebase and generate/update tasks/context/ files")

    # Command: trd
    trd_parser = subparsers.add_parser("trd", help="Generate Technical Requirements Document & Test Spec from ticket")
    trd_parser.add_argument("ticket", help="Path to ticket file or prompt")
    trd_parser.add_argument("--provider", "-p", help="LLM Provider")
    trd_parser.add_argument("--model", "-m", help="Model name")

    # Command: tasks
    tasks_parser = subparsers.add_parser("tasks", help="Generate atomic TDD task files from an approved TRD")
    tasks_parser.add_argument("trd", help="Path to trd-*.md file")
    tasks_parser.add_argument("--spec", help="Optional path to test-spec-*.md file (defaults to sibling file)")
    tasks_parser.add_argument("--provider", "-p", help="LLM Provider")

    # Command: providers
    subparsers.add_parser("providers", help="List supported LLM providers and check active API keys")

    # Command: agents
    subparsers.add_parser("agents", help="List available specialized agent personas")

    # Command: status
    subparsers.add_parser("status", help="Show active tickets and execution progress")

    # Command: sync
    sync_parser = subparsers.add_parser("sync", help="Compare and synchronize agents & skills with upstream ECC repo")
    sync_parser.add_argument("--update", "-u", action="store_true", help="Apply updates to all outdated tracked agents and skills")
    sync_parser.add_argument("--import-agent", help="Import a specific agent from ECC (e.g. 'django-reviewer.md')")
    sync_parser.add_argument("--import-skill", help="Import a specific skill directory from ECC (e.g. 'docker-patterns')")
    sync_parser.add_argument("--ecc-path", help="Path to local ECC repository")

    return parser


def cmd_run(args, root: Path, config: dict):
    provider_name = args.provider or config.get("provider")
    model = args.model or config.get("model")
    api_key = args.api_key or config.get("api_key")
    target = args.target or config.get("default_target_repo")

    try:
        provider = create_provider(name=provider_name, model=model, api_key=api_key)
    except Exception as e:
        print(f"❌ Error configuring provider: {e}", file=sys.stderr)
        sys.exit(1)

    pipeline = FaenaPipeline(workspace_root=root, provider=provider)
    pipeline.run_ticket(
        ticket_input=args.ticket,
        target=target,
        auto_approve=not args.interactive,
        resume=args.resume,
    )


def cmd_project(root: Path):
    engine = ContextEngine(workspace_root=root)
    data = engine.detect_all_repositories()
    pdir = data["project_dir"]
    sub_repos = data["sub_repositories"]

    print(f"📁 Project Workspace: {pdir}/\n")
    if not sub_repos:
        print(f"  No repositories cloned in '{pdir}/' yet.")
        print(f"  Clone your company/client repositories here:")
        print(f"    cd {pdir}")
        print(f"    git clone <url-del-repo-de-la-empresa>")
    else:
        print(f"  Found {len(sub_repos)} active client repository(ies):\n")
        for sr in sub_repos:
            techs = ", ".join(set(sr["technologies"])) or "Undetermined"
            remote = f" ({sr['git_remote']})" if sr["git_remote"] else ""
            print(f"  📦 {sr['path']}{remote}")
            print(f"     Branch: {sr['git_branch']} | Tech: {techs}")

    # Check company rules
    rules_dir = root / "rules" / "project"
    rules = [f.name for f in rules_dir.glob("*.md*") if f.name != "README.md"] if rules_dir.exists() else []
    print(f"\n📏 Company Rules ({len(rules)} active in rules/project/):")
    for r in rules:
        print(f"  - {r}")

    # Check company skills
    skills_dir = root / "skills" / "project"
    skills = [f.parent.name for f in skills_dir.rglob("SKILL.md")] if skills_dir.exists() else []
    print(f"\n🧠 Company Skills ({len(skills)} active in skills/project/):")
    for s in skills:
        print(f"  - {s}")


def cmd_init(args, root: Path):
    print("🏭 Initializing Faena AI Factory workspace...")
    dirs = [
        root / "tasks" / "tickets",
        root / "tasks" / "context",
        root / "agents" / "coding",
        root / "agents" / "design",
        root / "rules",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"   Created directory: {d.relative_to(root)}")

    # Create config file if not exists
    config_file = root / "faena.config.json"
    if not config_file.exists():
        sample_config = {
            "provider": "gemini",
            "model": "gemini-2.5-flash",
            "auto_approve": True,
            "max_turns_per_task": 15,
        }
        with open(config_file, "w", encoding="utf-8") as f:
            import json
            json.dump(sample_config, f, indent=2)
        print(f"   Created config file: faena.config.json")

    # Create sample ticket
    sample_ticket = root / "tasks" / "tickets" / "sample-ticket.md"
    if not sample_ticket.exists():
        sample_ticket.write_text("""# Feature: User Activity Logger

## Problem Statement
We need a lightweight service that logs user actions (user_id, action, timestamp) and allows querying actions for a user.

## Requirements
1. Implement an ActivityLogger class with `log_action(user_id, action)` and `get_actions(user_id)`.
2. Persist actions in-memory or in a file.
3. Include unit tests covering normal logging, filtering, and empty queries.
""", encoding="utf-8")
        print(f"   Created sample ticket: tasks/tickets/sample-ticket.md")

    print("\n✅ Faena AI Factory initialized! Run `faena run tasks/tickets/sample-ticket.md` to start.")


def cmd_context(args, root: Path, config: dict):
    print("🔍 Analyzing codebase and creating project context...")
    engine = ContextEngine(workspace_root=root)
    files = engine.build_initial_context()
    for name, path in files.items():
        print(f"   Created context document: {path.relative_to(root)}")
    print("✅ Context creation complete in tasks/context/")


def cmd_trd(args, root: Path, config: dict):
    provider_name = args.provider or config.get("provider")
    model = args.model or config.get("model")
    provider = create_provider(name=provider_name, model=model)
    registry = AgentRegistry(root)

    engine = ContextEngine(root, provider)
    ctx_str = engine.load_synthesized_context()

    ticket_path = Path(args.ticket)
    if ticket_path.exists() and ticket_path.is_file():
        content = ticket_path.read_text(encoding="utf-8")
        title = ticket_path.stem
    else:
        content = args.ticket
        title = args.ticket[:40]

    trd_engine = TRDEngine(root, provider, registry)
    trd_path, spec_path = trd_engine.generate_trd(title, content, ctx_str)
    print(f"✅ TRD created: {trd_path}")
    print(f"✅ Test Spec created: {spec_path}")


def cmd_tasks(args, root: Path, config: dict):
    trd_file = Path(args.trd)
    if not trd_file.exists():
        print(f"❌ TRD file not found: {args.trd}", file=sys.stderr)
        sys.exit(1)

    spec_file = Path(args.spec) if args.spec else trd_file.parent / trd_file.name.replace("trd-", "test-spec-")
    if not spec_file.exists():
        spec_file = trd_file

    provider_name = args.provider or config.get("provider")
    provider = create_provider(name=provider_name)

    engine = TaskEngine(root, provider)
    tasks = engine.generate_tasks(trd_file, spec_file)
    print(f"✅ Generated {len(tasks)} tasks in {trd_file.parent}:")
    for t in tasks:
        print(f"   - Task {t.number:02d} [{t.phase.upper()}]: {t.title}")


def cmd_providers():
    print("🔌 Faena LLM Providers Status:\n")
    statuses = list_providers_status()
    for display_name, internal_name, is_available in statuses:
        status_icon = "🟢 ACTIVE" if is_available else "⚪ NOT CONFIGURED"
        print(f"  {status_icon:<18} {display_name:<20} (--provider {internal_name})")
    print("\nTo configure a provider, export the corresponding API key:")
    print("  export ANTHROPIC_API_KEY='your-key'")
    print("  export OPENAI_API_KEY='your-key'")
    print("  export GEMINI_API_KEY='your-key'")
    print("  export DEEPSEEK_API_KEY='your-key'")
    print("  export OPENROUTER_API_KEY='your-key'")


def cmd_agents(root: Path):
    registry = AgentRegistry(root)
    agents = registry.list_agents()
    print(f"🤖 Available Specialized Agents ({len(agents)} registered):\n")
    for a in agents:
        cat_badge = f"[{a.category.upper()}]"
        print(f"  {cat_badge:<10} {a.name:<32} {a.description[:60]}")


def cmd_status(root: Path):
    tasks_dir = root / "tasks"
    if not tasks_dir.exists():
        print("No tasks/ directory found.")
        return

    sessions = list(tasks_dir.glob("task-*/state.json"))
    if not sessions:
        print("No active or past ticket sessions found.")
        return

    print(f"📊 Found {len(sessions)} Ticket Session(s):\n")
    for sfile in sessions:
        try:
            state = TicketSessionState.load(sfile)
            completed = sum(1 for t in state.tasks if t.status == "completed")
            total = len(state.tasks)
            print(f"  📌 {state.ticket_title} [{state.status.upper()}]")
            print(f"     Folder: tasks/{sfile.parent.name}")
            print(f"     Tasks:  {completed}/{total} completed")
        except Exception:
            continue


def cmd_sync(args, root: Path, config: dict):
    from faena.orchestrator.sync_engine import ECCSyncEngine
    ecc_path = Path(args.ecc_path) if args.ecc_path else Path(config.get("ecc_path", r"C:\Users\santi\Documents\GitHub\ECC"))
    engine = ECCSyncEngine(workspace_root=root, ecc_path=ecc_path)

    if not engine.is_ecc_available():
        print(f"❌ ECC repository not found at: {ecc_path}", file=sys.stderr)
        print("  Specify the path with --ecc-path <path> or in faena.config.json ('ecc_path')", file=sys.stderr)
        sys.exit(1)

    print(f"🔄 Comparing with ECC at: {ecc_path}\n")

    if args.import_agent:
        name = args.import_agent if args.import_agent.endswith(".md") else f"{args.import_agent}.md"
        ok = engine.update_agent(name)
        if ok:
            print(f"✅ Successfully imported agent '{name}' into Faena (agents/coding/)")
        else:
            print(f"❌ Agent '{name}' not found in ECC agents/", file=sys.stderr)
        return

    if args.import_skill:
        ok = engine.update_skill(args.import_skill)
        if ok:
            print(f"✅ Successfully imported skill '{args.import_skill}' into Faena (skills/)")
        else:
            print(f"❌ Skill '{args.import_skill}' not found in ECC skills/", file=sys.stderr)
        return

    if args.update:
        up_agents, up_skills = engine.sync_tracked()
        print(f"🚀 Updated {len(up_agents)} agent(s) and {len(up_skills)} skill(s) from ECC:")
        for a in up_agents:
            print(f"   - Agent updated: {a}")
        for s in up_skills:
            print(f"   - Skill updated: {s}")
        if not up_agents and not up_skills:
            print("   ✨ Everything tracked is already up to date!")
        return

    agent_comp = engine.compare_agents()
    skill_comp = engine.compare_skills()

    print("📊 AGENTS COMPARISON:")
    print(f"  🟢 Up to date with ECC:  {len(agent_comp['up_to_date'])}")
    print(f"  🔄 Outdated (updates):   {len(agent_comp['outdated'])}")
    for item in agent_comp['outdated']:
        print(f"     - {item['name']}")
    print(f"  ⭐ Faena Custom:         {len(agent_comp['faena_custom'])}")
    print(f"  💡 Available in ECC:     {len(agent_comp['available_in_ecc'])}")

    print("\n📊 SKILLS COMPARISON:")
    print(f"  🟢 Up to date with ECC:  {len(skill_comp['up_to_date'])}")
    print(f"  🔄 Outdated (updates):   {len(skill_comp['outdated'])}")
    for item in skill_comp['outdated']:
        print(f"     - {item['name']}")
    print(f"  ⭐ Faena Custom:         {len(skill_comp['faena_custom'])}")
    print(f"  💡 Available in ECC:     {len(skill_comp['available_in_ecc'])}")

    if agent_comp['outdated'] or skill_comp['outdated']:
        print("\n💡 Run `faena sync --update` to apply upstream updates to existing tracked files.")
    else:
        print("\n✨ All tracked agents and skills match ECC upstream.")
    print("💡 To import a new skill: `faena sync --import-skill <skill-name>`")
    print("💡 To import a new agent: `faena sync --import-agent <agent-name>`")


def main():
    root = Path.cwd()
    load_env_file(root / ".env")
    config = load_config_file(root / "faena.config.json")

    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "run":
        cmd_run(args, root, config)
    elif args.command == "init":
        cmd_init(args, root)
    elif args.command == "project":
        cmd_project(root)
    elif args.command == "context":
        cmd_context(args, root, config)
    elif args.command == "trd":
        cmd_trd(args, root, config)
    elif args.command == "tasks":
        cmd_tasks(args, root, config)
    elif args.command == "providers":
        cmd_providers()
    elif args.command == "agents":
        cmd_agents(root)
    elif args.command == "status":
        cmd_status(root)
    elif args.command == "sync":
        cmd_sync(args, root, config)


if __name__ == "__main__":
    main()
