#Requires -Version 5.1
<#
.SYNOPSIS
    Genera tasks/INDEX.md: una fila por ticket con su estado real.

.DESCRIPTION
    Lee tasks/task-*/ y cuenta artefactos y checkboxes. El resultado es local y
    NO se versiona (esta en .gitignore): el estado difiere por rama y por
    maquina, y commitearlo solo produce conflictos.

    Estado que reporta cada ticket:
      - que artefactos tiene (design, trd, test-spec, README, tareas)
      - tareas hechas / totales, segun los checkboxes de su README.md
      - fecha de ultima modificacion

    Solo ASCII a proposito: PowerShell 5.1 lee los scripts sin BOM como ANSI y
    cualquier acento terminaria escrito en el indice como mojibake.

.EXAMPLE
    .\scripts\build-tasks-index.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$tasksRoot = Join-Path $repoRoot 'tasks'
$indexPath = Join-Path $tasksRoot 'INDEX.md'

function Get-CheckboxCounts {
    param([string] $Path)

    $done = 0
    $pending = 0
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        foreach ($line in ([System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8) -split "\r?\n")) {
            if ($line -match '^\s*-\s*\[[xX]\]') { $done++ }
            elseif ($line -match '^\s*-\s*\[\s\]') { $pending++ }
        }
    }
    return [pscustomobject] @{ Done = $done; Pending = $pending }
}

$rows = New-Object System.Collections.ArrayList

if (Test-Path -LiteralPath $tasksRoot -PathType Container) {
    foreach ($directory in (Get-ChildItem -LiteralPath $tasksRoot -Directory -Filter 'task-*' | Sort-Object Name)) {
        $files = @(Get-ChildItem -LiteralPath $directory.FullName -File)

        $name = $directory.Name.Substring(5)   # sin el prefijo 'task-'
        $hasDesign = @($files | Where-Object { $_.Name -like 'design-*' }).Count -gt 0
        $hasTrd = @($files | Where-Object { $_.Name -like 'trd-*' }).Count -gt 0
        $hasSpec = @($files | Where-Object { $_.Name -like 'test-spec-*' }).Count -gt 0
        $taskFiles = @($files | Where-Object { $_.Name -match '^task\d+' })

        $counts = Get-CheckboxCounts -Path (Join-Path $directory.FullName 'README.md')
        $total = $counts.Done + $counts.Pending
        $progress = if ($total -gt 0) { '{0}/{1}' -f $counts.Done, $total } else { '-' }

        $missing = @()
        if (-not $hasDesign) { $missing += 'design' }
        if (-not $hasTrd) { $missing += 'trd' }
        if (-not $hasSpec) { $missing += 'test-spec' }
        if ($taskFiles.Count -eq 0) { $missing += 'tareas' }

        if ($missing.Count -eq 0 -and $total -gt 0 -and $counts.Pending -eq 0) { $state = 'completo' }
        elseif ($missing.Count -gt 0) { $state = 'incompleto' }
        else { $state = 'en curso' }

        [void] $rows.Add([pscustomobject] @{
            Ticket   = $name
            Estado   = $state
            Tareas   = $progress
            Archivos = $taskFiles.Count
            Falta    = if ($missing.Count -gt 0) { $missing -join ', ' } else { '-' }
            Fecha    = $directory.LastWriteTime.ToString('yyyy-MM-dd')
        })
    }
}

$lines = New-Object System.Collections.ArrayList
[void] $lines.Add('# Indice de tickets')
[void] $lines.Add('')
[void] $lines.Add('_Generado por `scripts/build-tasks-index.ps1`. Local: no se versiona._')
[void] $lines.Add('')

if ($rows.Count -eq 0) {
    [void] $lines.Add('No hay tickets en `tasks/task-*/` todavia.')
}
else {
    [void] $lines.Add(('**{0} ticket(s).**' -f $rows.Count))
    [void] $lines.Add('')
    [void] $lines.Add('| Ticket | Estado | Tareas | Archivos de tarea | Falta | Ultima modificacion |')
    [void] $lines.Add('| :--- | :--- | :--- | :--- | :--- | :--- |')
    foreach ($row in $rows) {
        [void] $lines.Add(('| [`{0}`]({0}/README.md) | {1} | {2} | {3} | {4} | {5} |' -f
            $row.Ticket, $row.Estado, $row.Tareas, $row.Archivos, $row.Falta, $row.Fecha))
    }
}

$ticketFiles = @()
$ticketsDirectory = Join-Path $tasksRoot 'tickets'
if (Test-Path -LiteralPath $ticketsDirectory -PathType Container) {
    $ticketFiles = @(Get-ChildItem -LiteralPath $ticketsDirectory -File -Filter '*.md' | Sort-Object Name)
}

[void] $lines.Add('')
[void] $lines.Add('## Tickets guardados como referencia')
[void] $lines.Add('')
if ($ticketFiles.Count -eq 0) {
    [void] $lines.Add('Ninguno.')
}
else {
    foreach ($ticket in $ticketFiles) {
        [void] $lines.Add(('- [`{0}`](tickets/{0})' -f $ticket.Name))
    }
}

[void] $lines.Add('')

$content = ($lines -join "`n")
[System.IO.File]::WriteAllText($indexPath, $content, (New-Object System.Text.UTF8Encoding($false)))

Write-Host ('Indice escrito: tasks/INDEX.md ({0} ticket(s))' -f $rows.Count) -ForegroundColor Green
