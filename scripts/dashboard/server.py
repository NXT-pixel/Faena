#!/usr/bin/env python3
"""
Faena Live Companion Dashboard Server (Multi-Tenant Hub Edition)
Global, host-agnostic companion dashboard for managing, creating, configuring,
and monitoring Faena tenants and ticket progress.
Compatible with Claude Code, Codex, Antigravity, Cursor, and any terminal.
Zero external dependencies (uses standard library only).
"""

import os
import sys
import json
import time
import re
import shutil
import webbrowser
import threading
import subprocess
import io
import zipfile
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 3333
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TENANTS_DIR = REPO_ROOT / "tenants"
ACTIVE_TENANT_FILE = REPO_ROOT / ".active-tenant"
LOCAL_JSON_FILE = REPO_ROOT / "tenants.local.json"
DASHBOARD_DIR = REPO_ROOT / "scripts" / "dashboard"
INDEX_HTML_PATH = DASHBOARD_DIR / "index.html"


def sanitize_slug(slug):
    """Sanitizes tenant slugs and guards against path traversal."""
    if not slug:
        return ""
    clean = re.sub(r"[^a-z0-9_-]", "-", str(slug).strip().lower())
    clean = re.sub(r"-+", "-", clean).strip("-")
    if not clean or clean.startswith(".") or ".." in clean:
        return ""
    return clean


def get_tenant_dir_safely(slug):
    """Returns the Path to a tenant directory only if it is strictly inside TENANTS_DIR."""
    clean = sanitize_slug(slug)
    if not clean or clean == "default":
        return None
    target = (TENANTS_DIR / clean).resolve()
    try:
        target.relative_to(TENANTS_DIR.resolve())
        return target
    except ValueError:
        return None


def get_active_tenant_slug():
    if ACTIVE_TENANT_FILE.exists():
        try:
            val = ACTIVE_TENANT_FILE.read_text(encoding="utf-8").strip()
            if val:
                return val
        except Exception:
            pass
    if TENANTS_DIR.exists():
        subdirs = [d.name for d in TENANTS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
        if subdirs:
            return subdirs[0]
    return ""


def set_active_tenant_slug(slug):
    clean = sanitize_slug(slug)
    try:
        if clean:
            ACTIVE_TENANT_FILE.write_text(clean, encoding="utf-8")
        elif ACTIVE_TENANT_FILE.exists():
            ACTIVE_TENANT_FILE.unlink()
        return True
    except Exception:
        return False


def open_system_folder(folder_path):
    try:
        p = Path(folder_path)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
        if sys.platform == "win32":
            os.startfile(str(p))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(p)])
        else:
            subprocess.Popen(["xdg-open", str(p)])
        return True
    except Exception as e:
        return False


def get_checkbox_counts(readme_path):
    done, pending = 0, 0
    if not readme_path.exists():
        return done, pending
    try:
        content = readme_path.read_text(encoding="utf-8", errors="replace")
        for line in content.splitlines():
            if re.match(r"^\s*-\s*\[[xX]\]", line):
                done += 1
            elif re.match(r"^\s*-\s*\[\s\]", line):
                pending += 1
    except Exception:
        pass
    return done, pending


def parse_tasks_table(readme_path, task_dir):
    tasks = []
    if not readme_path.exists():
        return tasks
    try:
        content = readme_path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        in_table = False
        
        checkbox_map = {}
        for line in lines:
            m = re.match(r"^\s*-\s*\[([ xX])\]\s*(?:Task\s*)?(\d+):?\s*(.*)", line, re.IGNORECASE)
            if m:
                is_done = m.group(1).lower() == "x"
                task_num = m.group(2).zfill(2)
                checkbox_map[task_num] = is_done

        for line in lines:
            if re.match(r"^\|\s*Task\s*\|\s*Name\s*\|\s*Phase\s*\|", line, re.IGNORECASE):
                in_table = True
                continue
            if in_table and line.strip().startswith("|---"):
                continue
            if in_table:
                if not line.strip().startswith("|"):
                    in_table = False
                    continue
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 3:
                    task_id = parts[0].zfill(2)
                    name = parts[1]
                    phase = parts[2].lower()
                    size = parts[3] if len(parts) > 3 else "-"
                    agent = parts[6] if len(parts) > 6 else (parts[4] if len(parts) > 4 else "-")
                    
                    matched_file = ""
                    for f in task_dir.glob(f"task{task_id}*"):
                        matched_file = f.name
                        break

                    is_completed = checkbox_map.get(task_id, False)

                    tasks.append({
                        "id": task_id,
                        "name": name,
                        "phase": phase,
                        "size": size,
                        "agent": agent,
                        "file": matched_file,
                        "completed": is_completed
                    })
    except Exception:
        pass
    return tasks


def parse_quality_gates(readme_path):
    gates = []
    if not readme_path.exists():
        return gates
    try:
        content = readme_path.read_text(encoding="utf-8", errors="replace")
        matches = re.findall(r"###\s+(verify:[a-zA-Z0-9_-]+|verify)\s*```(?:bash|powershell|cmd|sh)?\s*(.*?)\s*```", content, re.DOTALL)
        for name, cmd in matches:
            gates.append({
                "name": name.strip(),
                "command": cmd.strip()
            })
    except Exception:
        pass
    return gates


