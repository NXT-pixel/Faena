#Requires -Version 5.1
<#
.SYNOPSIS
    Exporta la configuracion, contexto, reglas y preferencias de todos los tenants a tenants.local.json.

.DESCRIPTION
    Genera un archivo JSON portable (ignorado por Git) que contiene la definicion completa de todos
    los tenants para poder transferirlos manualmente a otro clon de Faena sin reconfigurar nada.

.EXAMPLE
    .\scripts\export-tenants.ps1
    .\scripts\export-tenants.ps1 -OutputFile "$HOME\Desktop\mis-tenants.json"
#>
[CmdletBinding()]
param(
    [string] $OutputFile
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$tenantsDir = Join-Path $repoRoot 'tenants'
$activeTenantFile = Join-Path $repoRoot '.active-tenant'

if (-not $OutputFile) {
    $OutputFile = Join-Path $repoRoot 'tenants.local.json'
}

$activeTenant = ''
if (Test-Path -LiteralPath $activeTenantFile -PathType Leaf) {
    $activeTenant = (Get-Content -LiteralPath $activeTenantFile -Raw).Trim()
}

$tenantsList = New-Object System.Collections.ArrayList

if (Test-Path -LiteralPath $tenantsDir -PathType Container) {
    $dirs = Get-ChildItem -LiteralPath $tenantsDir -Directory | Where-Object { $_.Name -notlike '.*' }
    foreach ($d in $dirs) {
        $slug = $d.Name
        $contextDir = Join-Path $d.FullName 'context'
        $rulesDir = Join-Path $d.FullName 'rules'
        $proyDir = Join-Path $d.FullName 'Proyecto'

        function Read-Safe([string]$path) {
            if (Test-Path -LiteralPath $path -PathType Leaf) {
                return [System.IO.File]::ReadAllText($path, (New-Object System.Text.UTF8Encoding($false)))
            }
            return ''
        }

        # Scan repos in Proyecto
        $repos = @()
        if (Test-Path -LiteralPath $proyDir -PathType Container) {
            foreach ($r in (Get-ChildItem -LiteralPath $proyDir -Directory | Where-Object { $_.Name -notlike '.*' })) {
                $remoteUrl = ''
                $gitDir = Join-Path $r.FullName '.git'
                if (Test-Path -LiteralPath $gitDir) {
                    try {
                        $remoteUrl = (git -C $r.FullName remote get-url origin 2>$null)
                    } catch {}
                }
                $repos += @{
                    name = $r.Name
                    remote_url = [string]$remoteUrl
                }
            }
        }

        $adrsDir = Join-Path $contextDir 'adrs'
        $adrs = @()
        if (Test-Path -LiteralPath $adrsDir -PathType Container) {
            foreach ($af in (Get-ChildItem -LiteralPath $adrsDir -File -Filter '*.md' | Sort-Object Name)) {
                $adrs += @{
                    filename = $af.Name
                    content = (Read-Safe $af.FullName)
                }
            }
        }

        $tenantObj = @{
            slug = $slug
            name = ($slug -replace '-', ' ')
            team_context = (Read-Safe (Join-Path $contextDir 'team-context.md'))
            tech_context = (Read-Safe (Join-Path $contextDir 'tech-context.md'))
            company_standards = (Read-Safe (Join-Path $rulesDir 'company-standards.md'))
            learnings = (Read-Safe (Join-Path $contextDir 'learnings.md'))
            project_structure = (Read-Safe (Join-Path $contextDir 'project-structure.md'))
            progress = (Read-Safe (Join-Path $contextDir 'progress.md'))
            system_patterns = (Read-Safe (Join-Path $contextDir 'system-patterns.md'))
            adrs = $adrs
            repos = $repos
        }

        [void]$tenantsList.Add($tenantObj)
    }
}

$payload = @{
    version = "1.0"
    exported_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:sszzz")
    active_tenant = $activeTenant
    tenants = $tenantsList
}

$json = ConvertTo-Json $payload -Depth 10
[System.IO.File]::WriteAllText($OutputFile, $json, (New-Object System.Text.UTF8Encoding($false)))

Write-Host "============================================================" -ForegroundColor Green
Write-Host "      [OK] Configuracion de Tenants Exportada con Exito     " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Archivo generado: $OutputFile" -ForegroundColor White
Write-Host "  Tenants guardados: $($tenantsList.Count)" -ForegroundColor White
Write-Host "  Tenant activo:    $activeTenant" -ForegroundColor Gray
Write-Host "------------------------------------------------------------" -ForegroundColor Green
Write-Host "Este archivo está excluido de Git (.gitignore)." -ForegroundColor Cyan
Write-Host "Puedes enviartelo a tu otro PC y restaurarlo con:" -ForegroundColor Yellow
Write-Host "  .\scripts\import-tenants.cmd" -ForegroundColor White
