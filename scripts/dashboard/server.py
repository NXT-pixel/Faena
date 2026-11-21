#!/usr/bin/env python3
"""
Faena Live Companion Dashboard Server
Global, host-agnostic companion dashboard for monitoring Faena implementation progress.
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
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 3333
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TASKS_DIR = REPO_ROOT / "tasks"
DASHBOARD_DIR = REPO_ROOT / "scripts" / "dashboard"
INDEX_HTML_PATH = DASHBOARD_DIR / "index.html"


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
    except Exception as e:
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


def get_ticket_data(task_dir):
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
    repo_location = "Proyecto/"
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
            snippet = ""
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


def scan_all_tickets():
    tickets = []
    if TASKS_DIR.exists():
        dirs = [d for d in TASKS_DIR.iterdir() if d.is_dir() and d.name.startswith("task-")]
        dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
        for d in dirs:
            try:
                tickets.append(get_ticket_data(d))
            except Exception:
                pass
    return tickets


class DashboardRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Mute normal stdout logging to keep console clean
        return

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
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
            params = parse_qs(parsed.query)
            selected_slug = params.get("ticket", [None])[0]

            tickets = scan_all_tickets()
            active_ticket = None

            if selected_slug:
                for t in tickets:
                    if t["slug"] == selected_slug:
                        active_ticket = t
                        break
            
            if not active_ticket and tickets:
                active_ticket = tickets[0]

            data = {
                "server_time": time.strftime("%H:%M:%S"),
                "repo_path": str(REPO_ROOT),
                "tickets": [{"slug": t["slug"], "title": t["title"], "pct": t["percentage"]} for t in tickets],
                "active_ticket": active_ticket
            }

            resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(resp)

        else:
            self.send_error(404, "Not Found")


def run_server():
    server_address = ("localhost", PORT)
    try:
        httpd = ThreadingHTTPServer(server_address, DashboardRequestHandler)
    except OSError:
        # Fallback to alternate port if 3333 is in use
        alt_port = PORT + 1
        server_address = ("localhost", alt_port)
        httpd = ThreadingHTTPServer(server_address, DashboardRequestHandler)

    url = f"http://{server_address[0]}:{server_address[1]}"

    print("=" * 68)
    print("      🏭  FAENA LIVE COMPANION DASHBOARD (Modo Global)")
    print("=" * 68)
    print(f"  [✓] Servidor activo en : {url}")
    print(f"  [✓] Monitoreando       : {TASKS_DIR}")
    print("  [✓] Compatible con     : Claude Code, OpenAI Codex, Antigravity, Cursor")
    print("-" * 68)
    print("  [Tip] Esta ventana mantiene vivo el dashboard.")
    print("  [Tip] Para apagar el dashboard, simplemente cierra esta ventana.")
    print("=" * 68)

    # Open browser automatically in background
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