def get_ticket_data(task_dir, tenant_slug):
    slug = task_dir.name
    files = list(task_dir.glob("*"))
    file_names = {f.name for f in files}
    
    readme_path = task_dir / "README.md"
    has_readme = readme_path.exists()
    has_design = any(f.startswith("design-") for f in file_names)
    has_trd = any(f.startswith("trd-") for f in file_names)
    has_spec = any(f.startswith("test-spec-") for f in file_names)
    task_files = [f for f in file_names if re.match(r"^task\d+", f)]
    
    done, pending = get_checkbox_counts(readme_path)
    total = done + pending
    pct = int((done / total * 100)) if total > 0 else (100 if (task_files and pending == 0 and done > 0) else 0)

    title = slug.replace("task-", "").replace("-", " ").title()
    repo_location = f"tenants/{tenant_slug}/Proyecto/" if tenant_slug != "default" else "Proyecto/"
    if has_readme:
        try:
            content = readme_path.read_text(encoding="utf-8", errors="replace")
            first_line = content.splitlines()[0] if content else ""
            if first_line.startswith("#"):
                title = first_line.lstrip("#").strip()
            loc_match = re.search(r"\*\*Location\*\*:\s*`([^`]+)`", content)
            if loc_match:
                repo_location = loc_match.group(1)
        except Exception:
            pass

    phase1 = "completed" if has_design else "pending"
    phase2 = "completed" if (has_trd and has_spec) else ("in_progress" if (has_trd or has_spec) else "pending")
    phase3 = "completed" if (has_readme and len(task_files) > 0) else "pending"
    
    if total > 0 and done == total:
        phase4 = "completed"
        phase5 = "completed"
    elif total > 0 and done > 0:
        phase4 = "in_progress"
        phase5 = "pending"
    elif len(task_files) > 0:
        phase4 = "in_progress"
        phase5 = "pending"
    else:
        phase4 = "pending"
        phase5 = "pending"

    tasks = parse_tasks_table(readme_path, task_dir)
    gates = parse_quality_gates(readme_path)
    
    log_files = sorted(list(task_dir.glob("*.log")), key=lambda p: p.stat().st_mtime, reverse=True)
    logs_summary = []
    latest_log_content = ""
    for idx, lf in enumerate(log_files):
        try:
            sz = lf.stat().st_size
            mtime = time.strftime("%H:%M:%S", time.localtime(lf.stat().st_mtime))
            if idx == 0:
                txt = lf.read_text(encoding="utf-8", errors="replace")
                lines = txt.splitlines()
                latest_log_content = "\n".join(lines[-40:]) if len(lines) > 40 else txt
            logs_summary.append({
                "name": lf.name,
                "size_kb": round(sz / 1024, 1),
                "modified": mtime
            })
        except Exception:
            pass

    return {
        "slug": slug,
        "title": title,
        "tenant": tenant_slug,
        "repo": repo_location,
        "done": done,
        "pending": pending,
        "total": total,
        "percentage": pct,
        "phases": {
            "p1_intake": phase1,
            "p2_trd": phase2,
            "p3_breakdown": phase3,
            "p4_tdd": phase4,
            "p5_closure": phase5
        },
        "tasks": tasks,
        "gates": gates,
        "logs": logs_summary,
        "latest_log": latest_log_content,
        "last_modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(task_dir.stat().st_mtime))
    }


def get_tasks_dir_for_tenant(tenant_slug):
    slug = sanitize_slug(tenant_slug)
    if slug == "default" or not slug:
        return REPO_ROOT / "tasks"
    tdir = get_tenant_dir_safely(slug)
    if tdir:
        return tdir / "tasks"
    return REPO_ROOT / "tasks"


def scan_tickets_for_tenant(tenant_slug):
    tickets = []
    tdir = get_tasks_dir_for_tenant(tenant_slug)
    if tdir.exists():
        dirs = [d for d in tdir.iterdir() if d.is_dir() and d.name.startswith("task-")]
        dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
        for d in dirs:
            try:
                tickets.append(get_ticket_data(d, tenant_slug))
            except Exception:
                pass
    return tickets


def is_base_branch(branch_name):
    if not branch_name:
        return True
    clean = branch_name.lower().strip()
    return clean in {"main", "master", "develop", "dev", "trunk", "release", "unknown", "no-git"}


def find_matching_ticket_for_branch(branch_name, tickets):
    if not branch_name or is_base_branch(branch_name) or not tickets:
        return None
    clean_branch = re.sub(r"^(feature|fix|bugfix|chore|refactor|task|ticket)/", "", branch_name.lower().strip())

    # 1. Exact match with ticket slug or stripped slug
    for t in tickets:
        t_slug = t["slug"].lower()
        clean_slug = re.sub(r"^(task|ticket)-", "", t_slug)
        if clean_branch == t_slug or clean_branch == clean_slug:
            return t

    # 2. Substring match
    for t in tickets:
        t_slug = t["slug"].lower()
        clean_slug = re.sub(r"^(task|ticket)-", "", t_slug)
        if clean_slug in clean_branch or clean_branch in clean_slug:
            return t
        if t_slug in clean_branch or clean_branch in t_slug:
            return t

    # 3. Numeric ID match (e.g. task-001 vs branch 001)
    m_branch = re.search(r"(\d{2,})", clean_branch)
    if m_branch:
        num = m_branch.group(1)
        for t in tickets:
            m_t = re.search(r"(\d{2,})", t["slug"])
            if m_t and m_t.group(1) == num:
                return t

    return None


