#!/usr/bin/env python3
"""Unit tests for Faena Dashboard server security, path safety, and ticket logic."""

import json
import os
import stat
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
import server  # noqa: E402


class TestDashboardSecurityAndLogic(unittest.TestCase):
    def test_sanitize_and_resolve_inside_blocks_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "base"
            base.mkdir()
            self.assertIsNone(server.resolve_inside(base, "../escape"))
            self.assertIsNone(server.resolve_inside(base, "..\\escape"))
            self.assertIsNone(server.resolve_inside(base, ".."))
            self.assertIsNone(server.resolve_inside(base, "."))
            ok = server.resolve_inside(base, "my-repo.git")
            self.assertIsNotNone(ok)
            self.assertEqual(ok.parent, base.resolve())

    def test_is_safe_git_url(self):
        self.assertTrue(server.is_safe_git_url("https://github.com/org/repo.git"))
        self.assertTrue(server.is_safe_git_url("git@github.com:org/repo.git"))
        self.assertFalse(server.is_safe_git_url("--upload-pack=calc.exe"))
        self.assertFalse(server.is_safe_git_url("ext::sh -c calc"))
        self.assertFalse(server.is_safe_git_url(""))

    def test_checkbox_counts_scoped_to_progress_tracking(self):
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(
                "# Ticket\n\n## Notes\n- [ ] unrelated example\n\n## Progress Tracking\n- [x] Task 01\n- [ ] Task 02\n",
                encoding="utf-8",
            )
            done, pending = server.get_checkbox_counts(readme)
            self.assertEqual((done, pending), (1, 1))

    def test_branch_matching_does_not_leak_unrelated_tickets(self):
        tickets = [
            {
                "slug": "task-vendty-payment-receipts",
                "title": "Recibos de Pago (Vendty / PrototypeZero)",
                "raw_ticket_name": "[AI] [Vendty] Generate and Share Payment Receipts",
                "branch": "",
                "percentage": 50,
            },
            {
                "slug": "task-unrelated-old",
                "title": "Old Incomplete Work",
                "raw_ticket_name": "Old Incomplete Work",
                "branch": "",
                "percentage": 90,
            },
        ]
        matched = server.find_matching_ticket_for_branch("feature/-GenerateSharePaymentReceipts", tickets)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["slug"], "task-vendty-payment-receipts")

        # Unrelated new feature branch must return None instead of leaking stale <100% tickets
        unmatched = server.find_matching_ticket_for_branch("feature/brand-new-auth-flow", tickets)
        self.assertIsNone(unmatched)

    def test_delete_tenant_handles_readonly_git_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            orig_tenants = server.TENANTS_DIR
            orig_active = server.ACTIVE_TENANT_FILE
            orig_local = server.LOCAL_JSON_FILE
            try:
                server.TENANTS_DIR = Path(tmp) / "tenants"
                server.ACTIVE_TENANT_FILE = Path(tmp) / ".active-tenant"
                server.LOCAL_JSON_FILE = Path(tmp) / "tenants.local.json"
                server.TENANTS_DIR.mkdir()

                ok, slug = server.create_tenant_structure("acme-ro")
                self.assertTrue(ok)
                ro_file = server.TENANTS_DIR / slug / "Proyecto" / "repo" / ".git" / "pack.idx"
                ro_file.parent.mkdir(parents=True)
                ro_file.write_text("locked", encoding="utf-8")
                os.chmod(ro_file, stat.S_IREAD)

                deleted, _ = server.delete_tenant_structure(slug)
                self.assertTrue(deleted)
                self.assertFalse((server.TENANTS_DIR / slug).exists())
            finally:
                server.TENANTS_DIR = orig_tenants
                server.ACTIVE_TENANT_FILE = orig_active
                server.LOCAL_JSON_FILE = orig_local

    def test_http_csrf_origin_and_html_injection(self):
        orig_port = server.ACTUAL_PORT
        httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.DashboardRequestHandler)
        port = httpd.server_address[1]
        server.ACTUAL_PORT = port
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()
        try:
            # 1. GET / injects session CSRF token and sets security headers
            with urlopen(f"http://127.0.0.1:{port}/", timeout=5) as resp:
                html = resp.read().decode("utf-8")
                self.assertEqual(resp.headers.get("X-Content-Type-Options"), "nosniff")
                self.assertEqual(resp.headers.get("X-Frame-Options"), "DENY")
                self.assertNotIn("__FAENA_CSRF_TOKEN__", html)
                self.assertIn(server.SESSION_CSRF_TOKEN, html)

            # 2. Cross-origin POST without token must be rejected with 403
            req_bad_origin = Request(
                f"http://127.0.0.1:{port}/api/run_quality_gate",
                data=json.dumps({"command": "echo hi"}).encode("utf-8"),
                headers={
                    "Host": f"127.0.0.1:{port}",
                    "Origin": "https://evil.example",
                    "Content-Type": "application/json",
                    "X-Faena-Token": server.SESSION_CSRF_TOKEN,
                },
                method="POST",
            )
            with self.assertRaises(HTTPError) as ctx:
                urlopen(req_bad_origin, timeout=5)
            self.assertEqual(ctx.exception.code, 403)

            # 3. Same-origin POST missing CSRF token must be rejected with 403
            req_no_csrf = Request(
                f"http://127.0.0.1:{port}/api/run_quality_gate",
                data=json.dumps({"command": "echo hi"}).encode("utf-8"),
                headers={
                    "Host": f"127.0.0.1:{port}",
                    "Origin": f"http://127.0.0.1:{port}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with self.assertRaises(HTTPError) as ctx2:
                urlopen(req_no_csrf, timeout=5)
            self.assertEqual(ctx2.exception.code, 403)

            # 4. Non-JSON Content-Type must be rejected with 415
            req_bad_ctype = Request(
                f"http://127.0.0.1:{port}/api/run_quality_gate",
                data=b'{"command":"echo hi"}',
                headers={
                    "Host": f"127.0.0.1:{port}",
                    "Origin": f"http://127.0.0.1:{port}",
                    "Content-Type": "text/plain",
                    "X-Faena-Token": server.SESSION_CSRF_TOKEN,
                },
                method="POST",
            )
            with self.assertRaises(HTTPError) as ctx3:
                urlopen(req_bad_ctype, timeout=5)
            self.assertEqual(ctx3.exception.code, 415)
        finally:
            httpd.shutdown()
            httpd.server_close()
            server.ACTUAL_PORT = orig_port

    def test_ticket_metadata_accepts_both_bold_styles(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = Path(tmp) / "task-demo"
            task_dir.mkdir()
            (task_dir / "design-demo.md").write_text(
                "# Demo\n\n**Ticket Origen:** ABC-123\n**Branch:** `feature/abc-123`\n",
                encoding="utf-8",
            )
            (task_dir / "README.md").write_text(
                "# Demo - Task Index\n\n**Location**: `tenants/x/Proyecto/repo/`\n\n"
                "| Tarea | Nombre | Fase | Size | Est. Hours | Dependencies | Agent |\n"
                "|---|---|---|---|---|---|---|\n"
                "| 01 | Setup | setup | S | 1h | - | npm-workspace-specialist |\n\n"
                "## Progress Tracking\n\n- [x] Task 01: Setup (setup)\n",
                encoding="utf-8",
            )
            data = server.get_ticket_data(task_dir, "x")
            self.assertEqual(data["branch"], "feature/abc-123")
            self.assertEqual(data["raw_ticket_name"], "ABC-123")
            self.assertEqual(data["repo"], "tenants/x/Proyecto/repo/")
            self.assertEqual(len(data["tasks"]), 1)
            self.assertTrue(data["tasks"][0]["completed"])

            (task_dir / "design-demo.md").write_text("**Branch**: `feature/legacy`\n", encoding="utf-8")
            self.assertEqual(server.get_ticket_data(task_dir, "x")["branch"], "feature/legacy")

    def test_active_tenant_resolution_follows_protocol(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tenants" / "acme").mkdir(parents=True)
            orig = (server.ACTIVE_TENANT_FILE, server.TENANTS_DIR)
            server.ACTIVE_TENANT_FILE = root / ".active-tenant"
            server.TENANTS_DIR = root / "tenants"
            try:
                # Sin archivo: default (raiz), nunca el primer tenant encontrado.
                self.assertEqual(server.get_active_tenant_slug(), "default")
                self.assertEqual(server.get_agent_tenant_info()["source"], "missing")
                # Tenant valido, con BOM incluido.
                server.ACTIVE_TENANT_FILE.write_bytes("\ufeffacme".encode("utf-8"))
                self.assertEqual(server.get_active_tenant_slug(), "acme")
                self.assertEqual(server.get_agent_tenant_info()["source"], "file")
                # Tenant inexistente: default, marcado como invalido.
                server.ACTIVE_TENANT_FILE.write_text("fantasma", encoding="utf-8")
                self.assertEqual(server.get_active_tenant_slug(), "default")
                info = server.get_agent_tenant_info()
                self.assertEqual(info["source"], "invalid")
                self.assertEqual(info["raw"], "fantasma")
            finally:
                server.ACTIVE_TENANT_FILE, server.TENANTS_DIR = orig


if __name__ == "__main__":
    unittest.main(verbosity=2)
