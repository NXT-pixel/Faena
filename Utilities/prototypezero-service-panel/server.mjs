import http from "node:http";
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const configPath = path.join(__dirname, "config.json");
const config = JSON.parse(fs.readFileSync(configPath, "utf8"));

const REPO_ROOT = path.resolve(__dirname, process.env.PROTOZERO_ROOT || config.repoRoot);
const PORT = Number(process.env.PORT || config.port || 3847);
const PUBLIC_DIR = path.join(__dirname, "public");
const RUNTIME_DIR = path.join(__dirname, ".runtime");
const PIDS_FILE = path.join(RUNTIME_DIR, "pids.json");
const LOGS_DIR = path.join(RUNTIME_DIR, "logs");

fs.mkdirSync(LOGS_DIR, { recursive: true });

const isWin = process.platform === "win32";

// Apps run on the host (dotnet run / npm start). Ports match WebGateway ReverseProxy Clusters.
const APP_SERVICES = [
  {
    id: "authserver",
    label: "Auth Server",
    port: 44333,
    gatewayCluster: "AuthServer",
    order: 1,
    group: "apps",
    run: "dotnet",
    project: "apps/auth-server/PrototypeZero.AuthServer/PrototypeZero.AuthServer.csproj",
    launchProfile: "PrototypeZero.AuthServer",
    why: "OIDC issuer — everything authenticates here",
  },
  {
    id: "identity",
    label: "Identity",
    port: 44305,
    gatewayCluster: "Identity",
    order: 2,
    group: "apps",
    run: "dotnet",
    project: "services/identity/PrototypeZero.IdentityService/PrototypeZero.IdentityService.csproj",
    launchProfile: "PrototypeZero.IdentityService",
    why: "Users / OpenIddict APIs",
  },
  {
    id: "administration",
    label: "Administration",
    port: 44388,
    gatewayCluster: "Administration",
    order: 3,
    group: "apps",
    run: "dotnet",
    project: "services/administration/PrototypeZero.AdministrationService/PrototypeZero.AdministrationService.csproj",
    launchProfile: "PrototypeZero.AdministrationService",
    why: "Permissions, settings, features",
  },
  {
    id: "saas",
    label: "SaaS",
    port: 44374,
    gatewayCluster: "Saas",
    order: 4,
    group: "apps",
    run: "dotnet",
    project: "services/saas/PrototypeZero.SaasService/PrototypeZero.SaasService.csproj",
    launchProfile: "PrototypeZero.SaasService",
    why: "Tenants & editions",
  },
  {
    id: "file-management",
    label: "File Management",
    port: 44346,
    gatewayCluster: "FileManagement",
    order: 5,
    group: "apps",
    run: "dotnet",
    project: "services/file-management/PrototypeZero.FileManagementService/PrototypeZero.FileManagementService.csproj",
    launchProfile: "PrototypeZero.FileManagementService",
    why: "Blob / file APIs",
  },
  {
    id: "core",
    label: "Core",
    port: 44314,
    gatewayCluster: "Core",
    order: 6,
    group: "apps",
    run: "dotnet",
    project: "services/core/PrototypeZero.CoreService/PrototypeZero.CoreService.csproj",
    launchProfile: "PrototypeZero.CoreService",
    why: "Commerce verticals + MCP",
  },
  {
    id: "payment",
    label: "Payment",
    port: 44367,
    gatewayCluster: "Payment",
    order: 7,
    group: "apps",
    run: "dotnet",
    project: "services/payment/PrototypeZero.PaymentService/PrototypeZero.PaymentService.csproj",
    launchProfile: "PrototypeZero.PaymentService",
    why: "Wompi / payment links (uses Core)",
  },
  {
    id: "whatsapp",
    label: "WhatsApp",
    port: 44364,
    gatewayCluster: "WhatsApp",
    order: 8,
    group: "apps",
    run: "dotnet",
    project: "services/whatsapp/PrototypeZero.WhatsAppService/PrototypeZero.WhatsAppService.csproj",
    launchProfile: "PrototypeZero.WhatsAppService",
    why: "Messaging + MassTransit (needs Rabbit)",
  },
  {
    id: "ai",
    label: "AI",
    port: 44366,
    gatewayCluster: "Ai",
    order: 9,
    group: "apps",
    run: "dotnet",
    project: "services/ai/PrototypeZero.AiService/PrototypeZero.AiService.csproj",
    launchProfile: "PrototypeZero.AiService",
    why: "Chat orchestration (uses Core + WhatsApp MCP)",
  },
  {
    id: "webgateway",
    label: "Web Gateway",
    port: 44368,
    gatewayCluster: null,
    order: 10,
    group: "apps",
    run: "dotnet",
    project: "gateways/web/PrototypeZero.WebGateway/PrototypeZero.WebGateway.csproj",
    launchProfile: "PrototypeZero.WebGateway",
    why: "YARP entrypoint — start after backends",
  },
  {
    id: "angular",
    label: "Angular",
    port: 4200,
    gatewayCluster: null,
    order: 11,
    group: "apps",
    run: "npm",
    cwd: "apps/angular",
    npmScript: "start",
    why: "SPA — last; needs Auth + Gateway",
  },
];

