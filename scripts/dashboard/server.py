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
import webbrowser
import threading
import subprocess
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 3333
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TENANTS_DIR = REPO_ROOT / "tenants"
ACTIVE_TENANT_FILE = REPO_ROOT / ".active-tenant"
DASHBOARD_DIR = REPO_ROOT / "scripts" / "dashboard"
INDEX_HTML_PATH = DASHBOARD_DIR / "index.html"


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
    try:
        ACTIVE_TENANT_FILE.write_text(slug.strip(), encoding="utf-8")
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
    if tenant_slug == "default" or not tenant_slug:
        return REPO_ROOT / "tasks"
    return TENANTS_DIR / tenant_slug / "tasks"


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

                # Check repos in Proyecto
                proy_dir = d / "Proyecto"
                repos = []
                if proy_dir.exists():
                    repos = [r.name for r in proy_dir.iterdir() if r.is_dir() and not r.name.startswith(".")]

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
            root_repos = [r.name for r in proy_root.iterdir() if r.is_dir() and not r.name.startswith(".")]

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
    slug = re.sub(r"[^a-z0-9_-]", "-", slug.strip().lower())
    if not slug:
        return False, "Nombre de tenant inválido"
    
    tenant_dir = TENANTS_DIR / slug
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


def get_tenant_context_files(slug):
    if not slug:
        return {
            "slug": "",
            "team_context": "",
            "tech_context": "",
            "company_standards": "",
            "learnings": "",
            "repos": [],
            "proy_path": ""
        }
    if slug == "default":
        c_dir = REPO_ROOT / "tasks" / "context"
        r_dir = REPO_ROOT / "rules" / "project"
        p_dir = REPO_ROOT / "Proyecto"
    else:
        c_dir = TENANTS_DIR / slug / "context"
        r_dir = TENANTS_DIR / slug / "rules"
        p_dir = TENANTS_DIR / slug / "Proyecto"

    def read_safe(path):
        if path.exists():
            return path.read_text(encoding="utf-8", errors="replace")
        return ""

    repos = []
    if p_dir.exists():
        repos = [r.name for r in p_dir.iterdir() if r.is_dir() and not r.name.startswith(".")]

    return {
        "slug": slug,
        "team_context": read_safe(c_dir / "team-context.md"),
        "tech_context": read_safe(c_dir / "tech-context.md"),
        "company_standards": read_safe(r_dir / "company-standards.md"),
        "learnings": read_safe(c_dir / "learnings.md"),
        "repos": repos,
        "proy_path": str(p_dir)
    }


def save_tenant_context_file(slug, file_type, content):
    if slug == "default":
        c_dir = REPO_ROOT / "tasks" / "context"
        r_dir = REPO_ROOT / "rules" / "project"
    else:
        c_dir = TENANTS_DIR / slug / "context"
        r_dir = TENANTS_DIR / slug / "rules"

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


class DashboardRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _send_json(self, data, status=200):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(resp)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
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

        elif path == "/api/status":
            all_tenants = scan_all_tenants()
            active_tenant_slug = params.get("tenant", [None])[0] or get_active_tenant_slug()

            valid_slugs = {t["slug"] for t in all_tenants}
            if active_tenant_slug not in valid_slugs:
                active_tenant_slug = all_tenants[0]["slug"] if all_tenants else ""

            selected_ticket_slug = params.get("ticket", [None])[0]
            tickets = scan_tickets_for_tenant(active_tenant_slug) if active_tenant_slug else []
            active_ticket = None

            if selected_ticket_slug:
                for t in tickets:
                    if t["slug"] == selected_ticket_slug:
                        active_ticket = t
                        break
            
            if not active_ticket and tickets:
                active_ticket = tickets[0]

            data = {
                "server_time": time.strftime("%H:%M:%S"),
                "repo_path": str(REPO_ROOT),
                "active_tenant": active_tenant_slug,
                "tenants": all_tenants,
                "tickets": [{"slug": t["slug"], "title": t["title"], "pct": t["percentage"]} for t in tickets],
                "active_ticket": active_ticket
            }
            self._send_json(data)

        elif path == "/api/switch_tenant":
            target_slug = params.get("tenant", [None])[0]
            if target_slug:
                set_active_tenant_slug(target_slug)
                self._send_json({"success": True, "active_tenant": target_slug})
            else:
                self._send_json({"success": False, "error": "Falta parámetro tenant"}, status=400)

        elif path == "/api/tenant_details":
            tenant_slug = params.get("tenant", [None])[0] or get_active_tenant_slug()
            data = get_tenant_context_files(tenant_slug)
            self._send_json(data)

        elif path == "/api/open_folder":
            tenant_slug = params.get("tenant", [None])[0] or get_active_tenant_slug()
            if tenant_slug == "default":
                target = REPO_ROOT
            else:
                target = TENANTS_DIR / tenant_slug
            ok = open_system_folder(target)
            self._send_json({"success": ok, "path": str(target)})

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
            slug = body.get("slug") or body.get("name", "")
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

        elif path == "/api/save_context":
            slug = body.get("slug", "default")
            file_type = body.get("file_type", "")
            content = body.get("content", "")
            ok, msg = save_tenant_context_file(slug, file_type, content)
            if ok:
                self._send_json({"success": True, "message": msg})
            else:
                self._send_json({"success": False, "error": msg}, status=400)

        else:
            self.send_error(404, "Not Found")


def run_server():
    server_address = ("localhost", PORT)
    try:
        httpd = ThreadingHTTPServer(server_address, DashboardRequestHandler)
    except OSError:
        alt_port = PORT + 1
        server_address = ("localhost", alt_port)
        httpd = ThreadingHTTPServer(server_address, DashboardRequestHandler)

    url = f"http://{server_address[0]}:{server_address[1]}"

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
