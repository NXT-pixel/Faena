const appsGrid = document.getElementById("appsGrid");
const infraGrid = document.getElementById("infraGrid");
const infraOrder = document.getElementById("infraOrder");
const appsOrder = document.getElementById("appsOrder");
const portNotes = document.getElementById("portNotes");
const repoPath = document.getElementById("repoPath");
const toast = document.getElementById("toast");
const refreshBtn = document.getElementById("refreshBtn");
const consoleTabs = document.getElementById("consoleTabs");
const consoleOut = document.getElementById("consoleOut");
const consoleClearBtn = document.getElementById("consoleClearBtn");
const consoleClearAllBtn = document.getElementById("consoleClearAllBtn");
const consoleFollowBtn = document.getElementById("consoleFollowBtn");

/** @type {Record<string, HTMLElement>} */
const cards = {};
let busy = new Set();
let catalog = { apps: [], infra: [] };

let activeConsoleId = null;
/** @type {EventSource | null} */
let logSource = null;
let followConsole = true;
/** @type {Record<string, string>} */
const consoleBuffers = {};

function setToast(message, isError = false) {
  toast.textContent = message || "";
  toast.classList.toggle("error", Boolean(isError));
}

function portLine(svc) {
  const parts = [];
  if (svc.port != null) parts.push(`:${svc.port}`);
  if (svc.uiPort != null) parts.push(`ui :${svc.uiPort}`);
  if (svc.run === "dotnet") parts.push("dotnet run");
  else if (svc.run === "npm") parts.push("npm start");
  else if (svc.group === "infra") parts.push("docker");
  if (svc.gatewayCluster) parts.push(`gw → ${svc.gatewayCluster}`);
  return parts.join(" · ");
}

function cardHtml(svc) {
  const el = document.createElement("article");
  el.className = "card";
  el.dataset.id = svc.id;
  const meta =
    svc.group === "apps"
      ? `<button type="button" class="console-link" data-console="${svc.id}">Console</button>`
      : "";
  el.innerHTML = `
    <div class="card-top">
      <div class="card-copy">
        <div class="name-row">
          <span class="order-pill">${svc.order}</span>
          <h3 class="name">${svc.label}</h3>
        </div>
        <p class="port">${portLine(svc)}</p>
        <p class="why">${svc.why || ""}</p>
      </div>
      <div class="card-meta">
        <span class="badge stopped">stopped</span>
        ${meta}
      </div>
    </div>
    <p class="status-line">—</p>
    <div class="actions">
      <button type="button" class="primary" data-action="start">Start</button>
      <button type="button" class="danger" data-action="stop">Stop</button>
      <button type="button" data-action="restart">Restart</button>
    </div>
  `;
  el.querySelectorAll("button[data-action]").forEach((btn) => {
    btn.addEventListener("click", () => act(svc.id, btn.dataset.action));
  });
  el.querySelectorAll("button[data-console]").forEach((btn) => {
    btn.addEventListener("click", () => openConsole(btn.dataset.console));
  });
  return el;
}

function orderItemHtml(entry, group) {
  const li = document.createElement("li");
  const optional = group === "infra" && entry.required === false;
  li.className = optional ? "optional" : "required";
  const portBit =
    entry.port != null
      ? ` · :${entry.port}${entry.gatewayCluster ? ` (${entry.gatewayCluster})` : ""}`
      : "";
  const reqBit = optional ? "optional" : group === "infra" ? "required" : "";
  li.innerHTML = `
    <span class="order-step">${entry.order}</span>
    <div class="order-body">
      <strong>${entry.label}${portBit}</strong>
      <span>${entry.why || ""}${reqBit ? ` · ${reqBit}` : ""}</span>
    </div>
  `;
  return li;
}

function renderOrder(startOrder, notes) {
  portNotes.textContent = notes?.summary || "";
  infraOrder.replaceChildren(
    ...(startOrder?.infra || []).map((e) => orderItemHtml(e, "infra"))
  );
  appsOrder.replaceChildren(
    ...(startOrder?.apps || []).map((e) => orderItemHtml(e, "apps"))
  );
}

function renderConsoleTabs() {
  const apps = [...catalog.apps].sort((a, b) => a.order - b.order);
  consoleTabs.replaceChildren(
    ...apps.map((svc) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = svc.label;
      btn.dataset.id = svc.id;
      if (svc.id === activeConsoleId) btn.classList.add("active");
      btn.addEventListener("click", () => openConsole(svc.id));
      return btn;
    })
  );
}

function paintConsole() {
  consoleOut.textContent = consoleBuffers[activeConsoleId] || "";
  if (followConsole) {
    consoleOut.scrollTop = consoleOut.scrollHeight;
  }
  consoleTabs.querySelectorAll("button").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.id === activeConsoleId);
  });
}