const INFRA_SERVICES = [
  {
    id: "sqlserver",
    label: "SQL Server",
    composeFile: "containers/sqlserver.yml",
    port: 1434,
    order: 1,
    group: "infra",
    required: true,
    why: "All ABP DbContexts (host 1434 → container 1433)",
  },
  {
    id: "redis",
    label: "Redis",
    composeFile: "containers/redis.yml",
    port: 6379,
    order: 2,
    group: "infra",
    required: true,
    why: "Distributed cache / data protection",
  },
  {
    id: "rabbitmq",
    label: "RabbitMQ",
    composeFile: "containers/rabbitmq.yml",
    port: 5672,
    uiPort: 15672,
    order: 3,
    group: "infra",
    required: true,
    why: "WhatsApp MassTransit",
  },
  {
    id: "elasticsearch",
    label: "Elasticsearch",
    composeFile: "containers/elasticsearch.yml",
    port: 9200,
    order: 4,
    group: "infra",
    required: false,
    why: "Optional logging / search",
  },
  {
    id: "kibana",
    label: "Kibana",
    composeFile: "containers/kibana.yml",
    port: 5601,
    order: 5,
    group: "infra",
    required: false,
    why: "Optional ES UI",
  },
  {
    id: "grafana",
    label: "Grafana",
    composeFile: "containers/grafana.yml",
    port: 3001,
    order: 6,
    group: "infra",
    required: false,
    why: "Optional dashboards (host 3001 → 3000)",
  },
  {
    id: "prometheus",
    label: "Prometheus",
    composeFile: "containers/prometheus.yml",
    port: 9090,
    order: 7,
    group: "infra",
    required: false,
    why: "Optional metrics",
  },
  {
    id: "postgres",
    label: "PostgreSQL",
    composeFile: "containers/postgresql.yml",
    port: 5432,
    order: 8,
    group: "infra",
    required: false,
    why: "Optional / secondary DB",
  },
];

const PORT_NOTES = {
  summary:
    "Apps use dotnet run / npm start on the host. Ports match WebGateway ReverseProxy Clusters in appsettings.json (localhost:443xx). Infra stays in Docker.",
  gatewayFile:
    "gateways/web/PrototypeZero.WebGateway/appsettings.json → ReverseProxy:Clusters",
};

const ALL = [...APP_SERVICES, ...INFRA_SERVICES];
const byId = Object.fromEntries(ALL.map((s) => [s.id, s]));

const etcDockerDir = path.join(REPO_ROOT, "etc", "docker");

