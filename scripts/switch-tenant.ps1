#Requires -Version 5.1
<#
.SYNOPSIS
    Consulta o cambia el tenant activo en Faena.

.DESCRIPTION
    Sin parametros: lista todos los tenants disponibles y senala el activo.
    Con parametro: activa el tenant especificado actualizando .active-tenant.

.EXAMPLE
    .\scripts\switch-tenant.ps1
    .\scripts\switch-tenant.ps1 -TenantName "fintech-corp"
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string] $TenantName
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$tenantsDir = Join-Path $repoRoot 'tenants'
$activeTenantFile = Join-Path $repoRoot '.active-tenant'

$currentActive = $null
if (Test-Path -LiteralPath $activeTenantFile -PathType Leaf) {
    $currentActive = (Get-Content -LiteralPath $activeTenantFile -Raw).Trim()
}

# 1. Si no se pasa nombre, listar tenants
if (-not $TenantName) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "              🏢 Tenants Disponibles en Faena               " -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan

    $found = @()
    if (Test-Path -LiteralPath $tenantsDir -PathType Container) {
        $found = @(Get-ChildItem -LiteralPath $tenantsDir -Directory | Where-Object { $_.Name -notlike '.*' })
    }

    if ($found.Count -eq 0) {
        Write-Host "No se encontraron tenants en 'tenants/'." -ForegroundColor Yellow
        Write-Host "Crea uno nuevo ejecutando: .\scripts\create-tenant.cmd <nombre>" -ForegroundColor Gray
    }
    else {
        foreach ($t in $found) {
            $isCur = ($currentActive -and ($currentActive.ToLower() -eq $t.Name.ToLower()))
            $marker = if ($isCur) { " [ACTIVO] *" } else { "          " }
            $color = if ($isCur) { [ConsoleColor]::Green } else { [ConsoleColor]::White }
            Write-Host (" {0} {1}  ({2})" -f $marker, $t.Name, (Join-Path 'tenants' $t.Name)) -ForegroundColor $color
        }
    }

    Write-Host "------------------------------------------------------------" -ForegroundColor Cyan
    if ($currentActive) {
        Write-Host "Tenant actualmente seleccionado: $currentActive" -ForegroundColor Green
    } else {
        Write-Host "Tenant actualmente seleccionado: (Ninguno / Modo global por defecto)" -ForegroundColor Gray
    }
    Write-Host "Para cambiar de tenant ejecuta: .\scripts\switch-tenant.cmd <nombre>" -ForegroundColor Yellow
    exit 0
}

# 2. Activar tenant especifico
$slug = $TenantName.Trim().ToLower()
$targetTenantDir = Join-Path $tenantsDir $slug

if (-not (Test-Path -LiteralPath $targetTenantDir -PathType Container)) {
    Write-Error "El tenant '$slug' no existe en tenants/$slug.`nCrea el tenant primero con: .\scripts\create-tenant.cmd $slug"
    exit 1
}

# Guardar en .active-tenant
[System.IO.File]::WriteAllText($activeTenantFile, $slug, (New-Object System.Text.UTF8Encoding($false)))

Write-Host "============================================================" -ForegroundColor Green
Write-Host "        [OK] Tenant Activo Cambiado Exitosamente             " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Tenant:     $slug" -ForegroundColor White
Write-Host "  Ubicacion:  tenants/$slug/" -ForegroundColor Gray
Write-Host "  Contexto:   tenants/$slug/context/" -ForegroundColor Gray
Write-Host "  Proyecto:   tenants/$slug/Proyecto/" -ForegroundColor Gray
Write-Host "  Tareas:     tenants/$slug/tasks/" -ForegroundColor Gray
Write-Host "------------------------------------------------------------" -ForegroundColor Green
Write-Host "El orquestador y el Dashboard Companion ahora apuntaran a este tenant." -ForegroundColor Cyan
