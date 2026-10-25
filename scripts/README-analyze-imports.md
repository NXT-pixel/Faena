# Onboarding: analyze-imports

**Run this when you start the project** to see where Angular, C#, and Python apps live and how to run them, plus import/dependency patterns.

## From repo root (`orchestration_framework`)

### Option 1: Bash (Git Bash or WSL on Windows)

```bash
bash AngularWithMCPServers/scripts/analyze-imports.sh
```

- `--full` (default): project map + Angular/C#/Python import analysis  
- `--check`: project map only (quick overview)

### Option 2: PowerShell (Windows)

```powershell
.\AngularWithMCPServers\.cursor\scripts\analyze-imports.ps1
```

- Add `-Check` for project map only.

If you see "string is missing the terminator", run via the launcher (it normalizes quotes):

```powershell
.\AngularWithMCPServers\.cursor\scripts\run-analyze-imports.ps1
```

## What you get

- **Project map**: Angular app, all .NET projects, Python Azure Functions apps and how to run them  
- **Angular**: external vs internal imports (Control Panel)  
- **C#**: project references and top `using` namespaces per project  
- **Python**: import counts and `requirements.txt` per app