function run(cmd, args, cwd) {
  return new Promise((resolve) => {
    const child = spawn(cmd, args, {
      cwd,
      shell: false,
      windowsHide: true,
      env: process.env,
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (d) => (stdout += d.toString()));
    child.stderr.on("data", (d) => (stderr += d.toString()));
    child.on("close", (code) => resolve({ code: code ?? 1, stdout, stderr }));
    child.on("error", (err) => resolve({ code: 1, stdout, stderr: String(err) }));
  });
}

function loadPids() {
  try {
    return JSON.parse(fs.readFileSync(PIDS_FILE, "utf8"));
  } catch {
    return {};
  }
}

function savePids(map) {
  fs.writeFileSync(PIDS_FILE, JSON.stringify(map, null, 2));
}

function setPid(id, pid) {
  const map = loadPids();
  if (pid == null) delete map[id];
  else map[id] = { pid, startedAt: new Date().toISOString() };
  savePids(map);
}

function isPidAlive(pid) {
  if (!pid || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

/** One netstat call → Map<port, pid>. Avoids slow per-port PowerShell (was hanging /api/status). */
async function getListeningPortMap() {
  const map = new Map();
  if (isWin) {
    // No `-p tcp`: that only lists IPv4 on Windows, and Node/ng serve binds
    // localhost on IPv6 ([::1]:4200) — the listener would be missed.
    const result = await run("netstat.exe", ["-ano"]);
    for (const line of result.stdout.split(/\r?\n/)) {
      if (!/LISTENING/i.test(line)) continue;
      const parts = line.trim().split(/\s+/);
      // Proto LocalAddress ForeignAddress State PID
      if (parts.length < 5) continue;
      const local = parts[1];
      const pid = Number(parts[parts.length - 1]);
      const m = local.match(/:(\d+)$/);
      if (!m || !Number.isFinite(pid) || pid <= 0) continue;
      const port = Number(m[1]);
      if (!map.has(port)) map.set(port, pid);
    }
    return map;
  }
  const result = await run("netstat", ["-lntp"]);
  for (const line of result.stdout.split(/\r?\n/)) {
    if (!/LISTEN/i.test(line)) continue;
    const m = line.match(/:(\d+)\s+.*LISTEN\s+(\d+)/);
    if (!m) continue;
    const port = Number(m[1]);
    const pid = Number(m[2]);
    if (!map.has(port)) map.set(port, pid);
  }
  return map;
}

async function getListenerPid(port) {
  const map = await getListeningPortMap();
  return map.get(Number(port)) || null;
}

async function ensureNetwork() {
  const listed = await run("docker", ["network", "ls", "--format", "{{.Name}}"]);
  if (!listed.stdout.split(/\r?\n/).includes("prototypezero")) {
    return run("docker", ["network", "create", "prototypezero", "--label=prototypezero"]);
  }
  return { code: 0, stdout: "", stderr: "" };
}

async function infraCompose(composeFile, args) {
  return run("docker", ["compose", "-f", composeFile, ...args], etcDockerDir);
}

function normalizeState(raw) {
  const s = (raw || "").toLowerCase();
  if (s.includes("running") || s === "up") return "running";
  if (s.includes("restarting")) return "restarting";
  if (s.includes("paused")) return "paused";
  if (s.includes("exited") || s.includes("dead") || s.includes("created")) return "stopped";
  if (!s) return "absent";
  return s;
}

async function statusApps() {
  const map = {};
  const stored = loadPids();
  const ports = await getListeningPortMap();
  const nextPids = { ...stored };

  for (const svc of APP_SERVICES) {
    const listenerPid = ports.get(Number(svc.port)) || null;
    const tracked = stored[svc.id]?.pid;
    const trackedAlive = isPidAlive(tracked);

    if (listenerPid) {
      map[svc.id] = {
        state: "running",
        status: `listening :${svc.port} (pid ${listenerPid})`,
        name: `host:${svc.id}`,
        pid: listenerPid,
        mode: svc.run,
      };
      nextPids[svc.id] = {
        pid: listenerPid,
        startedAt: stored[svc.id]?.startedAt || new Date().toISOString(),
      };
      continue;
    }

    if (trackedAlive) {
      map[svc.id] = {
        state: "starting",
        status: `process ${tracked} (not listening yet)`,
        name: `host:${svc.id}`,
        pid: tracked,
        mode: svc.run,
      };
      continue;
    }

    if (tracked) delete nextPids[svc.id];
    map[svc.id] = {
      state: "stopped",
      status: "not running",
      name: null,
      pid: null,
      mode: svc.run,
    };
  }

  savePids(nextPids);
  return map;
}

async function statusInfra() {
  const map = {};
  const all = await run("docker", [
    "ps",
    "-a",
    "--format",
    "{{.Names}}\t{{.Status}}\t{{.State}}",
  ]);

  if (all.code !== 0) {
    const err = (all.stderr || all.stdout || `docker exit ${all.code}`).trim();
    for (const s of INFRA_SERVICES) {
      map[s.id] = {
        state: "absent",
        status: `docker error: ${err || "not available"}`,
        name: null,
      };
    }
    return map;
  }

  for (const line of all.stdout.split(/\r?\n/).filter(Boolean)) {
    const [name, status, state] = line.split("\t");
    const match =
      INFRA_SERVICES.find((s) => name === s.id) ||
      INFRA_SERVICES.find((s) => name.startsWith(`${s.id}-`));
    if (match) {
      map[match.id] = {
        state: normalizeState(state || status),
        status: status || "",
        name,
      };
    }
  }

  return map;
}

async function killPidTree(pid) {
  if (!pid) return { code: 0, stdout: "", stderr: "" };
  if (isWin) {
    return run("taskkill.exe", ["/PID", String(pid), "/T", "/F"]);
  }
  try {
    process.kill(-pid, "SIGTERM");
  } catch {
    try {
      process.kill(pid, "SIGTERM");
    } catch {
      /* ignore */
    }
  }
  return { code: 0, stdout: "", stderr: "" };
}

function spawnDetached(cmd, args, cwd, logPath) {
  // Keep the fd open for the child's lifetime (do not close after spawn on Windows).
  const logFd = fs.openSync(logPath, "a");
  let child;
  try {
    child = spawn(cmd, args, {
      cwd,
      shell: false,
      windowsHide: true,
      detached: true,
      stdio: ["ignore", logFd, logFd],
      env: {
        ...process.env,
        DOTNET_ENVIRONMENT: "Development",
        ASPNETCORE_ENVIRONMENT: "Development",
      },
    });
  } catch (err) {
    try {
      fs.writeSync(logFd, `\n[panel] spawn failed: ${String(err?.stack || err)}\n`);
      fs.closeSync(logFd);
    } catch {
      /* ignore */
    }
    return null;
  }
  child.on("error", (err) => {
    try {
      fs.writeSync(logFd, `\n[panel] spawn error: ${String(err?.stack || err)}\n`);
    } catch {
      /* ignore */
    }
  });
  child.on("exit", () => {
    try {
      fs.closeSync(logFd);
    } catch {
      /* already closed */
    }
  });
  child.unref();
  return child.pid;
}

function logPathFor(id) {
  return path.join(LOGS_DIR, `${id}.log`);
}

function readLogTail(id, maxBytes = 120_000) {
  const file = logPathFor(id);
  if (!fs.existsSync(file)) {
    return { text: "(no log yet — start the service to capture console output)\n", size: 0, mtime: null };
  }
  const stat = fs.statSync(file);
  const size = stat.size;
  const start = Math.max(0, size - maxBytes);
  const fd = fs.openSync(file, "r");
  try {
    const buf = Buffer.alloc(size - start);
    fs.readSync(fd, buf, 0, buf.length, start);
    let text = buf.toString("utf8");
    if (start > 0) text = `… (earlier output truncated)\n${text}`;
    return { text, size, mtime: stat.mtime.toISOString() };
  } finally {
    fs.closeSync(fd);
  }
}

function clearAllLogs() {
  const cleared = [];
  const failed = [];
  for (const svc of APP_SERVICES) {
    const file = logPathFor(svc.id);
    try {
      if (fs.existsSync(file)) {
        fs.truncateSync(file, 0);
      } else {
        fs.writeFileSync(file, "");
      }
      cleared.push(svc.id);
    } catch (err) {
      failed.push({ id: svc.id, error: String(err?.message || err) });
    }
  }
  return { cleared, failed };
}

function streamLogs(req, res, id) {
  if (!byId[id] || byId[id].group !== "apps") {
    json(res, 404, { error: "Unknown app service" });
    return;
  }

  res.writeHead(200, {
    "Content-Type": "text/event-stream; charset=utf-8",
    "Cache-Control": "no-cache, no-transform",
    Connection: "keep-alive",
  });
  res.write(`event: ready\ndata: ${JSON.stringify({ id })}\n\n`);

  const file = logPathFor(id);
  let offset = 0;
  if (fs.existsSync(file)) {
    const initial = readLogTail(id);
    offset = initial.size;
    res.write(`event: snapshot\ndata: ${JSON.stringify({ text: initial.text, size: initial.size })}\n\n`);
  } else {
    res.write(
      `event: snapshot\ndata: ${JSON.stringify({
        text: "(no log yet — start the service to capture console output)\n",
        size: 0,
      })}\n\n`
    );
  }

  const timer = setInterval(() => {
    try {
      if (!fs.existsSync(file)) return;
      const size = fs.statSync(file).size;
      if (size < offset) {
        // log rotated / truncated
        offset = 0;
      }
      if (size > offset) {
        const fd = fs.openSync(file, "r");
        try {
          const buf = Buffer.alloc(size - offset);
          fs.readSync(fd, buf, 0, buf.length, offset);
          offset = size;
          res.write(
            `event: append\ndata: ${JSON.stringify({ text: buf.toString("utf8"), size })}\n\n`
          );
        } finally {
          fs.closeSync(fd);
        }
      } else {
        res.write(`event: ping\ndata: {}\n\n`);
      }
    } catch (err) {
      res.write(`event: error\ndata: ${JSON.stringify({ error: String(err) })}\n\n`);
    }
  }, 800);

  const cleanup = () => clearInterval(timer);
  req.on("close", cleanup);
  res.on("close", cleanup);
}

async function startAppHost(svc) {
  const existing = await getListenerPid(svc.port);
  if (existing) {
    setPid(svc.id, existing);
    return {
      ok: true,
      stdout: `Already listening on :${svc.port} (pid ${existing})`,
      stderr: "",
    };
  }

  const tracked = loadPids()[svc.id]?.pid;
  if (isPidAlive(tracked)) {
    return {
      ok: true,
      stdout: `Already starting (pid ${tracked})`,
      stderr: "",
    };
  }

  const logPath = path.join(LOGS_DIR, `${svc.id}.log`);
  fs.writeFileSync(
    logPath,
    `\n===== start ${new Date().toISOString()} =====\n`,
    { flag: "a" }
  );

  let pid;
  if (svc.run === "dotnet") {
    const projectPath = path.join(REPO_ROOT, svc.project);
    if (!fs.existsSync(projectPath)) {
      return { ok: false, error: `Project not found: ${projectPath}` };
    }
    const cwd = path.dirname(projectPath);
    pid = spawnDetached(
      "dotnet",
      ["run", "--project", projectPath, "--launch-profile", svc.launchProfile],
      cwd,
      logPath
    );
  } else if (svc.run === "npm") {
    const cwd = path.join(REPO_ROOT, svc.cwd);
    if (!fs.existsSync(path.join(cwd, "package.json"))) {
      return { ok: false, error: `Angular app not found: ${cwd}` };
    }
    // On Windows npm is a .cmd shim — Node spawn(..., shell:false) throws EINVAL for it.
    // Launch through cmd.exe instead so Angular works like the .NET (real .exe) services.
    if (isWin) {
      pid = spawnDetached(
        "cmd.exe",
        ["/d", "/s", "/c", "npm", "run", svc.npmScript || "start"],
        cwd,
        logPath
      );
    } else {
      pid = spawnDetached("npm", ["run", svc.npmScript || "start"], cwd, logPath);
    }
  } else {
    return { ok: false, error: `Unknown run mode: ${svc.run}` };
  }

  if (!pid) {
    return {
      ok: false,
      error: `Failed to spawn process. See log: ${logPath}`,
    };
  }

  setPid(svc.id, pid);
  return {
    ok: true,
    stdout: `Started ${svc.id} (pid ${pid}). Log: ${logPath}`,
    stderr: "",
    pid,
  };
}

async function stopAppHost(svc) {
  const stored = loadPids()[svc.id]?.pid;
  const listenerPid = await getListenerPid(svc.port);
  const pids = new Set([stored, listenerPid].filter((p) => p && p > 0));

  if (!pids.size) {
    setPid(svc.id, null);
    return { ok: true, stdout: "Already stopped", stderr: "" };
  }

  const errors = [];
  for (const pid of pids) {
    const result = await killPidTree(pid);
    if (result.code !== 0 && !/not found|no running/i.test(result.stderr || "")) {
      errors.push(result.stderr || result.stdout || `exit ${result.code}`);
    }
  }

  // Wait briefly and force-clear port holder if still up
  await new Promise((r) => setTimeout(r, 400));
  const still = await getListenerPid(svc.port);
  if (still) {
    await killPidTree(still);
  }

  setPid(svc.id, null);
  return {
    ok: errors.length === 0,
    stdout: `Stopped ${[...pids].join(", ")}`,
    stderr: errors.join("\n"),
    error: errors.length ? errors.join("\n") : undefined,
  };
}

async function dockerContainerState(name) {
  const result = await run("docker", ["inspect", "--format", "{{.State.Status}}", name]);
  if (result.code !== 0) return null;
  return (result.stdout || "").trim() || null;
}

async function startService(id) {
  const svc = byId[id];
  if (!svc) return { ok: false, error: `Unknown service: ${id}` };

  if (svc.group === "apps") {
    return startAppHost(svc);
  }

  await ensureNetwork();

  // Reuse an existing container with this exact name (e.g. rabbitmq created outside
  // the current Compose project). `compose up` would fail with a name conflict.
  const existing = await dockerContainerState(svc.id);
  if (existing) {
    if (existing === "running") {
      return { ok: true, stdout: `${svc.id} already running`, stderr: "" };
    }
    const started = await run("docker", ["start", svc.id]);
    return {
      ok: started.code === 0,
      stdout: started.stdout || `Started existing container ${svc.id}`,
      stderr: started.stderr,
      error:
        started.code === 0
          ? undefined
          : started.stderr || started.stdout || `exit ${started.code}`,
    };
  }

  const result = await infraCompose(svc.composeFile, ["up", "-d"]);
  return {
    ok: result.code === 0,
    stdout: result.stdout,
    stderr: result.stderr,
    error: result.code === 0 ? undefined : result.stderr || result.stdout || `exit ${result.code}`,
  };
}

async function stopService(id) {
  const svc = byId[id];
  if (!svc) return { ok: false, error: `Unknown service: ${id}` };

  if (svc.group === "apps") {
    return stopAppHost(svc);
  }

  // Prefer docker stop by name so non-Compose / differently-projected containers stop too.
  const existing = await dockerContainerState(svc.id);
  if (existing) {
    if (existing !== "running") {
      return { ok: true, stdout: `${svc.id} already stopped`, stderr: "" };
    }
    const stopped = await run("docker", ["stop", svc.id]);
    return {
      ok: stopped.code === 0,
      stdout: stopped.stdout || `Stopped ${svc.id}`,
      stderr: stopped.stderr,
      error:
        stopped.code === 0
          ? undefined
          : stopped.stderr || stopped.stdout || `exit ${stopped.code}`,
    };
  }

  const result = await infraCompose(svc.composeFile, ["stop"]);
  return {
    ok: result.code === 0,
    stdout: result.stdout,
    stderr: result.stderr,
    error: result.code === 0 ? undefined : result.stderr || result.stdout || `exit ${result.code}`,
  };
}

async function restartService(id) {
  const stopped = await stopService(id);
  if (!stopped.ok) return stopped;
  await new Promise((r) => setTimeout(r, 500));
  return startService(id);
}

function json(res, status, body) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
  });
  res.end(payload);
}

