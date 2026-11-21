#Requires -Version 5.1
<#
.SYNOPSIS
    Importa la configuracion, contexto, reglas y preferencias de tenants desde tenants.local.json.

.DESCRIPTION
    Restaura los tenants completos en la carpeta tenants/ a partir de un archivo JSON exportado
    previamente. Permite clonar Faena en una nueva maquina y reanudar el trabajo inmediatamente
    sin tener que reconfigurar tenants ni subir informacion confidencial a Git.

.EXAMPLE
    .\scripts\import-tenants.ps1
    .\scripts\import-tenants.ps1 -InputFile "C:\respaldos\mis-tenants.json"
    .\scripts\import-tenants.ps1 -CloneRepos
#>
[CmdletBinding()]
param(
    [string] $InputFile,
    [switch] $CloneRepos
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$tenantsDir = Join-Path $repoRoot 'tenants'
$activeTenantFile = Join-Path $repoRoot '.active-tenant'

if (-not $InputFile) {
    $InputFile = Join-Path $repoRoot 'tenants.local.json'
}

if (-not (Test-Path -LiteralPath $InputFile -PathType Leaf)) {
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "  [ERROR] No se encontro el archivo de tenants: $InputFile" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "Coloca 'tenants.local.json' en la raiz de Faena o especifica la ruta:" -ForegroundColor Yellow
    Write-Host "  .\scripts\import-tenants.cmd -InputFile 'C:\ruta\al\archivo.json'" -ForegroundColor White
    exit 1
}

$rawJson = [System.IO.File]::ReadAllText($InputFile, [System.Text.Encoding]::UTF8)
$data = $rawJson | ConvertFrom-Json

if (-not $data.tenants -or $data.tenants.Count -eq 0) {
    Write-Host "[-] El archivo no contiene ningun tenant para importar." -ForegroundColor Yellow
    exit 0
}

if (-not (Test-Path -LiteralPath $tenantsDir)) {
    New-Item -ItemType Directory -Path $tenantsDir -Force | Out-Null
}

$importedCount = 0
$restoredSlugs = @()

foreach ($t in $data.tenants) {
    $slug = [string]$t.slug
    if (-not $slug) { continue }

    $tenantDir = Join-Path $tenantsDir $slug
    $contextDir = Join-Path $tenantDir 'context'
    $rulesDir = Join-Path $tenantDir 'rules'
    $tasksDir = Join-Path $tenantDir 'tasks'
    $proyDir = Join-Path $tenantDir 'Proyecto'

    New-Item -ItemType Directory -Path $contextDir -Force | Out-Null
    New-Item -ItemType Directory -Path $rulesDir -Force | Out-Null
    New-Item -ItemType Directory -Path $tasksDir -Force | Out-Null
    New-Item -ItemType Directory -Path $proyDir -Force | Out-Null

    function Write-FileSafe([string]$path, [string]$content) {
        if ($content) {
            [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
        }
    }

    Write-FileSafe (Join-Path $contextDir 'team-context.md') $t.team_context
    Write-FileSafe (Join-Path $contextDir 'tech-context.md') $t.tech_context
    Write-FileSafe (Join-Path $rulesDir 'company-standards.md') $t.company_standards
    Write-FileSafe (Join-Path $contextDir 'learnings.md') $t.learnings
    Write-FileSafe (Join-Path $contextDir 'project-structure.md') $t.project_structure
    Write-FileSafe (Join-Path $contextDir 'progress.md') $t.progress
    Write-FileSafe (Join-Path $contextDir 'system-patterns.md') $t.system_patterns

    # Gitkeeps
    $keepTasks = Join-Path $tasksDir '.gitkeep'
    $keepProy = Join-Path $proyDir '.gitkeep'
    if (-not (Test-Path -LiteralPath $keepTasks)) { New-Item -ItemType File -Path $keepTasks -Force | Out-Null }
    if (-not (Test-Path -LiteralPath $keepProy)) { New-Item -ItemType File -Path $keepProy -Force | Out-Null }

    # Repositories
    if ($t.repos) {
        foreach ($r in $t.repos) {
            $repoName = [string]$r.name
            $remoteUrl = [string]$r.remote_url
            if (-not $repoName) { continue }

            $repoFolder = Join-Path $proyDir $repoName
            if (-not (Test-Path -LiteralPath $repoFolder)) {
                if ($CloneRepos -and $remoteUrl) {
                    Write-Host "  -> Clonando repo $repoName desde $remoteUrl..." -ForegroundColor Cyan
                    try {
                        git clone $remoteUrl $repoFolder
                    } catch {
                        Write-Host "     [!] No se pudo clonar automaticamente. Creando carpeta vacia." -ForegroundColor Yellow
                        New-Item -ItemType Directory -Path $repoFolder -Force | Out-Null
                    }
                } else {
                    New-Item -ItemType Directory -Path $repoFolder -Force | Out-Null
                }
            }
        }
    }

    $importedCount++
    $restoredSlugs += $slug
}

# Restaurar active tenant
$activeToSet = [string]$data.active_tenant
if (-not $activeToSet -and $restoredSlugs.Count -gt 0) {
    $activeToSet = $restoredSlugs[0]
}

if ($activeToSet) {
    [System.IO.File]::WriteAllText($activeTenantFile, $activeToSet, [System.Text.Encoding]::UTF8)
}

Write-Host "============================================================" -ForegroundColor Green
Write-Host "      [OK] Configuracion de Tenants Importada con Exito     " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Archivo origen:    $InputFile" -ForegroundColor White
Write-Host "  Tenants restaurados: $importedCount ($($restoredSlugs -join ', '))" -ForegroundColor White
Write-Host "  Tenant activo:     $activeToSet" -ForegroundColor Cyan
Write-Host "------------------------------------------------------------" -ForegroundColor Green
Write-Host "Todo el contexto, reglas y preferencias estan listos." -ForegroundColor Green
Write-Host "Puedes abrir el Dashboard para comenzar a trabajar:" -ForegroundColor Yellow
Write-Host "  .\Faena-Dashboard.cmd" -ForegroundColor White
