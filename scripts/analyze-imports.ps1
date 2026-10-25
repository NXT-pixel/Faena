# analyze-imports.ps1 — Onboarding & import analysis for the Orchestration Framework
#
# Run this when you start the project to see:
#   - Where Angular, C#, and Python apps live and how to run them
#   - Import/dependency patterns across the monorepo
#
# Usage: from repo root (orchestration_framework):
#   .\AngularWithMCPServers\.cursor\scripts\analyze-imports.ps1
#   .\AngularWithMCPServers\.cursor\scripts\analyze-imports.ps1 -Check
#
# Or from anywhere, then cd to repo root first:
#   cd "D:\Orchestration Framework\orchestration_framework"
#   .\AngularWithMCPServers\.cursor\scripts\analyze-imports.ps1

param(
    [switch]$Check  # Only show project map, skip full import analysis
)

$ErrorActionPreference = "Stop"

# --- Repo root discovery ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AngularMcp = (Resolve-Path (Join-Path $ScriptDir "../..")).Path
$PythonMaf = Join-Path (Split-Path -Parent $AngularMcp) "PythonMAFWithAzureFunctions"
if (Test-Path $PythonMaf) {
    $RepoRoot = (Resolve-Path (Join-Path $AngularMcp "..")).Path
} else {
    $RepoRoot = $AngularMcp
}

$ExcludeDirs = @("node_modules", "dist", "build", "coverage", ".angular", ".vite", ".cache", "bin", "obj", "__pycache__", ".venv", "venv")

function Write-Onboarding {
    Write-Host ""
    Write-Host "=== ORCHESTRATION FRAMEWORK — PROJECT MAP ==="
    Write-Host "Run this script from repo root when you start the project (Angular + C# + Python)."
    Write-Host "Generated: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))"
    Write-Host "Repo root: $RepoRoot"
    Write-Host ""

    # Angular
    Write-Host "--- Angular ---"
    $controlPanel = Join-Path $RepoRoot "AngularWithMCPServers\src\ControlPanel"
    if (Test-Path $controlPanel) {
        Write-Host "  App: AngularWithMCPServers\src\ControlPanel (Control Panel UI)"
        Write-Host "    Run: cd $controlPanel ; npm install ; npm start"
        Write-Host ""
    }

    # C# (.NET)
    Write-Host "--- C# / .NET ---"
    Get-ChildItem -Path $RepoRoot -Recurse -Filter "*.csproj" -File | Where-Object {
        $p = $_.FullName
        $p -notlike "*\node_modules\*" -and $p -notlike "*\.angular\*"
    } | ForEach-Object {
        $dir = $_.DirectoryName
        $name = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
        Write-Host "  Project: $name"
        Write-Host "    Path: $dir"
        Write-Host "    Run: cd $dir ; dotnet run"
        Write-Host ""
    }

    # Python
    Write-Host "--- Python ---"
    @(
        (Join-Path $RepoRoot "AngularWithMCPServers\src\Orchestration\requirements.txt"),
        (Join-Path $RepoRoot "PythonMAFWithAzureFunctions\Orchestration\requirements.txt")
    ) | Where-Object { Test-Path $_ } | ForEach-Object {
        $dir = Split-Path -Parent $_
        Write-Host "  App: $dir"
        Write-Host "    Run: cd $dir ; pip install -r requirements.txt ; func start (Azure Functions)"
        Write-Host ""
    }
    Write-Host ""
}

function Get-AngularImports {
    $root = Join-Path $RepoRoot "AngularWithMCPServers\src\ControlPanel"
    if (-not (Test-Path $root)) { return }
    $src = Join-Path $root "src"
    if (-not (Test-Path $src)) { return }

    Write-Host "=== ANGULAR (Control Panel) IMPORTS ==="
    Write-Host ""

    $tsFiles = Get-ChildItem -Path $src -Recurse -Include "*.ts","*.tsx" -File | Where-Object {
        $_.FullName -notlike "*\node_modules\*" -and $_.FullName -notlike "*\.angular\*"
    }
    $external = @{}
    $internal = @{}
    foreach ($f in $tsFiles) {
        Get-Content $f.FullName -Raw | ForEach-Object {
            $idx = 0
            while (($idx = $_.IndexOf(" from ", $idx, [StringComparison]::OrdinalIgnoreCase)) -ge 0) {
                $start = $idx + 6; $q = $null
                if ($start -lt $_.Length) {
                    $c = $_[$start]; if ($c -eq "'" -or $c -eq '"') { $q = $c; $start++ }
                }
                if ($q -and $start -lt $_.Length) {
                    $end = $_.IndexOf($q, $start)
                    if ($end -gt $start) {
                        $spec = $_.Substring($start, $end - $start)
                        if ($spec -like './*' -or $spec -like '../*') { $internal[$spec] = ($internal[$spec] + 1) } else { $pkg = ($spec -split "/")[0]; $external[$pkg] = ($external[$pkg] + 1) }
                        $idx = $end + 1
                    } else { $idx = $idx + 1 }
                } else { $idx = $idx + 1 }
            }
        }
    }
    Write-Host "--- External packages (top 25) ---"
    $external.GetEnumerator() | Sort-Object -Property Value -Descending | Select-Object -First 25 | ForEach-Object { Write-Host ("  " + $_.Value + " " + $_.Key) }
    Write-Host ""
    Write-Host "--- Internal (relative) imports ---"
    $internal.GetEnumerator() | Sort-Object -Property Value -Descending | Select-Object -First 20 | ForEach-Object { Write-Host ("  " + $_.Value + " " + $_.Key) }
    Write-Host ""
}

