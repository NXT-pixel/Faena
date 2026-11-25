#Requires -Version 5.1
<#
.SYNOPSIS
    Diagnostica el entorno de Faena y explica como arreglar lo que encuentre.

.DESCRIPTION
    No modifica nada: solo mira y aconseja. Comprueba repositorio, PowerShell,
    git, politica de ejecucion, hook, catalogo de skills, repositorios clonados,
    team-context y backend TLS.

    Pensado para correr antes de pedir ayuda y para el primer dia de una
    instalacion nueva.

.PARAMETER Network
    Comprueba tambien el acceso al remoto con git ls-remote --heads origin.
    Puede tardar y requiere credenciales.

.EXAMPLE
    .\scripts\doctor.ps1

.EXAMPLE
    .\scripts\doctor.cmd -Network
#>
[CmdletBinding()]
param(
    [switch] $Network
)

$ErrorActionPreference = 'Continue'

$repoRoot = Split-Path -Parent $PSScriptRoot
$diagnostics = New-Object System.Collections.ArrayList

function Add-Diagnostic {
    param(
        [Parameter(Mandatory = $true)] [string] $Name,
        [Parameter(Mandatory = $true)] [ValidateSet('PASS', 'WARN', 'FAIL')] [string] $Status,
        [string] $Detail = '',
        [string] $Fix = ''
    )
    [void] $diagnostics.Add([pscustomobject] @{
        Name   = $Name
        Status = $Status
        Detail = $Detail
        Fix    = $Fix
    })
}

# --------------------------------------------------------------------------
# 1. Raiz del repositorio
# --------------------------------------------------------------------------
if (Test-Path -LiteralPath (Join-Path $repoRoot 'PROTOCOL.md') -PathType Leaf) {
    Add-Diagnostic -Name 'repo-root' -Status 'PASS' -Detail $repoRoot
}
else {
    Add-Diagnostic -Name 'repo-root' -Status 'FAIL' -Detail 'no encuentro PROTOCOL.md' `
        -Fix 'Ejecuta el script desde el clon de Faena.'
}

# --------------------------------------------------------------------------
# 2. PowerShell
# --------------------------------------------------------------------------
$psVersion = $PSVersionTable.PSVersion
if ($psVersion.Major -ge 7) {
    Add-Diagnostic -Name 'powershell' -Status 'PASS' -Detail ('{0}' -f $psVersion)
}
else {
    Add-Diagnostic -Name 'powershell' -Status 'PASS' -Detail ('{0} (funciona; PowerShell 7 es mas comodo)' -f $psVersion)
}

# --------------------------------------------------------------------------
# 3. Git
# --------------------------------------------------------------------------
$gitVersionRaw = (& git --version 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $gitVersionRaw) {
    Add-Diagnostic -Name 'git' -Status 'FAIL' -Detail 'git no esta instalado o no esta en PATH' `
        -Fix 'Instala Git: https://git-scm.com/downloads'
}
else {
    $versionMatch = [regex]::Match($gitVersionRaw, '(\d+)\.(\d+)')
    $major = [int] $versionMatch.Groups[1].Value
    $minor = [int] $versionMatch.Groups[2].Value
    if ($major -gt 2 -or ($major -eq 2 -and $minor -ge 30)) {
        Add-Diagnostic -Name 'git' -Status 'PASS' -Detail $gitVersionRaw
    }
    else {
        Add-Diagnostic -Name 'git' -Status 'WARN' -Detail ('{0} (se recomienda 2.30+)' -f $gitVersionRaw) `
            -Fix 'Actualiza Git.'
    }
}

# --------------------------------------------------------------------------
# 4. Politica de ejecucion (solo Windows)
# --------------------------------------------------------------------------
if ($PSVersionTable.PSEdition -eq 'Desktop' -or $IsWindows) {
    $policies = @{}
    foreach ($scope in 'CurrentUser', 'LocalMachine') {
        try { $policies[$scope] = (Get-ExecutionPolicy -Scope $scope).ToString() } catch { $policies[$scope] = 'Undefined' }
    }

    $effective = $policies['CurrentUser']
    if (-not $effective -or $effective -eq 'Undefined') { $effective = $policies['LocalMachine'] }
    if (-not $effective -or $effective -eq 'Undefined') { $effective = (Get-ExecutionPolicy).ToString() }

    $detail = ('efectiva={0} (CurrentUser={1}, LocalMachine={2})' -f $effective, $policies['CurrentUser'], $policies['LocalMachine'])
    if ($effective -eq 'Restricted' -or $effective -eq 'AllSigned') {
        Add-Diagnostic -Name 'exec-policy' -Status 'WARN' -Detail $detail `
            -Fix 'Usa los wrappers .cmd (no pasan por la politica): .\scripts\validate.cmd, .\scripts\doctor.cmd. Si el clon vino de un zip: Unblock-File .\scripts\*.ps1. O: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned'
    }
    else {
        Add-Diagnostic -Name 'exec-policy' -Status 'PASS' -Detail $detail
    }
}
else {
    Add-Diagnostic -Name 'exec-policy' -Status 'PASS' -Detail 'no aplica'
}

