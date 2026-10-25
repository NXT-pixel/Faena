# start-env.ps1 — Entry point for new developers (invokes the full Docker stack).
#
# Delegates to scripts\start-dev-environment.ps1 in the repository root. Requires Docker; no local
# .NET/Node/ABP CLI is required for the default flow (builds use containers).
#
# Usage (from anywhere; repo is detected via this script’s location under scripts):
#   .\.cursor\scripts\start-env.ps1
#   .\.cursor\scripts\start-env.ps1 -NoCache -LocalSetup
#   .\.cursor\scripts\start-env.ps1 -SkipInfra -SkipPublish
#
# See: scripts\README.md, root README.md, docker\README.md

#requires -version 5.1
param(
    [switch] $NoCache,
    [switch] $LocalSetup,
    [switch] $SkipInfra,
    [switch] $SkipPublish,
    [switch] $RegenerateAuthCert
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path
$StartScript = Join-Path $RepoRoot "scripts\start-dev-environment.ps1"
if (-not (Test-Path $StartScript)) {
    Write-Error "Could not find $StartScript. Is this a PrototypeZero repository with scripts/start-dev-environment.ps1?"
    exit 1
}
& $StartScript @PSBoundParameters