function contentType(filePath) {
  if (filePath.endsWith(".html")) return "text/html; charset=utf-8";
  if (filePath.endsWith(".css")) return "text/css; charset=utf-8";
  if (filePath.endsWith(".js")) return "text/javascript; charset=utf-8";
  if (filePath.endsWith(".svg")) return "image/svg+xml";
  return "application/octet-stream";
}

function serveStatic(req, res) {
  let urlPath = decodeURIComponent(new URL(req.url, `http://${req.headers.host}`).pathname);
  if (urlPath === "/") urlPath = "/index.html";
  const filePath = path.normalize(path.join(PUBLIC_DIR, urlPath));
  if (!filePath.startsWith(PUBLIC_DIR)) {
    res.writeHead(403).end("Forbidden");
    return;
  }
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    res.writeHead(404).end("Not found");
    return;
  }
  res.writeHead(200, { "Content-Type": contentType(filePath) });
  fs.createReadStream(filePath).pipe(res);
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  if (!chunks.length) return {};
  try {
    return JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } catch {
    return {};
  }
}

function validateRepo() {
  const coreProj = path.join(
    REPO_ROOT,
    "services/core/PrototypeZero.CoreService/PrototypeZero.CoreService.csproj"
  );
  const ok = fs.existsSync(coreProj) && fs.existsSync(etcDockerDir);
  return {
    ok,
    repoRoot: REPO_ROOT,
    etcDockerDir,
    appMode: "dotnet-run",
  };
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const { pathname } = url;

    if (req.method === "GET" && pathname === "/api/health") {
      return json(res, 200, { ok: true, ...validateRepo() });
    }

    if (req.method === "GET" && pathname === "/api/services") {
      const apps = [...APP_SERVICES].sort((a, b) => a.order - b.order);
      const infra = [...INFRA_SERVICES].sort((a, b) => a.order - b.order);
      return json(res, 200, {
        repoRoot: REPO_ROOT,
        apps,
        infra,
        portNotes: PORT_NOTES,
        startOrder: {
          infra: infra.map((s) => ({
            order: s.order,
            id: s.id,
            label: s.label,
            required: s.required,
            why: s.why,
          })),
          apps: apps.map((s) => ({
            order: s.order,
            id: s.id,
            label: s.label,
            port: s.port,
            gatewayCluster: s.gatewayCluster,
            why: s.why,
            run: s.run,
          })),
        },
      });
    }

    if (req.method === "GET" && pathname === "/api/status") {
      const [apps, infra] = await Promise.all([statusApps(), statusInfra()]);
      const services = {};
      for (const s of ALL) {
        const info = (s.group === "apps" ? apps : infra)[s.id];
        services[s.id] = info || { state: "stopped", status: "not running", name: null };
      }
      return json(res, 200, { services, repo: validateRepo() });
    }

    if (req.method === "POST" && pathname === "/api/logs/clear-all") {
      const result = clearAllLogs();
      return json(res, result.failed.length ? 207 : 200, {
        ok: result.failed.length === 0,
        ...result,
      });
    }

    // GET /api/services/:id/logs  |  /api/services/:id/logs/stream
    if (req.method === "GET" && pathname.startsWith("/api/services/") && pathname.includes("/logs")) {
      const parts = pathname.split("/").filter(Boolean);
      // api services :id logs [stream]
      const id = parts[2];
      const svc = byId[id];
      if (!svc || svc.group !== "apps") {
        return json(res, 404, { error: "Unknown app service" });
      }
      if (parts[3] === "logs" && parts[4] === "stream") {
        return streamLogs(req, res, id);
      }
      if (parts[3] === "logs") {
        return json(res, 200, { id, ...readLogTail(id) });
      }
    }

    if (req.method === "POST" && pathname.startsWith("/api/services/")) {
      const parts = pathname.split("/").filter(Boolean);
      const id = parts[2];
      const action = parts[3];
      if (!byId[id]) return json(res, 404, { ok: false, error: "Unknown service" });

      let result;
      if (action === "start") result = await startService(id);
      else if (action === "stop") result = await stopService(id);
      else if (action === "restart") result = await restartService(id);
      else return json(res, 400, { ok: false, error: "Unknown action" });

      return json(res, result.ok ? 200 : 500, result);
    }

    if (req.method === "POST" && pathname === "/api/bulk") {
      const body = await readBody(req);
      const group = body.group;
      const action = body.action;
      const base = group === "infra" ? INFRA_SERVICES : APP_SERVICES;
      const list = [...base].sort((a, b) =>
        action === "stop" ? b.order - a.order : a.order - b.order
      );
      const results = [];

      if (action === "start" && group === "infra") await ensureNetwork();

      for (const svc of list) {
        const result =
          action === "start"
            ? await startService(svc.id)
            : action === "stop"
              ? await stopService(svc.id)
              : { ok: false, error: "Unknown action" };
        results.push({ id: svc.id, order: svc.order, ...result });
      }
      return json(res, 200, { results });
    }

    if (req.method === "GET") {
      return serveStatic(req, res);
    }

    json(res, 404, { error: "Not found" });
  } catch (err) {
    json(res, 500, { ok: false, error: String(err?.stack || err) });
  }
});

server.listen(PORT, () => {
  const repo = validateRepo();
  console.log(`PrototypeZero service panel → http://localhost:${PORT}`);
  console.log(`Repo: ${REPO_ROOT}`);
  console.log("Apps: dotnet run / npm start  |  Infra: Docker");
  if (!repo.ok) {
    console.warn("WARNING: repo path looks incomplete. Edit config.json or set PROTOZERO_ROOT.");
  }
});
