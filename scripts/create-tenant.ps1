#Requires -Version 5.1
<#
.SYNOPSIS
    Crea un nuevo tenant en tenants/<nombre> con su contexto, reglas y carpetas aisladas.

.DESCRIPTION
    Inicializa la estructura requerida para un nuevo cliente o proyecto:
      - tenants/<nombre>/context/ (con plantillas para team, tech, learnings, etc.)
      - tenants/<nombre>/rules/ (company-standards.md)
      - tenants/<nombre>/tasks/
      - tenants/<nombre>/Proyecto/ (con .gitkeep)

.EXAMPLE
    .\scripts\create-tenant.ps1 -TenantName "fintech-corp"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string] $TenantName
)

$ErrorActionPreference = 'Stop'

$slug = $TenantName.Trim().ToLower() -replace '[^a-z0-9_-]', '-'
if (-not $slug) {
    Write-Error "El nombre del tenant no es valido."
    exit 1
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$tenantsDir = Join-Path $repoRoot 'tenants'
$tenantDir = Join-Path $tenantsDir $slug

if (Test-Path -LiteralPath $tenantDir -PathType Container) {
    Write-Warning "El tenant '$slug' ya existe en: $tenantDir"
    exit 0
}

Write-Host "Inicializando tenant '$slug' en Faena..." -ForegroundColor Cyan

# 1. Crear directorios
$contextDir = Join-Path $tenantDir 'context'
$rulesDir = Join-Path $tenantDir 'rules'
$tasksDir = Join-Path $tenantDir 'tasks'
$proyectoDir = Join-Path $tenantDir 'Proyecto'

New-Item -ItemType Directory -Path $contextDir -Force | Out-Null
New-Item -ItemType Directory -Path $rulesDir -Force | Out-Null
New-Item -ItemType Directory -Path $tasksDir -Force | Out-Null
New-Item -ItemType Directory -Path $proyectoDir -Force | Out-Null

New-Item -ItemType File -Path (Join-Path $tasksDir '.gitkeep') -Force | Out-Null
New-Item -ItemType File -Path (Join-Path $proyectoDir '.gitkeep') -Force | Out-Null

$nowIso = (Get-Date).ToString("yyyy-MM-ddTHH:mm:sszzz")

# 2. team-context.md
$teamContext = @"
# Team Context — $slug

**Tenant:** \`$slug\`  
**Fecha de Creacion:** $nowIso

---

## 1. Identidad Git Corporativa
- **Email Corporativo:** \`developer@$slug.local\` (configurar en Proyecto/<repo> con git config --local user.email)
- **Nombre:** Desarrollador Faena

## 2. Organigrama y Roles
- **Tech Lead:** [Nombre del Tech Lead] (alineacion tecnica y arquitectura)
- **QA:** [Nombre del QA] (criterios de aceptacion y testing)
- **DevOps:** [Nombre de DevOps] (secretos, pipelines y despliegue)

## 3. Protocolo de Handoff
Todo ticket debe culminar con un resumen de handoff claro para QA y DevOps.
"@
[System.IO.File]::WriteAllText((Join-Path $contextDir 'team-context.md'), $teamContext, [System.Text.Encoding]::UTF8)

# 3. tech-context.md
$techContext = @"
# Tech Context — $slug

**Tenant:** \`$slug\`

---

## 1. Stack Tecnologico Principal
- **Backend:** [Ej. .NET 8 / ASP.NET Core, Node.js, FastAPI]
- **Frontend:** [Ej. Angular 18, React, Vue]
- **Base de Datos:** [Ej. SQL Server, PostgreSQL, CosmosDB]
- **Gestores de Paquetes:** [dotnet, npm, pnpm]

## 2. Comandos de Calidad (Quality Gates de Referencia)
- **Build:** [Ej. dotnet build / npm run build]
- **Tests unitarios:** [Ej. dotnet test / npm test]
"@
[System.IO.File]::WriteAllText((Join-Path $contextDir 'tech-context.md'), $techContext, [System.Text.Encoding]::UTF8)

# 4. project-structure.md
$projStructure = @"
# Project Structure — $slug

**Tenant:** \`$slug\`

---

## Repositorios Clonados en Proyecto/
Los repositorios del cliente viven dentro de \`tenants/$slug/Proyecto/<repo>/\`.

- *(Aun no hay repositorios clonados. Clona los repositorios del cliente aqui).*
"@
[System.IO.File]::WriteAllText((Join-Path $contextDir 'project-structure.md'), $projStructure, [System.Text.Encoding]::UTF8)

# 5. learnings.md
$learnings = @"
# Continuous Memory & Learnings — $slug

**Tenant:** \`$slug\`  
Registra aqui convenciones, trampas y decisiones de diseno especificas de este tenant para acelerar tickets futuros.

---

## Convenciones y Decisiones
- *(Pendiente de primeros tickets)*
"@
[System.IO.File]::WriteAllText((Join-Path $contextDir 'learnings.md'), $learnings, [System.Text.Encoding]::UTF8)

# 6. progress.md
$progress = @"
# Project Progress — $slug

**Tenant:** \`$slug\`  
**Estado:** Inicializado y listo para recibir tickets.
"@
[System.IO.File]::WriteAllText((Join-Path $contextDir 'progress.md'), $progress, [System.Text.Encoding]::UTF8)

# 7. system-patterns.md
$patterns = @"
# System Patterns — $slug

**Tenant:** \`$slug\`  
Patrones arquitectonicos y de diseno aprobados para este tenant.
"@
[System.IO.File]::WriteAllText((Join-Path $contextDir 'system-patterns.md'), $patterns, [System.Text.Encoding]::UTF8)

# 8. company-standards.md
$standards = @"
# Company Standards — $slug

Estandares de ingenieria obligatorios para el cliente \`$slug\`.
- Convencion de ramas: \`feature/TICKET-descripcion\`
- Cobertura de pruebas minima: Requerida en cada PR (disciplina TDD)
- Prohibido quemar secretos o cadenas de conexion
"@
[System.IO.File]::WriteAllText((Join-Path $rulesDir 'company-standards.md'), $standards, [System.Text.Encoding]::UTF8)

Write-Host "[OK] Tenant '$slug' creado exitosamente en: $tenantDir" -ForegroundColor Green
Write-Host "     Contexto:  tenants/$slug/context/" -ForegroundColor Gray
Write-Host "     Proyecto:  tenants/$slug/Proyecto/" -ForegroundColor Gray
Write-Host "     Tareas:    tenants/$slug/tasks/" -ForegroundColor Gray
Write-Host ""
Write-Host "Para activarlo como tenant de trabajo predeterminado:" -ForegroundColor Yellow
Write-Host "  .\scripts\switch-tenant.cmd $slug" -ForegroundColor White