function openConsole(id) {
  if (!id) return;
  if (activeConsoleId === id && logSource) {
    document.querySelector(".console-panel")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    return;
  }
  activeConsoleId = id;
  if (logSource) {
    logSource.close();
    logSource = null;
  }
  if (consoleBuffers[id] == null) consoleBuffers[id] = "";
  paintConsole();
  renderConsoleTabs();

  logSource = new EventSource(`/api/services/${id}/logs/stream`);
  logSource.addEventListener("snapshot", (ev) => {
    try {
      const data = JSON.parse(ev.data);
      consoleBuffers[id] = data.text || "";
      if (activeConsoleId === id) paintConsole();
    } catch {
      /* ignore */
    }
  });
  logSource.addEventListener("append", (ev) => {
    try {
      const data = JSON.parse(ev.data);
      consoleBuffers[id] = (consoleBuffers[id] || "") + (data.text || "");
      // keep buffer from growing forever in the browser
      if (consoleBuffers[id].length > 400_000) {
        consoleBuffers[id] = consoleBuffers[id].slice(-300_000);
      }
      if (activeConsoleId === id) paintConsole();
    } catch {
      /* ignore */
    }
  });
  logSource.onerror = () => {
    // browser will retry EventSource; leave buffer as-is
  };

  document.querySelector(".console-panel")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function renderCatalog() {
  const apps = [...catalog.apps].sort((a, b) => a.order - b.order);
  const infra = [...catalog.infra].sort((a, b) => a.order - b.order);
  appsGrid.replaceChildren(...apps.map(cardHtml));
  infraGrid.replaceChildren(...infra.map(cardHtml));
  for (const el of [...appsGrid.children, ...infraGrid.children]) {
    cards[el.dataset.id] = el;
  }
  if (!activeConsoleId && apps[0]) activeConsoleId = apps[0].id;
  renderConsoleTabs();
  if (activeConsoleId) openConsole(activeConsoleId);
}

function paintStatus(services) {
  for (const [id, info] of Object.entries(services)) {
    const card = cards[id];
    if (!card) continue;
    const badge = card.querySelector(".badge");
    const line = card.querySelector(".status-line");
    const state = busy.has(id) ? "busy" : info.state || "absent";
    badge.className = `badge ${state}`;
    badge.textContent = busy.has(id) ? "working" : state;
    line.textContent = info.status || info.name || "—";
    const disabled = busy.has(id);
    card.querySelectorAll("button[data-action]").forEach((b) => {
      b.disabled = disabled;
    });
  }
}

async function loadCatalog() {
  const res = await fetch("/api/services");
  const data = await res.json();
  catalog = data;
  repoPath.textContent = data.repoRoot;
  repoPath.title = data.repoRoot;
  renderOrder(data.startOrder, data.portNotes);
  renderCatalog();
}

async function refreshStatus() {
  const res = await fetch("/api/status");
  if (!res.ok) throw new Error(`status HTTP ${res.status}`);
  const data = await res.json();
  if (data.repo?.repoRoot) {
    repoPath.textContent = data.repo.repoRoot;
    repoPath.title = data.repo.repoRoot;
  }
  if (data.repo && !data.repo.ok) {
    setToast("Repo path incomplete — check config.json", true);
  }
  paintStatus(data.services || {});
  const dockerErr = Object.values(data.services || {}).find((s) =>
    String(s.status || "").startsWith("docker error:")
  );
  if (dockerErr) setToast(dockerErr.status, true);
}

async function act(id, action) {
  busy.add(id);
  paintStatus({ [id]: { state: "busy", status: `${action}…` } });
  setToast(`${action} ${id}…`);
  if (action === "start" || action === "restart") {
    openConsole(id);
  }
  try {
    const res = await fetch(`/api/services/${id}/${action}`, { method: "POST" });
    const data = await res.json();
    if (!data.ok) throw new Error(data.error || `Failed to ${action} ${id}`);
    setToast(`${action} ${id} ok`);
  } catch (err) {
    setToast(String(err.message || err), true);
  } finally {
    busy.delete(id);
    await refreshStatus();
  }
}

async function bulk(group, action) {
  const list = group === "infra" ? catalog.infra : catalog.apps;
  list.forEach((s) => busy.add(s.id));
  setToast(`${action} all ${group} (${action === "stop" ? "reverse " : ""}order)…`);
  if (group === "apps" && action === "start" && list[0]) {
    openConsole(list[0].id);
  }
  await refreshStatus();
  try {
    const res = await fetch("/api/bulk", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ group, action }),
    });
    const data = await res.json();
    const failed = (data.results || []).filter((r) => !r.ok);
    if (failed.length) {
      setToast(`${failed.length} failed: ${failed.map((f) => f.id).join(", ")}`, true);
    } else {
      setToast(`${action} all ${group} ok`);
    }
  } catch (err) {
    setToast(String(err.message || err), true);
  } finally {
    busy = new Set();
    await refreshStatus();
  }
}

document.querySelectorAll("[data-bulk]").forEach((btn) => {
  btn.addEventListener("click", () => {
    const [group, action] = btn.dataset.bulk.split(":");
    bulk(group, action);
  });
});

refreshBtn.addEventListener("click", () => refreshStatus().catch(console.error));

consoleClearBtn.addEventListener("click", () => {
  if (!activeConsoleId) return;
  consoleBuffers[activeConsoleId] = "";
  paintConsole();
});

consoleClearAllBtn.addEventListener("click", async () => {
  consoleClearAllBtn.disabled = true;
  try {
    const res = await fetch("/api/logs/clear-all", { method: "POST" });
    const data = await res.json();
    for (const id of Object.keys(consoleBuffers)) {
      consoleBuffers[id] = "";
    }
    if (activeConsoleId) consoleBuffers[activeConsoleId] = "";
    paintConsole();
    if (data.failed?.length) {
      setToast(
        `Cleared ${data.cleared.length} logs; failed: ${data.failed.map((f) => f.id).join(", ")}`,
        true
      );
    } else {
      setToast(`Cleared all ${data.cleared.length} console logs`);
    }
  } catch (err) {
    setToast(String(err.message || err), true);
  } finally {
    consoleClearAllBtn.disabled = false;
  }
});

consoleFollowBtn.addEventListener("click", () => {
  followConsole = true;
  paintConsole();
});

consoleOut.addEventListener("scroll", () => {
  const nearBottom =
    consoleOut.scrollHeight - consoleOut.scrollTop - consoleOut.clientHeight < 40;
  followConsole = nearBottom;
});

await loadCatalog();
await refreshStatus();
setInterval(() => {
  if (busy.size === 0) refreshStatus().catch(() => {});
}, 5000);