function Get-CSharpAnalysis {
    Write-Host "=== C# / .NET PROJECTS and NAMESPACES ==="
    Write-Host ""

    Get-ChildItem -Path $RepoRoot -Recurse -Filter "*.csproj" -File | Where-Object {
        $_.FullName -notlike "*\node_modules\*"
    } | ForEach-Object {
        $dir = $_.DirectoryName
        $name = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
        Write-Host "--- Project: $name ($dir) ---"

        $refs = @()
        Get-Content $_.FullName | ForEach-Object {
            $line = $_
            $i = $line.IndexOf("Include=`"")
            if ($i -ge 0) { $i += 9; $j = $line.IndexOf([char]34, $i); if ($j -gt $i) { $refs += $line.Substring($i, $j - $i) } }
        }
        if ($refs) {
            Write-Host "  References:"
            $refs | ForEach-Object { Write-Host ("    - " + $_) }
        }

        Write-Host "  Top namespaces (using):"
        $usingCount = @{}
        Get-ChildItem -Path $dir -Recurse -Filter "*.cs" -File | Where-Object { $_.FullName -notlike "*\bin\*" -and $_.FullName -notlike "*\obj\*" } | ForEach-Object {
            Select-String -Path $_.FullName -Pattern "^\s*using\s+" | ForEach-Object {
                $ns = ($_.Line -replace "^\s*using\s+", "" -replace ";\s*$", "").Trim()
                if ($ns) { $usingCount[$ns] = ($usingCount[$ns] + 1) }
            }
        }
        $usingCount.GetEnumerator() | Sort-Object -Property Value -Descending | Select-Object -First 15 | ForEach-Object { Write-Host ("    " + $_.Value + " " + $_.Key) }
        Write-Host ""
    }
}

function Get-PythonAnalysis {
    Write-Host "=== PYTHON IMPORTS ==="
    Write-Host ""

    @(
        (Join-Path $RepoRoot "AngularWithMCPServers\src\Orchestration"),
        (Join-Path $RepoRoot "PythonMAFWithAzureFunctions\Orchestration")
    ) | Where-Object { Test-Path $_ } | ForEach-Object {
        $pyroot = $_
        Write-Host ("--- " + $pyroot + " ---")
        $importCount = @{}
        Get-ChildItem -Path $pyroot -Recurse -Filter "*.py" -File | Where-Object {
            $_.FullName -notlike "*\__pycache__\*" -and $_.FullName -notlike "*\.venv\*" -and $_.FullName -notlike "*\venv\*"
        } | ForEach-Object {
            Get-Content $_.FullName | ForEach-Object {
                $line = $_
                if ($line -match "^\s*import\s+(\S+)") { $p = ($Matches[1] -split "\.")[0]; $importCount[$p] = ($importCount[$p] + 1) }
                elseif ($line -match "^\s*from\s+(\S+)") { $p = ($Matches[1] -split "\.")[0]; $importCount[$p] = ($importCount[$p] + 1) }
            }
        }
        $importCount.GetEnumerator() | Sort-Object -Property Value -Descending | Select-Object -First 20 | ForEach-Object { Write-Host ("  " + $_.Value + " " + $_.Key) }
        Write-Host ""
    }

    Write-Host "--- requirements.txt (declared deps) ---"
    @(
        (Join-Path $RepoRoot "AngularWithMCPServers\src\Orchestration\requirements.txt"),
        (Join-Path $RepoRoot "PythonMAFWithAzureFunctions\Orchestration\requirements.txt")
    ) | Where-Object { Test-Path $_ } | ForEach-Object {
        Write-Host ("  " + $_)
        Get-Content $_ | Where-Object { $commentPattern = [char]94 + [char]92 + [char]115 + [char]42 + [char]35; $_ -notmatch $commentPattern -and $_.Trim().Length -gt 0 } | ForEach-Object { Write-Host ([string]::new([char]32,4) + $_) }
        Write-Host ""
    }
}

# ---------- Main ----------
Write-Onboarding
if ($Check) {
    $m = -join (61,61,61,32,77,79,68,69,58,32,99,104,101,99,107,32,40,111,109,105,116,32,45,67,104,101,99,107,32,102,111,114,32,102,117,108,108,32,105,109,112,111,114,116,32,97,110,97,108,121,115,105,115,41,32,61,61,61 | ForEach-Object { [char]$_ }); Write-Host $m
    exit 0
}
Get-AngularImports
Get-CSharpAnalysis
Get-PythonAnalysis
Write-Host (-join (61,61,61,32,69,78,68,32,79,70,32,82,69,80,79,82,84,32,61,61,61 | ForEach-Object { [char]$_ }))

