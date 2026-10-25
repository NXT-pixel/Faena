# Scripts for new developers

Run from **PrototypeZero repo root** (or invoke paths below from anywhere; they resolve the repo from `scripts`).

---

## 1. Start the **full** environment (recommended for first-time setup)

`start-env.ps1` and `start-env.sh` are thin wrappers. They run [`scripts/start-dev-environment.ps1`](../../scripts/start-dev-environment.ps1) (or the equivalent [`.sh`](../../scripts/start-dev-environment.sh)), which in one go:

- Creates the `prototypezero` Docker network (if needed)
- Starts **infrastructure** from `etc/docker/containers/*.yml` (SQL Server, Redis, RabbitMQ, monitoring, etc.)
- Creates `openiddict.pfx` for the Auth host (in a .NET SDK container) if missing
- **Publishes** all microservice/gateway projects (in a container; no local .NET required)
- Runs **`docker/docker-compose.apps.yml`** (all app containers, including Angular on port 4200)

**Requires:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine) with Compose. You do **not** need a local .NET SDK, Node, or ABP CLI for this path.

### PowerShell (Windows)

```powershell
.\.cursor\scripts\start-env.ps1
```

| Flag | Purpose |
|------|--------|
| `-NoCache` | `docker compose down` each infra stack, then `up` again (clean infra) |
| `-LocalSetup` | Optional: `abp install-libs` (if on PATH), `npm install` in `apps/angular`, `dotnet restore` (for local IDE / `ng serve` work) |
| `-SkipInfra` | Skip `etc/docker` (use if infra is already up) |
| `-SkipPublish` | Skip `dotnet publish` in container (faster if only changing frontend image build) |
| `-RegenerateAuthCert` | Regenerate `openiddict.pfx` |

**Stop the app stack:** `.\scripts\stop-dev-environment.ps1` (add `-StopInfra` to also stop `etc/docker`).

### Bash (WSL, macOS, Linux, Git Bash with Docker)

```bash
bash scripts/start-env.sh
bash scripts/start-env.sh --no-cache --local-setup
```

Same flags as long names: `--skip-infra`, `--skip-publish`, `--regenerate-auth-cert`.

**When it finishes:** open [http://localhost:4200/](http://localhost:4200/) (Angular in Docker), [http://localhost:44368/](http://localhost:44368/) (gateway), [http://localhost:44333/](http://localhost:44333/) (Auth). More detail: [scripts/README.md](../../scripts/README.md), [docker/README.md](../../docker/README.md).

**Infra only (no full stack):** you can still run `cd etc/docker` and `.\up.ps1` / `.\down.ps1` if you only need dependencies and run services on the host (ABP Studio, `dotnet run`, `ng serve`).

---

## 2. Analyze imports (onboarding / context)

Run when you want to see **where apps live** and **import/dependency patterns** (Angular, C#, Python).

### PowerShell

```powershell
.\.cursor\scripts\analyze-imports.ps1
.\.cursor\scripts\analyze-imports.ps1 -Check   # project map only
```

If you see quote/terminator errors, use: `.\.cursor\scripts\run-analyze-imports.ps1` (this repo’s script targets a generic template; PrototypeZero layout may differ). 

### Bash

```bash
bash scripts/analyze-imports.sh
bash scripts/analyze-imports.sh --check
```

See [README-analyze-imports.md](README-analyze-imports.md) for details.

