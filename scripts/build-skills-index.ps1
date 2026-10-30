#Requires -Version 5.1
<#
.SYNOPSIS
    Regenera el catalogo de skills en skills/README.md a partir del front matter
    de cada skills/<nombre>/SKILL.md.

.DESCRIPTION
    El catalogo es derivado: nunca se edita a mano. Este script es la unica
    forma de mantenerlo al dia, y scripts/validate-faena.ps1 falla si quedo
    desactualizado.

.PARAMETER Check
    No escribe nada. Sale con codigo 1 si el catalogo esta desactualizado
    (modo CI / pre-commit).

.EXAMPLE
    .\scripts\build-skills-index.ps1

.EXAMPLE
    .\scripts\build-skills-index.ps1 -Check
#>
[CmdletBinding()]
param(
    [switch] $Check
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot 'common\SkillsCatalog.ps1')

$skillsDirectory = Join-Path $repoRoot 'skills'
$catalogPath = Join-Path $skillsDirectory 'README.md'

try {
    $changed = Update-FaenaSkillsCatalog -SkillsDirectory $skillsDirectory -CatalogPath $catalogPath -Check:$Check

    if ($Check) {
        Write-Host 'OK: el catalogo de skills esta actualizado.'
        exit 0
    }

    if ($changed) { Write-Host 'Catalogo actualizado: skills/README.md' }
    else { Write-Host 'Sin cambios: el catalogo ya estaba actualizado.' }
    exit 0
}
catch {
    Write-Host ('ERROR: ' + $_.Exception.Message)
    exit 1
}