# --------------------------------------------------------------------------
# 5. Hook de pre-commit
# --------------------------------------------------------------------------
$hooksPath = (& git config --get core.hooksPath 2>$null)
if ($LASTEXITCODE -eq 0 -and $hooksPath) {
    Add-Diagnostic -Name 'hooks' -Status 'PASS' -Detail ('core.hooksPath = {0}' -f $hooksPath)
}
else {
    Add-Diagnostic -Name 'hooks' -Status 'WARN' -Detail 'hook de pre-commit no activado' `
        -Fix 'git config core.hooksPath .githooks'
}

# --------------------------------------------------------------------------
# 6. Catalogo de skills
# --------------------------------------------------------------------------
try {
    . (Join-Path $PSScriptRoot 'common\SkillsCatalog.ps1')
    [void] (Update-FaenaSkillsCatalog -SkillsDirectory (Join-Path $repoRoot 'skills') `
            -CatalogPath (Join-Path $repoRoot 'skills\README.md') -Check)
    Add-Diagnostic -Name 'skills-catalog' -Status 'PASS' -Detail 'skills/README.md al dia'
}
catch {
    Add-Diagnostic -Name 'skills-catalog' -Status 'FAIL' -Detail $_.Exception.Message `
        -Fix '.\scripts\rebuild-skills.cmd'
}

# --------------------------------------------------------------------------
# 7. Repositorios del cliente (resuelve segun .active-tenant si existe)
# --------------------------------------------------------------------------
$activeTenantFile = Join-Path $repoRoot '.active-tenant'
$activeTenant = ''
if (Test-Path -LiteralPath $activeTenantFile -PathType Leaf) {
    $activeTenant = (Get-Content -LiteralPath $activeTenantFile -Raw).Trim()
}

$useTenantScope = ($activeTenant -and $activeTenant -ne 'default' -and (Test-Path -LiteralPath (Join-Path (Join-Path $repoRoot 'tenants') $activeTenant) -PathType Container))
$proyectoPath = if ($useTenantScope) { Join-Path (Join-Path (Join-Path $repoRoot 'tenants') $activeTenant) 'Proyecto' } else { Join-Path $repoRoot 'Proyecto' }
$proyectoLabel = if ($useTenantScope) { "tenants/$activeTenant/Proyecto/" } else { 'Proyecto/' }

$repoDirs = @()
if (Test-Path -LiteralPath $proyectoPath -PathType Container) {
    $repoDirs = @(Get-ChildItem -LiteralPath $proyectoPath -Directory | Where-Object { $_.Name -notlike '.*' })
}
if ($repoDirs.Count -gt 0) {
    Add-Diagnostic -Name 'proyecto' -Status 'PASS' -Detail (($repoDirs | ForEach-Object { $_.Name }) -join ', ')
}
else {
    Add-Diagnostic -Name 'proyecto' -Status 'WARN' -Detail ($proyectoLabel + ' no tiene repositorios clonados') `
        -Fix ("git clone <url-del-repo> " + $proyectoLabel + "<repo>")
}