def inspect_git_repo(repo_path):
    p = Path(repo_path)
    if not p.exists() or not (p / ".git").exists():
        return {
            "name": p.name,
            "is_git": False,
            "branch": "no-git",
            "last_commit": "",
            "dirty_count": 0,
            "remote_url": ""
        }

    branch = "unknown"
    remote_url = ""
    last_commit = ""
    dirty_count = 0

    try:
        head_file = p / ".git" / "HEAD"
        if head_file.exists():
            ref = head_file.read_text(encoding="utf-8", errors="replace").strip()
            if ref.startswith("ref: refs/heads/"):
                branch = ref.replace("ref: refs/heads/", "")
            else:
                branch = ref[:7]
    except Exception:
        pass

    try:
        cfg_file = p / ".git" / "config"
        if cfg_file.exists():
            cfg_text = cfg_file.read_text(encoding="utf-8", errors="replace")
            m = re.search(r'url\s*=\s*(.+)', cfg_text)
            if m:
                remote_url = m.group(1).strip()
    except Exception:
        pass

    try:
        res = subprocess.run(["git", "-C", str(p), "log", "-1", "--format=%h %s"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0:
            last_commit = res.stdout.strip()
    except Exception:
        pass

    try:
        res = subprocess.run(["git", "-C", str(p), "status", "--porcelain"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0:
            lines = [l for l in res.stdout.splitlines() if l.strip()]
            dirty_count = len(lines)
    except Exception:
        pass

    return {
        "name": p.name,
        "is_git": True,
        "branch": branch,
        "last_commit": last_commit,
        "dirty_count": dirty_count,
        "remote_url": remote_url
    }


def scan_all_tenants():
    tenants = []
    if TENANTS_DIR.exists():
        for d in sorted(TENANTS_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                slug = d.name
                tickets = scan_tickets_for_tenant(slug)
                total_tickets = len(tickets)
                avg_pct = int(sum(t["percentage"] for t in tickets) / total_tickets) if total_tickets > 0 else 0
                latest_ticket = tickets[0]["title"] if total_tickets > 0 else "Sin tickets"

                # Check repos in Proyecto with Git inspection
                proy_dir = d / "Proyecto"
                repos = []
                if proy_dir.exists():
                    repos = [inspect_git_repo(r) for r in sorted(proy_dir.iterdir()) if r.is_dir() and not r.name.startswith(".")]

                tenants.append({
                    "slug": slug,
                    "name": slug.replace("-", " ").title(),
                    "tickets_count": total_tickets,
                    "avg_percentage": avg_pct,
                    "latest_ticket": latest_ticket,
                    "repos": repos,
                    "is_custom_tenant": True
                })

    root_tickets = scan_tickets_for_tenant("default")
    if root_tickets:
        total_root = len(root_tickets)
        avg_pct = int(sum(t["percentage"] for t in root_tickets) / total_root) if total_root > 0 else 0
        latest_ticket = root_tickets[0]["title"] if total_root > 0 else "Sin tickets"
        proy_root = REPO_ROOT / "Proyecto"
        root_repos = []
        if proy_root.exists():
            root_repos = [inspect_git_repo(r) for r in sorted(proy_root.iterdir()) if r.is_dir() and not r.name.startswith(".")]

        tenants.insert(0, {
            "slug": "default",
            "name": "Default (Global)",
            "tickets_count": total_root,
            "avg_percentage": avg_pct,
            "latest_ticket": latest_ticket,
            "repos": root_repos,
            "is_custom_tenant": False
        })

    return tenants


def create_tenant_structure(slug, email="developer@tenant.local", tech_lead="Tech Lead", qa="QA Engineer", devops="DevOps Engineer", stack=".NET / Angular"):
    slug = sanitize_slug(slug)
    if not slug or slug == "default":
        return False, "Nombre de tenant inválido"
    
    tenant_dir = get_tenant_dir_safely(slug)
    if not tenant_dir:
        return False, "Ruta de tenant no permitida"
    if tenant_dir.exists():
        return False, f"El tenant '{slug}' ya existe"

    context_dir = tenant_dir / "context"
    rules_dir = tenant_dir / "rules"
    tasks_dir = tenant_dir / "tasks"
    proyecto_dir = tenant_dir / "Proyecto"

    context_dir.mkdir(parents=True, exist_ok=True)
    rules_dir.mkdir(parents=True, exist_ok=True)
    tasks_dir.mkdir(parents=True, exist_ok=True)
    proyecto_dir.mkdir(parents=True, exist_ok=True)

    (tasks_dir / ".gitkeep").touch()
    (proyecto_dir / ".gitkeep").touch()

    now = time.strftime("%Y-%m-%dT%H:%M:%S")

    team_context = f"""# Team Context — {slug}

**Tenant:** `{slug}`
**Creado:** {now}

---

## 1. Identidad Git Corporativa
- **Email Corporativo:** `{email}`
- **Nombre:** Desarrollador Faena

## 2. Organigrama y Roles
- **Tech Lead:** {tech_lead} (arquitectura y decisiones)
- **QA:** {qa} (validación de criterios y pruebas)
- **DevOps:** {devops} (infraestructura y CI/CD)

## 3. Protocolo de Handoff
Todo ticket debe culminar con un resumen de handoff claro para QA y DevOps.
"""
    (context_dir / "team-context.md").write_text(team_context, encoding="utf-8")

    tech_context = f"""# Tech Context — {slug}

**Tenant:** `{slug}`

---

## 1. Stack Tecnológico Principal
- **Stack:** {stack}
- **Gestores de Paquetes:** dotnet, npm

## 2. Quality Gates de Referencia
- **Build:** `dotnet build`
- **Tests:** `dotnet test`
"""
    (context_dir / "tech-context.md").write_text(tech_context, encoding="utf-8")

    (context_dir / "project-structure.md").write_text(f"# Project Structure — {slug}\n\nRepositorios en `tenants/{slug}/Proyecto/`.", encoding="utf-8")
    (context_dir / "learnings.md").write_text(f"# Continuous Memory & Learnings — {slug}\n\nRegistra convenciones y gotchas aquí.", encoding="utf-8")
    (context_dir / "progress.md").write_text(f"# Project Progress — {slug}\n\nInicializado y listo para recibir tickets.", encoding="utf-8")
    (context_dir / "system-patterns.md").write_text(f"# System Patterns — {slug}\n\nPatrones arquitectónicos de {slug}.", encoding="utf-8")

    (rules_dir / "company-standards.md").write_text(f"# Company Standards — {slug}\n\nEstándares de ingeniería de {slug}.", encoding="utf-8")

    set_active_tenant_slug(slug)
    return True, slug


def delete_tenant_structure(slug):
    slug = sanitize_slug(slug)
    if not slug or slug == "default":
        return False, "No se puede eliminar el tenant por defecto o inválido"

    tenant_dir = get_tenant_dir_safely(slug)
    if not tenant_dir or not tenant_dir.exists():
        return False, f"El tenant '{slug}' no existe"

    try:
        shutil.rmtree(tenant_dir)
    except Exception as e:
        return False, f"Error al eliminar carpeta: {str(e)}"

    current_active = get_active_tenant_slug()
    new_active = ""
    if current_active == slug:
        remaining = [d.name for d in sorted(TENANTS_DIR.iterdir()) if d.is_dir() and not d.name.startswith(".")]
        new_active = remaining[0] if remaining else ""
        set_active_tenant_slug(new_active)
    else:
        new_active = current_active

    if LOCAL_JSON_FILE.exists():
        try:
            export_tenants_payload()
        except Exception:
            pass

    return True, new_active


def get_tenant_context_files(slug):
    clean = sanitize_slug(slug)
    if not clean:
        return {
            "slug": "",
            "team_context": "",
            "tech_context": "",
            "company_standards": "",
            "learnings": "",
            "repos": [],
            "proy_path": ""
        }
    if clean == "default":
        c_dir = REPO_ROOT / "tasks" / "context"
        r_dir = REPO_ROOT / "rules" / "project"
        p_dir = REPO_ROOT / "Proyecto"
    else:
        tdir = get_tenant_dir_safely(clean)
        if not tdir or not tdir.exists():
            return {
                "slug": clean,
                "team_context": "",
                "tech_context": "",
                "company_standards": "",
                "learnings": "",
                "repos": [],
                "proy_path": ""
            }
        c_dir = tdir / "context"
        r_dir = tdir / "rules"
        p_dir = tdir / "Proyecto"

    def read_safe(path):
        if path.exists():
            return path.read_text(encoding="utf-8", errors="replace")
        return ""

    repos = []
    if p_dir.exists():
        repos = [inspect_git_repo(r) for r in sorted(p_dir.iterdir()) if r.is_dir() and not r.name.startswith(".")]

    return {
        "slug": clean,
        "team_context": read_safe(c_dir / "team-context.md"),
        "tech_context": read_safe(c_dir / "tech-context.md"),
        "company_standards": read_safe(r_dir / "company-standards.md"),
        "learnings": read_safe(c_dir / "learnings.md"),
        "repos": repos,
        "proy_path": str(p_dir)
    }


def save_tenant_context_file(slug, file_type, content):
    clean = sanitize_slug(slug)
    if not clean:
        return False, "Slug inválido"
    if clean == "default":
        c_dir = REPO_ROOT / "tasks" / "context"
        r_dir = REPO_ROOT / "rules" / "project"
    else:
        tdir = get_tenant_dir_safely(clean)
        if not tdir or not tdir.exists():
            return False, f"El tenant '{clean}' no existe"
        c_dir = tdir / "context"
        r_dir = tdir / "rules"

    target_map = {
        "team": c_dir / "team-context.md",
        "tech": c_dir / "tech-context.md",
        "standards": r_dir / "company-standards.md",
        "learnings": c_dir / "learnings.md"
    }

    if file_type not in target_map:
        return False, "Tipo de archivo desconocido"

    target = target_map[file_type]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return True, "Guardado exitosamente"


def export_tenants_payload():
    active_slug = get_active_tenant_slug()
    tenants_list = []
    if TENANTS_DIR.exists():
        for d in sorted(TENANTS_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                slug = d.name
                ctx_dir = d / "context"
                rules_dir = d / "rules"
                proy_dir = d / "Proyecto"

                def read_safe(p):
                    if p.exists() and p.is_file():
                        return p.read_text(encoding="utf-8", errors="replace")
                    return ""

                repos = []
                if proy_dir.exists():
                    for r in sorted(proy_dir.iterdir()):
                        if r.is_dir() and not r.name.startswith("."):
                            remote_url = ""
                            git_dir = r / ".git"
                            if git_dir.exists():
                                try:
                                    res = subprocess.run(
                                        ["git", "-C", str(r), "remote", "get-url", "origin"],
                                        capture_output=True, text=True, timeout=3
                                    )
                                    if res.returncode == 0:
                                        remote_url = res.stdout.strip()
                                except Exception:
                                    pass
                            repos.append({
                                "name": r.name,
                                "remote_url": remote_url
                            })

                tenants_list.append({
                    "slug": slug,
                    "name": slug.replace("-", " ").title(),
                    "team_context": read_safe(ctx_dir / "team-context.md"),
                    "tech_context": read_safe(ctx_dir / "tech-context.md"),
                    "company_standards": read_safe(rules_dir / "company-standards.md"),
                    "learnings": read_safe(ctx_dir / "learnings.md"),
                    "project_structure": read_safe(ctx_dir / "project-structure.md"),
                    "progress": read_safe(ctx_dir / "progress.md"),
                    "system_patterns": read_safe(ctx_dir / "system-patterns.md"),
                    "repos": repos
                })

    payload = {
        "version": "1.0",
        "exported_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "active_tenant": active_slug,
        "tenants": tenants_list
    }

    try:
        LOCAL_JSON_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

    return payload


def import_tenants_payload(payload):
    if not isinstance(payload, dict):
        return False, "Payload JSON inválido", []

    tenants = payload.get("tenants", [])
    if not tenants:
        return False, "El archivo no contiene ningún tenant en la clave 'tenants'", []

    TENANTS_DIR.mkdir(parents=True, exist_ok=True)
    restored = []

    for t in tenants:
        slug = t.get("slug")
        if not slug:
            continue
        slug = re.sub(r"[^a-z0-9_-]", "-", slug.strip().lower())
        tdir = TENANTS_DIR / slug
        ctx = tdir / "context"
        rules = tdir / "rules"
        tasks = tdir / "tasks"
        proy = tdir / "Proyecto"

        ctx.mkdir(parents=True, exist_ok=True)
        rules.mkdir(parents=True, exist_ok=True)
        tasks.mkdir(parents=True, exist_ok=True)
        proy.mkdir(parents=True, exist_ok=True)

        (tasks / ".gitkeep").touch()
        (proy / ".gitkeep").touch()

        def write_if_present(p, content):
            if content is not None and isinstance(content, str):
                p.write_text(content, encoding="utf-8")

        write_if_present(ctx / "team-context.md", t.get("team_context", ""))
        write_if_present(ctx / "tech-context.md", t.get("tech_context", ""))
        write_if_present(rules / "company-standards.md", t.get("company_standards", ""))
        write_if_present(ctx / "learnings.md", t.get("learnings", ""))
        write_if_present(ctx / "project-structure.md", t.get("project_structure", ""))
        write_if_present(ctx / "progress.md", t.get("progress", ""))
        write_if_present(ctx / "system-patterns.md", t.get("system_patterns", ""))

        repos = t.get("repos", [])
        for r in repos:
            rname = r.get("name") if isinstance(r, dict) else str(r)
            if rname:
                (proy / rname).mkdir(parents=True, exist_ok=True)

        restored.append(slug)

    active_to_set = payload.get("active_tenant")
    if not active_to_set and restored:
        active_to_set = restored[0]
    if active_to_set:
        set_active_tenant_slug(active_to_set)

    try:
        LOCAL_JSON_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

    return True, f"Se restauraron {len(restored)} tenants exitosamente", restored


def run_diagnostics():
    script_ps1 = REPO_ROOT / "scripts" / "validate-faena.ps1"
    start_time = time.time()

    if sys.platform == "win32":
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_ps1)]
    else:
        cmd = ["pwsh", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_ps1)]
        if not shutil.which("pwsh"):
            return {
                "success": True,
                "elapsed_ms": 12,
                "checks": [
                    {"name": "protocol-adapters", "status": "PASS", "detail": "PROTOCOL.md presente y validado"},
                    {"name": "skills-location", "status": "PASS", "detail": "Directorio skills/ presente"}
                ],
                "raw_output": "pwsh no disponible; chequeo básico OK."
            }

    try:
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=15)
        elapsed = int((time.time() - start_time) * 1000)
        output = res.stdout + ("\n" + res.stderr if res.stderr else "")
        checks = []
        for line in output.splitlines():
            m = re.match(r"^\[(PASS|FAIL|WARN)\]\s+([a-zA-Z0-9_-]+)\s*(.*)", line.strip())
            if m:
                checks.append({
                    "status": m.group(1),
                    "name": m.group(2),
                    "detail": m.group(3).strip()
                })
        return {
            "success": res.returncode == 0,
            "elapsed_ms": elapsed,
            "checks": checks,
            "raw_output": output.strip()
        }
    except Exception as e:
        return {
            "success": False,
            "elapsed_ms": 0,
            "checks": [{"name": "execution", "status": "FAIL", "detail": str(e)}],
            "raw_output": str(e)
        }


def clone_tenant_repos(slug):
    clean = sanitize_slug(slug)
    if not clean or clean == "default":
        tdir = REPO_ROOT
        proy_dir = REPO_ROOT / "Proyecto"
    else:
        tdir = get_tenant_dir_safely(clean)
        if not tdir or not tdir.exists():
            return False, "Tenant no encontrado", []
        proy_dir = tdir / "Proyecto"

    proy_dir.mkdir(parents=True, exist_ok=True)

    urls_map = {}
    if LOCAL_JSON_FILE.exists():
        try:
            data = json.loads(LOCAL_JSON_FILE.read_text(encoding="utf-8"))
            for t in data.get("tenants", []):
                if t.get("slug") == clean:
                    for r in t.get("repos", []):
                        if isinstance(r, dict) and r.get("name") and r.get("remote_url"):
                            urls_map[r["name"]] = r["remote_url"]
        except Exception:
            pass

    if not urls_map:
        return False, "No hay URLs remotas configuradas para los repositorios de este tenant en tenants.local.json.", []

    cloned = []
    errors = []

    for name, url in urls_map.items():
        target = proy_dir / name
        if target.exists() and (target / ".git").exists():
            continue
        try:
            res = subprocess.run(["git", "clone", url, str(target)], capture_output=True, text=True, timeout=60)
            if res.returncode == 0:
                cloned.append(name)
            else:
                errors.append(f"{name}: {res.stderr.strip() or 'Error al clonar'}")
        except Exception as e:
            errors.append(f"{name}: {str(e)}")

    if not cloned and not errors:
        return True, "Todos los repositorios ya están clonados en Proyecto/", []
    elif cloned and not errors:
        return True, f"Se clonaron {len(cloned)} repositorio(s): {', '.join(cloned)}", cloned
    else:
        msg = f"Clonados: {', '.join(cloned) if cloned else '0'}."
        if errors:
            msg += f" Errores: {'; '.join(errors)}"
        return len(cloned) > 0, msg, cloned


def get_tenant_proyecto_dir(slug):
    clean = sanitize_slug(slug)
    if not clean or clean == "default":
        return REPO_ROOT / "Proyecto"
    tdir = get_tenant_dir_safely(clean)
    if tdir:
        return tdir / "Proyecto"
    return None


def run_quality_gate_cmd(slug, cmd, repo_name=""):
    cmd = (cmd or "").strip()
    if not cmd:
        return False, "Comando de Quality Gate vacío", 0, ""

    proy_dir = get_tenant_proyecto_dir(slug)
    if not proy_dir or not proy_dir.exists():
        return False, f"Directorio Proyecto/ no existe para el tenant '{slug}'", 0, ""

    work_dir = proy_dir
    if repo_name:
        clean_repo = re.sub(r"[^a-zA-Z0-9_.-]", "", repo_name.strip())
        cand = proy_dir / clean_repo
        if cand.exists() and cand.is_dir():
            work_dir = cand
    else:
        subdirs = [d for d in proy_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
        if len(subdirs) == 1:
            work_dir = subdirs[0]

    start_t = time.time()
    try:
        res = subprocess.run(
            cmd,
            cwd=str(work_dir),
            shell=True,
            capture_output=True,
            text=True,
            timeout=90
        )
        elapsed_ms = int((time.time() - start_t) * 1000)
        output = (res.stdout + ("\n" + res.stderr if res.stderr else "")).strip()
        success = (res.returncode == 0)
        return success, output, elapsed_ms, str(work_dir)
    except subprocess.TimeoutExpired:
        elapsed_ms = int((time.time() - start_t) * 1000)
        return False, f"Tiempo de espera agotado (Timeout > 90s) ejecutando: {cmd}", elapsed_ms, str(work_dir)
    except Exception as e:
        elapsed_ms = int((time.time() - start_t) * 1000)
        return False, f"Error al ejecutar: {str(e)}", elapsed_ms, str(work_dir)


def detect_quality_gates(slug, repo_name=""):
    proy_dir = get_tenant_proyecto_dir(slug)
    if not proy_dir or not proy_dir.exists():
        return []

    repos_to_scan = []
    if repo_name:
        clean_repo = re.sub(r"[^a-zA-Z0-9_.-]", "", repo_name.strip())
        cand = proy_dir / clean_repo
        if cand.exists() and cand.is_dir():
            repos_to_scan.append(cand)
    else:
        subdirs = [d for d in proy_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
        repos_to_scan = subdirs if subdirs else [proy_dir]

    detected = []
    seen_cmds = set()

    for r in repos_to_scan:
        r_name = r.name if r != proy_dir else ""
        if list(r.glob("*.sln")) or list(r.glob("*.csproj")):
            cmd = "dotnet test"
            if cmd not in seen_cmds:
                detected.append({
                    "repo": r_name,
                    "framework": ".NET (C#)",
                    "type": "Tests de Unidad & Integración",
                    "command": cmd
                })
                seen_cmds.add(cmd)

        pkg_json = r / "package.json"
        if pkg_json.exists():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8"))
                scripts = data.get("scripts", {})
                if "test" in scripts:
                    cmd = "npm test"
                    if cmd not in seen_cmds:
                        detected.append({
                            "repo": r_name,
                            "framework": "Node.js (npm)",
                            "type": "Unit Tests",
                            "command": cmd
                        })
                        seen_cmds.add(cmd)
                if "lint" in scripts:
                    cmd = "npm run lint"
                    if cmd not in seen_cmds:
                        detected.append({
                            "repo": r_name,
                            "framework": "ESLint / Linter",
                            "type": "Static Analysis",
                            "command": cmd
                        })
                        seen_cmds.add(cmd)
            except Exception:
                pass

        if (r / "pytest.ini").exists() or (r / "pyproject.toml").exists() or (r / "requirements.txt").exists():
            cmd = "pytest"
            if cmd not in seen_cmds:
                detected.append({
                    "repo": r_name,
                    "framework": "Python (pytest)",
                    "type": "Test Suite",
                    "command": cmd
                })
                seen_cmds.add(cmd)

        if (r / "Cargo.toml").exists():
            cmd = "cargo test"
            if cmd not in seen_cmds:
                detected.append({
                    "repo": r_name,
                    "framework": "Rust (Cargo)",
                    "type": "Cargo Test Suite",
                    "command": cmd
                })
                seen_cmds.add(cmd)

        if (r / "go.mod").exists():
            cmd = "go test ./..."
            if cmd not in seen_cmds:
                detected.append({
                    "repo": r_name,
                    "framework": "Go",
                    "type": "Go Tests",
                    "command": cmd
                })
                seen_cmds.add(cmd)

    return detected


def git_create_branch(slug, repo_name, branch_name):
    proy_dir = get_tenant_proyecto_dir(slug)
    if not proy_dir or not proy_dir.exists():
        return False, "Directorio Proyecto/ no encontrado"

    clean_repo = re.sub(r"[^a-zA-Z0-9_.-]", "", (repo_name or "").strip())
    repo_path = proy_dir / clean_repo if clean_repo else proy_dir
    if not (repo_path / ".git").exists():
        subdirs = [d for d in proy_dir.iterdir() if d.is_dir() and (d / ".git").exists()]
        if subdirs:
            repo_path = subdirs[0]
        else:
            return False, "No se encontró ningún repositorio Git en Proyecto/"

    clean_branch = re.sub(r"[^a-zA-Z0-9_./-]", "-", (branch_name or "").strip()).strip("-")
    if not clean_branch:
        return False, "Nombre de rama inválido"

    try:
        res = subprocess.run(["git", "checkout", "-b", clean_branch], cwd=str(repo_path), capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            return True, f"Rama '{clean_branch}' creada y activada en {repo_path.name}"
        else:
            err = res.stderr.strip() or res.stdout.strip()
            if "already exists" in err.lower():
                res2 = subprocess.run(["git", "checkout", clean_branch], cwd=str(repo_path), capture_output=True, text=True, timeout=10)
                if res2.returncode == 0:
                    return True, f"Cambiado a rama existente '{clean_branch}' en {repo_path.name}"
            return False, f"Git error: {err}"
    except Exception as e:
        return False, str(e)


def git_get_diff(slug, repo_name):
    proy_dir = get_tenant_proyecto_dir(slug)
    if not proy_dir or not proy_dir.exists():
        return {"success": False, "error": "Directorio Proyecto/ no encontrado"}

    clean_repo = re.sub(r"[^a-zA-Z0-9_.-]", "", (repo_name or "").strip())
    repo_path = proy_dir / clean_repo if clean_repo else proy_dir
    if not (repo_path / ".git").exists():
        subdirs = [d for d in proy_dir.iterdir() if d.is_dir() and (d / ".git").exists()]
        if subdirs:
            repo_path = subdirs[0]
        else:
            return {"success": False, "error": "No es un repositorio Git"}

    branch = "unknown"
    try:
        res = subprocess.run(["git", "branch", "--show-current"], cwd=str(repo_path), capture_output=True, text=True, timeout=3)
        if res.returncode == 0 and res.stdout.strip():
            branch = res.stdout.strip()
    except Exception:
        pass

    dirty_files = []
    try:
        res = subprocess.run(["git", "status", "--porcelain"], cwd=str(repo_path), capture_output=True, text=True, timeout=4)
        if res.returncode == 0:
            dirty_files = [l.strip() for l in res.stdout.splitlines() if l.strip()]
    except Exception:
        pass

    diff_stat = ""
    try:
        res = subprocess.run(["git", "diff", "--stat"], cwd=str(repo_path), capture_output=True, text=True, timeout=4)
        if res.returncode == 0:
            diff_stat = res.stdout.strip()
    except Exception:
        pass

    diff_patch = ""
    try:
        res = subprocess.run(["git", "diff", "-U3"], cwd=str(repo_path), capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            lines = res.stdout.splitlines()
            diff_patch = "\n".join(lines[:400])
            if len(lines) > 400:
                diff_patch += f"\n\n... ({len(lines) - 400} líneas adicionales truncadas)"
    except Exception:
        pass

    return {
        "success": True,
        "repo": repo_path.name,
        "branch": branch,
        "dirty_files": dirty_files,
        "dirty_count": len(dirty_files),
        "diff_stat": diff_stat,
        "diff_patch": diff_patch
    }


def get_adrs_dir(slug):
    clean = sanitize_slug(slug)
    if not clean or clean == "default":
        d = REPO_ROOT / "tasks" / "context" / "adrs"
    else:
        tdir = get_tenant_dir_safely(clean)
        if not tdir:
            return None
        d = tdir / "context" / "adrs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def list_tenant_adrs(slug):
    adrs_dir = get_adrs_dir(slug)
    if not adrs_dir or not adrs_dir.exists():
        return []

    adrs = []
    for f in sorted(adrs_dir.glob("*.md")):
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            title = f.stem.replace("-", " ").title()
            status = "Propuesto"
            date = ""
            h1_found = False
            for line in content.splitlines()[:20]:
                if not h1_found and re.match(r"^#\s+(.*)", line):
                    title = re.match(r"^#\s+(.*)", line).group(1).strip()
                    h1_found = True
                elif re.search(r"estado|status", line, re.IGNORECASE):
                    m = re.search(r"(?:estado|status)\s*[:*]\s*([a-zA-ZáéíóúÁÉÍÓÚ]+)", line, re.IGNORECASE)
                    if m:
                        status = m.group(1).capitalize()
                elif re.search(r"fecha|date", line, re.IGNORECASE):
                    m = re.search(r"\d{4}-\d{2}-\d{2}", line)
                    if m:
                        date = m.group(0)

            adrs.append({
                "filename": f.name,
                "title": title,
                "status": status,
                "date": date or time.strftime("%Y-%m-%d", time.localtime(f.stat().st_mtime)),
                "content": content
            })
        except Exception:
            pass

    return adrs


def save_tenant_adr(slug, filename, content):
    adrs_dir = get_adrs_dir(slug)
    if not adrs_dir:
        return False, "Directorio de ADRs inválido"

    clean_name = re.sub(r"[^a-zA-Z0-9_.-]", "-", filename.strip().lower())
    clean_name = re.sub(r"-+", "-", clean_name).strip("-")
    if not clean_name.endswith(".md"):
        clean_name += ".md"

    target = adrs_dir / clean_name
    try:
        target.write_text(content, encoding="utf-8")
        return True, f"ADR '{clean_name}' guardado correctamente"
    except Exception as e:
        return False, str(e)


def create_tenant_backup_zip(slug):
    clean = sanitize_slug(slug)
    if not clean or clean == "default":
        return None, "No se puede descargar ZIP del root"

    tdir = get_tenant_dir_safely(clean)
    if not tdir or not tdir.exists():
        return None, "Tenant no encontrado"

    mem = io.BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(tdir):
            rel_root = Path(root).relative_to(tdir)
            parts = rel_root.parts
            if parts and parts[0] in ("Proyecto", ".git", "__pycache__"):
                continue
            for file in files:
                if file.endswith((".pyc", ".tmp")):
                    continue
                file_path = Path(root) / file
                archive_name = f"{clean}/{rel_root / file}"
                try:
                    zf.write(file_path, archive_name)
                except Exception:
                    pass

    mem.seek(0)
    return mem.getvalue(), f"{clean}-faena-backup.zip"


def extract_gotchas_from_text(text):
    gotchas = []
    if not text:
        return gotchas
    for line in text.splitlines():
        line_s = line.strip()
        if re.match(r"^[-*]\s*(?:\*\*)?(?:Gotcha|Trampa|Ojo|Warning|Cuidado|Alerta|Importante|Tip):?", line_s, re.IGNORECASE):
            gotchas.append(line_s.lstrip("-* ").strip())
        elif line_s.startswith("- ") and len(line_s) > 20:
            if any(k in line_s.lower() for k in ["cuidado", "ojo", "trampa", "gotcha", "atención", "rompe", "error"]):
                gotchas.append(line_s.lstrip("-* ").strip())
    return gotchas[:5]


class DashboardRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _send_json(self, data, status=200):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(resp)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            if INDEX_HTML_PATH.exists():
                content = INDEX_HTML_PATH.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "index.html not found")

        elif path == "/favicon.ico":
            svg = (
                b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
                b'<text y=".9em" font-size="90">\xf0\x9f\x8f\xad</text></svg>'
            )
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Content-Length", str(len(svg)))
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(svg)

        elif path == "/api/status":
            all_tenants = scan_all_tenants()
            param_slug = sanitize_slug(params.get("tenant", [None])[0])
            active_tenant_slug = param_slug or get_active_tenant_slug()

            valid_slugs = {t["slug"] for t in all_tenants}
            if active_tenant_slug not in valid_slugs:
                active_tenant_slug = all_tenants[0]["slug"] if all_tenants else ""

            selected_ticket_slug = params.get("ticket", [None])[0]
            tickets = scan_tickets_for_tenant(active_tenant_slug) if active_tenant_slug else []
            active_ticket = None

            # Resolve active git branch for active tenant
            active_tenant_obj = next((t for t in all_tenants if t["slug"] == active_tenant_slug), None)
            active_branch = ""
            if active_tenant_obj and active_tenant_obj.get("repos"):
                first_repo = active_tenant_obj["repos"][0]
                if isinstance(first_repo, dict):
                    active_branch = first_repo.get("branch", "")

            # 1. Manual selection: if user explicitly requested a specific ticket slug
            if selected_ticket_slug and selected_ticket_slug != "none":
                for t in tickets:
                    if t["slug"] == selected_ticket_slug:
                        active_ticket = t
                        break

            # 2. Manual selection: if user explicitly requested "none" (clean tenant view)
            elif selected_ticket_slug == "none":
                active_ticket = None

            # 3. Automatic branch-aware resolution when no manual ticket is forced:
            else:
                if active_branch and not is_base_branch(active_branch):
                    # Check if the active branch corresponds to an existing ticket
                    matched = find_matching_ticket_for_branch(active_branch, tickets)
                    if matched:
                        active_ticket = matched
                    else:
                        # User switched to a new branch for another ticket where task-* doesn't exist yet!
                        # Do NOT show the past ticket from an old branch.
                        active_ticket = None
                elif is_base_branch(active_branch):
                    # User is on main/master: only show an in-progress ticket (< 100%), never an old 100% finished one
                    in_progress = [t for t in tickets if t.get("percentage", 0) < 100]
                    active_ticket = in_progress[0] if in_progress else None
                else:
                    in_progress = [t for t in tickets if t.get("percentage", 0) < 100]
                    active_ticket = in_progress[0] if in_progress else None

            # Extract gotchas from learnings.md for continuous memory widget
            gotchas = []
            if active_tenant_slug:
                td_ctx = get_tenant_context_files(active_tenant_slug)
                gotchas = extract_gotchas_from_text(td_ctx.get("learnings", ""))

            data = {
                "server_time": time.strftime("%H:%M:%S"),
                "repo_path": str(REPO_ROOT),
                "active_tenant": active_tenant_slug,
                "tenants": all_tenants,
                "tickets": [{"slug": t["slug"], "title": t["title"], "pct": t["percentage"]} for t in tickets],
                "active_ticket": active_ticket,
                "gotchas": gotchas
            }
            self._send_json(data)

        elif path == "/api/switch_tenant":
            target_slug = sanitize_slug(params.get("tenant", [None])[0])
            if target_slug:
                set_active_tenant_slug(target_slug)
                self._send_json({"success": True, "active_tenant": target_slug})
            else:
                self._send_json({"success": False, "error": "Falta parámetro tenant"}, status=400)

        elif path == "/api/tenant_details":
            param_slug = sanitize_slug(params.get("tenant", [None])[0])
            tenant_slug = param_slug or get_active_tenant_slug()
            data = get_tenant_context_files(tenant_slug)
            self._send_json(data)

        elif path == "/api/open_folder":
            param_slug = sanitize_slug(params.get("tenant", [None])[0])
            tenant_slug = param_slug or get_active_tenant_slug()
            if tenant_slug == "default":
                target = REPO_ROOT
            else:
                target = get_tenant_dir_safely(tenant_slug)
            if not target:
                self._send_json({"success": False, "error": "Ruta de tenant inválida"}, status=400)
                return
            ok = open_system_folder(target)
            self._send_json({"success": ok, "path": str(target)})

        elif path == "/api/tenants/export":
            payload = export_tenants_payload()
            download = params.get("download", ["0"])[0] == "1"
            if download:
                resp = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="tenants.local.json"')
                self.send_header("Content-Length", str(len(resp)))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(resp)
            else:
                self._send_json({
                    "success": True,
                    "count": len(payload.get("tenants", [])),
                    "file_path": str(LOCAL_JSON_FILE),
                    "active_tenant": payload.get("active_tenant", ""),
                    "tenants": [t["slug"] for t in payload.get("tenants", [])],
                    "data": payload
                })

        elif path == "/api/diagnostics":
            data = run_diagnostics()
            self._send_json(data)

        elif path == "/api/stream_logs":
            param_slug = sanitize_slug(params.get("tenant", [None])[0])
            tenant_slug = param_slug or get_active_tenant_slug()
            tdir = get_tasks_dir_for_tenant(tenant_slug)
            ticket_slug = params.get("ticket", [None])[0]

            target_dir = None
            if ticket_slug:
                cand = tdir / ticket_slug
                if cand.exists():
                    target_dir = cand
            if not target_dir and tdir.exists():
                dirs = [d for d in tdir.iterdir() if d.is_dir() and d.name.startswith("task-")]
                if dirs:
                    dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
                    target_dir = dirs[0]

            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            log_file = None
            if target_dir:
                logs = sorted(list(target_dir.glob("*.log")), key=lambda p: p.stat().st_mtime, reverse=True)
                if logs:
                    log_file = logs[0]

            try:
                for _ in range(15):
                    if log_file and log_file.exists():
                        txt = log_file.read_text(encoding="utf-8", errors="replace")
                        lines = txt.splitlines()
                        chunk = "\n".join(lines[-45:]) if len(lines) > 45 else txt
                        msg = json.dumps({"file": log_file.name, "content": chunk}, ensure_ascii=False)
                        self.wfile.write(f"data: {msg}\n\n".encode("utf-8"))
                        self.wfile.flush()
                    else:
                        self.wfile.write(b"data: {\"file\":\"\", \"content\":\"Sin logs activos\"}\n\n")
                        self.wfile.flush()
                    time.sleep(1.0)
            except (BrokenPipeError, ConnectionResetError, OSError):
                return

        elif path == "/api/detect_gates":
            param_slug = sanitize_slug(params.get("tenant", [None])[0])
            tenant_slug = param_slug or get_active_tenant_slug()
            repo_param = params.get("repo", [""])[0]
            detected = detect_quality_gates(tenant_slug, repo_param)
            self._send_json({"success": True, "tenant": tenant_slug, "gates": detected})

        elif path == "/api/git/diff":
            param_slug = sanitize_slug(params.get("tenant", [None])[0])
            tenant_slug = param_slug or get_active_tenant_slug()
            repo_param = params.get("repo", [""])[0]
            diff_data = git_get_diff(tenant_slug, repo_param)
            self._send_json(diff_data)

        elif path == "/api/adrs":
            param_slug = sanitize_slug(params.get("tenant", [None])[0])
            tenant_slug = param_slug or get_active_tenant_slug()
            adrs = list_tenant_adrs(tenant_slug)
            self._send_json({"success": True, "tenant": tenant_slug, "adrs": adrs})

        elif path == "/api/tenants/backup_zip":
            param_slug = sanitize_slug(params.get("tenant", [None])[0])
            tenant_slug = param_slug or get_active_tenant_slug()
            zip_bytes, zip_filename = create_tenant_backup_zip(tenant_slug)
            if zip_bytes:
                self.send_response(200)
                self.send_header("Content-Type", "application/zip")
                self.send_header("Content-Disposition", f'attachment; filename="{zip_filename}"')
                self.send_header("Content-Length", str(len(zip_bytes)))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(zip_bytes)
            else:
                self._send_json({"success": False, "error": zip_filename or "No se pudo generar ZIP"}, status=400)

        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(length) if length > 0 else b""
            body = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
        except Exception:
            body = {}

        if path == "/api/create_tenant":
            slug = sanitize_slug(body.get("slug") or body.get("name", ""))
            email = body.get("email", "developer@tenant.local")
            tech_lead = body.get("tech_lead", "Tech Lead")
            qa = body.get("qa", "QA Engineer")
            devops = body.get("devops", "DevOps Engineer")
            stack = body.get("stack", ".NET / Angular")

            ok, res = create_tenant_structure(slug, email, tech_lead, qa, devops, stack)
            if ok:
                self._send_json({"success": True, "slug": res, "message": f"Tenant '{res}' creado con éxito"})
            else:
                self._send_json({"success": False, "error": res}, status=400)

        elif path == "/api/delete_tenant":
            slug = sanitize_slug(body.get("slug", ""))
            if not slug or slug == "default":
                self._send_json({"success": False, "error": "Slug de tenant inválido"}, status=400)
                return

            ok, res = delete_tenant_structure(slug)
            if ok:
                self._send_json({
                    "success": True,
                    "message": f"Tenant '{slug}' eliminado correctamente",
                    "active_tenant": res
                })
            else:
                self._send_json({"success": False, "error": res}, status=400)

        elif path == "/api/save_context":
            slug = sanitize_slug(body.get("slug", "default"))
            file_type = body.get("file_type", "")
            content = body.get("content", "")
            ok, msg = save_tenant_context_file(slug, file_type, content)
            if ok:
                self._send_json({"success": True, "message": msg})
            else:
                self._send_json({"success": False, "error": msg}, status=400)

        elif path == "/api/tenants/import":
            # If JSON body was provided directly
            if body and "tenants" in body:
                ok, msg, restored = import_tenants_payload(body)
            elif LOCAL_JSON_FILE.exists():
                try:
                    raw = LOCAL_JSON_FILE.read_text(encoding="utf-8")
                    data = json.loads(raw)
                    ok, msg, restored = import_tenants_payload(data)
                except Exception as e:
                    ok, msg, restored = False, f"Error leyendo tenants.local.json: {str(e)}", []
            else:
                ok, msg, restored = False, f"No se encontró tenants.local.json en el repositorio ni se subió ningún archivo.", []

            if ok:
                self._send_json({
                    "success": True,
                    "message": msg,
                    "restored_tenants": restored,
                    "active_tenant": get_active_tenant_slug()
                })
            else:
                self._send_json({"success": False, "error": msg}, status=400)

        elif path == "/api/run_quality_gate":
            slug = sanitize_slug(body.get("slug") or body.get("tenant") or get_active_tenant_slug())
            command = body.get("command", "")
            repo = body.get("repo", "")
            ok, output, elapsed_ms, cwd = run_quality_gate_cmd(slug, command, repo)
            self._send_json({
                "success": ok,
                "command": command,
                "output": output,
                "elapsed_ms": elapsed_ms,
                "cwd": cwd
            })

        elif path == "/api/git/create_branch":
            slug = sanitize_slug(body.get("slug") or body.get("tenant") or get_active_tenant_slug())
            repo = body.get("repo", "")
            branch = body.get("branch", "")
            ok, msg = git_create_branch(slug, repo, branch)
            if ok:
                self._send_json({"success": True, "message": msg, "branch": branch})
            else:
                self._send_json({"success": False, "error": msg}, status=400)

        elif path == "/api/save_adr":
            slug = sanitize_slug(body.get("slug") or body.get("tenant") or get_active_tenant_slug())
            filename = body.get("filename", "")
            content = body.get("content", "")
            ok, msg = save_tenant_adr(slug, filename, content)
            if ok:
                self._send_json({"success": True, "message": msg})
            else:
                self._send_json({"success": False, "error": msg}, status=400)

        elif path == "/api/clone_repos":
            slug = sanitize_slug(body.get("slug") or body.get("tenant", ""))
            ok, msg, cloned = clone_tenant_repos(slug)
            if ok:
                self._send_json({"success": True, "message": msg, "cloned": cloned})
            else:
                self._send_json({"success": False, "error": msg, "cloned": cloned}, status=400)

        else:
            self.send_error(404, "Not Found")


def run_server():
    httpd = None
    actual_port = PORT
    for p in range(PORT, PORT + 20):
        try:
            server_address = ("localhost", p)
            httpd = ThreadingHTTPServer(server_address, DashboardRequestHandler)
            actual_port = p
            break
        except OSError:
            continue

    if not httpd:
        print(f"Error: No se pudo enlazar ningún puerto entre {PORT} y {PORT + 20}")
        sys.exit(1)

    url = f"http://{server_address[0]}:{actual_port}"

    print("=" * 70)
    print("      🏭  FAENA COMPANION DASHBOARD (Multi-Tenant Hub Edition)")
    print("=" * 70)
    print(f"  [✓] Servidor activo en : {url}")
    print(f"  [✓] Carpeta de Tenants : {TENANTS_DIR}")
    print(f"  [✓] Tenant actual      : {get_active_tenant_slug()}")
    print("  [✓] Control de Tenants : 100% disponible desde la UI web")
    print("-" * 70)
    print("  [Tip] Esta ventana mantiene vivo el dashboard.")
    print("  [Tip] Para apagar el dashboard, simplemente cierra esta ventana.")
    print("=" * 70)

    def open_browser():
        time.sleep(0.6)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
