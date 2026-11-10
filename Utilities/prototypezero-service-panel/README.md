# P0 Service Panel

Personal thin web UI to start/stop PrototypeZero services. Lives outside the PrototypeZero repo.

| Group | How |
|-------|-----|
| **Infrastructure** | Docker Compose (`etc/docker/containers/*.yml`) |
| **Application services** | `dotnet run --launch-profile …` on the host |
| **Angular** | `npm start` in `apps/angular` |

## Run

```powershell
cd Utilities/prototypezero-service-panel
npm start
```

Open [http://localhost:3847](http://localhost:3847).

Requires **Docker Desktop** (for infra), **.NET SDK**, and for Angular **Node/npm**. No npm package dependencies for the panel itself.

## Config

Edit `config.json` (`repoRoot`, `port`) or set `PROTOZERO_ROOT` / `PORT`.

## Logs & PIDs

- Process tracking: `.runtime/pids.json`
- Per-service stdout/stderr: `.runtime/logs/<service>.log`

## Stop / restart a host app

Use the panel **Stop** / **Restart** buttons (kills the process tree listening on that service’s port). Example: Web Gateway → Stop, then Start.