# --------------------------------------------------------------------------
# 8. team-context sin rellenar
# --------------------------------------------------------------------------
$teamContext = if ($useTenantScope) { Join-Path (Join-Path (Join-Path $repoRoot 'tenants') $activeTenant) 'context\team-context.md' } else { Join-Path $repoRoot 'tasks\context\team-context.md' }
$teamContextLabel = if ($useTenantScope) { "tenants/$activeTenant/context/team-context.md" } else { 'tasks/context/team-context.md' }
if (Test-Path -LiteralPath $teamContext -PathType Leaf) {
    $content = [System.IO.File]::ReadAllText($teamContext, [System.Text.Encoding]::UTF8)
    if ($content -match '\[Nombre|\[ej\.|\[Nombre de la Empresa') {
        Add-Diagnostic -Name 'team-context' -Status 'WARN' -Detail ($teamContextLabel + ' todavia tiene marcadores de plantilla') `
            -Fix ('Edita ' + $teamContextLabel + ': equipo, Tech Lead, QA, DevOps e identidad Git corporativa.')
    }
    else {
        Add-Diagnostic -Name 'team-context' -Status 'PASS' -Detail ('relleno (' + $teamContextLabel + ')')
    }
}
else {
    Add-Diagnostic -Name 'team-context' -Status 'FAIL' -Detail ('falta ' + $teamContextLabel) `
        -Fix 'Recuperalo con: git checkout -- tasks/context/team-context.md'
}

# --------------------------------------------------------------------------
# 9. Backend TLS / acceso al remoto
# --------------------------------------------------------------------------
$sslBackend = (& git config --get http.sslBackend 2>$null)
if ($sslBackend -eq 'schannel') {
    Add-Diagnostic -Name 'tls-backend' -Status 'WARN' -Detail 'http.sslBackend = schannel' `
        -Fix 'Si ves "schannel: AcquireCredentialsHandle failed", prueba: git -c http.sslBackend=openssl <comando>'
}
elseif ($sslBackend) {
    Add-Diagnostic -Name 'tls-backend' -Status 'PASS' -Detail ('http.sslBackend = {0}' -f $sslBackend)
}
else {
    Add-Diagnostic -Name 'tls-backend' -Status 'PASS' -Detail 'backend TLS por defecto'
}

if ($Network) {
    $remote = (& git remote 2>$null | Select-Object -First 1)
    if (-not $remote) {
        Add-Diagnostic -Name 'remote' -Status 'WARN' -Detail 'no hay remoto configurado' `
            -Fix 'git remote add origin <url>'
    }
    else {
        $null = & git ls-remote --heads $remote 2>$null
        if ($LASTEXITCODE -eq 0) {
            Add-Diagnostic -Name 'remote' -Status 'PASS' -Detail ("acceso a '{0}' OK" -f $remote)
        }
        else {
            Add-Diagnostic -Name 'remote' -Status 'FAIL' -Detail ("no puedo leer '{0}'" -f $remote) `
                -Fix 'Revisa credenciales y proxy. Si el error es de schannel: git -c http.sslBackend=openssl ls-remote --heads origin'
        }
    }
}

# --------------------------------------------------------------------------
# Reporte
# --------------------------------------------------------------------------
Write-Host ''
Write-Host 'Faena doctor' -ForegroundColor Cyan
Write-Host ('root: {0}' -f $repoRoot)
Write-Host ''

foreach ($item in $diagnostics) {
    $color = switch ($item.Status) {
        'PASS' { 'Green' }
        'WARN' { 'Yellow' }
        'FAIL' { 'Red' }
    }
    Write-Host ('[{0}] {1,-15} {2}' -f $item.Status, $item.Name, $item.Detail) -ForegroundColor $color
    if ($item.Status -ne 'PASS' -and $item.Fix) {
        Write-Host ('       -> {0}' -f $item.Fix) -ForegroundColor DarkGray
    }
}

$failures = @($diagnostics | Where-Object { $_.Status -eq 'FAIL' })
$warnings = @($diagnostics | Where-Object { $_.Status -eq 'WARN' })

Write-Host ''
if ($failures.Count -eq 0) {
    Write-Host ('OK: {0} comprobaciones, {1} aviso(s).' -f $diagnostics.Count, $warnings.Count) -ForegroundColor Green
    Write-Host 'Siguiente paso: .\scripts\validate.cmd' -ForegroundColor DarkGray
    exit 0
}

Write-Host ('FALLARON {0} comprobacion(es).' -f $failures.Count) -ForegroundColor Red
exit 1
