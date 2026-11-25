#Requires -Version 5.1
<#
.SYNOPSIS
    Verifica la integridad interna del harness Faena.

.DESCRIPTION
    Siete chequeos, pensados para correr en local y en CI:

      1. skill-location   Todo SKILL.md vive en skills/<nombre>/ o skills/project/<nombre>/.
      2. skill-metadata   Cada SKILL.md tiene name y description, y name == nombre de la carpeta.
      3. skills-catalog   skills/README.md esta al dia (mismo generador que build-skills-index.ps1).
      4. rules-extension  No queda ningun .mdc fuera de .cursor/rules/.
      5. protocol-adapters  PROTOCOL.md existe y AGENTS.md, CLAUDE.md, GEMINI.md, OPENCODE.md
                          y .cursorrules lo referencian. Un adaptador que no apunta al
                          protocolo es un fork esperando a divergir.
      6. proyecto-visibility  Todo repositorio presente en Proyecto/ aparece documentado en
                          tasks/context/project-structure.md. Detecta el caso en que los
                          agentes (o una persona) operan sin saber que hay repos clonados.
      7. path-references  Toda ruta skills/|rules/|agents/|commands/|scripts/|tasks/context/
                          citada en la documentacion existe, con mayusculas exactas.
                          Solo se verifican rutas de archivo (con extension): referencias
                          a carpetas son indistinguibles de prosa como "agents/commands".
                          Los docs bajo skills/ describen el repo del cliente, asi que sus
                          rutas scripts/ no se validan contra el harness.

    Las referencias rotas historicas se listan en scripts/faena-known-refs.txt y se
    reportan como [WARN]: arreglar una referencia significa borrar su linea del archivo.
    Cualquier ruta rota que no este en esa lista hace fallar el chequeo.

.PARAMETER IncludeProyecto
    Incluye Proyecto/ en los escaneos. Por defecto se ignora, porque es codigo del cliente.

.EXAMPLE
    .\scripts\validate-faena.ps1

.EXAMPLE
    .\scripts\validate-faena.ps1 -IncludeProyecto
#>
[CmdletBinding()]
param(
    [switch] $IncludeProyecto
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$knownRefsPath = Join-Path $PSScriptRoot 'faena-known-refs.txt'
$skillsDirectory = Join-Path $repoRoot 'skills'
$catalogPath = Join-Path $skillsDirectory 'README.md'

. (Join-Path $PSScriptRoot 'common\SkillsCatalog.ps1')

$script:Results = New-Object System.Collections.ArrayList

function Add-CheckResult {
    param(
        [Parameter(Mandatory = $true)] [string] $Name,
        [Parameter(Mandatory = $true)] [bool] $Ok,
        [string] $Detail = '',
        [string[]] $Lines = @()
    )
    [void] $script:Results.Add([pscustomobject] @{
        Name   = $Name
        Ok     = $Ok
        Detail = $Detail
        Lines  = $Lines
    })
}

function Get-FaenaRelativePath {
    param([Parameter(Mandatory = $true)] [string] $FullPath)
    $relative = $FullPath.Substring($repoRoot.Length).TrimStart('\', '/')
    return ($relative -replace '\\', '/')
}

function Test-FaenaPathExact {
    param([Parameter(Mandatory = $true)] [string] $RelativePath)

    $current = $repoRoot
    foreach ($segment in ($RelativePath -split '/')) {
        if (-not $segment) { continue }
        if (-not (Test-Path -LiteralPath $current -PathType Container)) { return $false }

        $matched = $null
        foreach ($entry in [System.IO.Directory]::GetFileSystemEntries($current)) {
            $leaf = [System.IO.Path]::GetFileName($entry)
            if ([string]::Equals($leaf, $segment, [System.StringComparison]::Ordinal)) {
                $matched = $entry
                break
            }
        }
        if (-not $matched) { return $false }
        $current = $matched
    }

    return (Test-Path -LiteralPath $current)
}

function Get-FaenaRepositoryFiles {
    param([string] $Filter)
    $skipProyecto = -not $IncludeProyecto

    Get-ChildItem -LiteralPath $repoRoot -Recurse -File -Filter $Filter -ErrorAction SilentlyContinue |
        Where-Object {
            $relative = Get-FaenaRelativePath $_.FullName
            if ($relative -like '.git/*') { return $false }
            if ($relative -like 'node_modules/*') { return $false }
            if ($relative -like '*/node_modules/*') { return $false }
            if ($skipProyecto -and $relative -like 'Proyecto/*') { return $false }
            return $true
        }
}

# --------------------------------------------------------------------------
# 1 + 2. Skills: ubicacion, metadata
# --------------------------------------------------------------------------

$skillFiles = @(Get-FaenaRepositoryFiles -Filter 'SKILL.md' | Where-Object { $_.Name -ieq 'SKILL.md' })
$locationProblems = New-Object System.Collections.ArrayList
$metadataProblems = New-Object System.Collections.ArrayList

foreach ($skillFile in $skillFiles) {
    $relative = Get-FaenaRelativePath $skillFile.FullName

    if (-not ($relative -match '^skills/(project/)?[^/]+/SKILL\.md$')) {
        [void] $locationProblems.Add(('fuera de lugar: {0}' -f $relative))
        continue
    }
    if ($skillFile.Name -cne 'SKILL.md') {
        [void] $locationProblems.Add(('extension con mayusculas: {0}' -f $relative))
    }

    $frontMatter = ConvertFrom-FaenaFrontMatter -Text (Read-FaenaText -Path $skillFile.FullName)
    $folder = Split-Path -Parent $skillFile.FullName
    $folderName = Split-Path -Leaf $folder

    if (-not $frontMatter.ContainsKey('name') -or -not $frontMatter['name']) {
        [void] $metadataProblems.Add(('sin `name`: {0}' -f $relative))
    }
    elseif ($frontMatter['name'] -cne $folderName) {
        [void] $metadataProblems.Add(('name "{0}" != carpeta "{1}": {2}' -f $frontMatter['name'], $folderName, $relative))
    }

    if (-not $frontMatter.ContainsKey('description') -or -not $frontMatter['description']) {
        [void] $metadataProblems.Add(('sin `description`: {0}' -f $relative))
    }
}

$locationOk = $locationProblems.Count -eq 0
Add-CheckResult -Name 'skill-location' -Ok $locationOk `
    -Detail ('{0} SKILL.md encontrados' -f $skillFiles.Count) `
    -Lines @($locationProblems)

$metadataOk = $metadataProblems.Count -eq 0
Add-CheckResult -Name 'skill-metadata' -Ok $metadataOk `
    -Detail ('{0} con name y description validos' -f ($skillFiles.Count - $metadataProblems.Count)) `
    -Lines @($metadataProblems)

# --------------------------------------------------------------------------
# 3. Catalogo de skills al dia
# --------------------------------------------------------------------------

try {
    [void] (Update-FaenaSkillsCatalog -SkillsDirectory $skillsDirectory -CatalogPath $catalogPath -Check)
    Add-CheckResult -Name 'skills-catalog' -Ok $true -Detail 'skills/README.md actualizado'
}
catch {
    Add-CheckResult -Name 'skills-catalog' -Ok $false -Detail $_.Exception.Message
}

# --------------------------------------------------------------------------
# 4. Sin .mdc fuera de .cursor/rules/
# --------------------------------------------------------------------------

$strayRuleFiles = @(Get-FaenaRepositoryFiles -Filter '*.mdc' |
    Where-Object { (Get-FaenaRelativePath $_.FullName) -notlike '.cursor/rules/*' } |
    ForEach-Object { Get-FaenaRelativePath $_.FullName })

Add-CheckResult -Name 'rules-extension' -Ok ($strayRuleFiles.Count -eq 0) `
    -Detail 'ningun .mdc fuera de .cursor/rules/' `
    -Lines $strayRuleFiles

# --------------------------------------------------------------------------
# 5. Protocolo unico y adaptadores
# --------------------------------------------------------------------------

$adapterNames = @('AGENTS.md', 'CLAUDE.md', 'GEMINI.md', 'OPENCODE.md', '.cursorrules')
$adapterProblems = New-Object System.Collections.ArrayList

if (-not (Test-Path -LiteralPath (Join-Path $repoRoot 'PROTOCOL.md') -PathType Leaf)) {
    [void] $adapterProblems.Add('falta PROTOCOL.md en la raiz')
}

foreach ($adapterName in $adapterNames) {
    $adapterPath = Join-Path $repoRoot $adapterName
    if (-not (Test-Path -LiteralPath $adapterPath -PathType Leaf)) {
        [void] $adapterProblems.Add(('falta el adaptador {0}' -f $adapterName))
        continue
    }

    $adapterText = Read-FaenaText -Path $adapterPath
    if ($adapterText -notmatch 'PROTOCOL\.md') {
        [void] $adapterProblems.Add(('{0} no referencia PROTOCOL.md' -f $adapterName))
    }
}

Add-CheckResult -Name 'protocol-adapters' -Ok ($adapterProblems.Count -eq 0) `
    -Detail ('{0} adaptadores apuntan al protocolo' -f $adapterNames.Count) `
    -Lines @($adapterProblems)

# --------------------------------------------------------------------------
# 6. Repositorios de Proyecto/ documentados (raiz + tenant activo si existe)
# --------------------------------------------------------------------------

$activeTenantPath = Join-Path $repoRoot '.active-tenant'
$activeTenant = ''
if (Test-Path -LiteralPath $activeTenantPath -PathType Leaf) {
    $activeTenant = (Read-FaenaText -Path $activeTenantPath).Trim()
}

$undocumented = New-Object System.Collections.ArrayList
$totalClonedCount = 0

$rootsToCheck = @(
    [pscustomobject] @{
        Label = 'Proyecto/'
        Proy  = (Join-Path $repoRoot 'Proyecto')
        Doc   = (Join-Path $repoRoot 'tasks\context\project-structure.md')
        DocLabel = 'tasks/context/project-structure.md'
    }
)

if ($activeTenant -and $activeTenant -ne 'default') {
    $tenantDir = Join-Path (Join-Path $repoRoot 'tenants') $activeTenant
    if (Test-Path -LiteralPath $tenantDir -PathType Container) {
        $rootsToCheck += [pscustomobject] @{
            Label = ('tenants/{0}/Proyecto/' -f $activeTenant)
            Proy  = (Join-Path $tenantDir 'Proyecto')
            Doc   = (Join-Path $tenantDir 'context\project-structure.md')
            DocLabel = ('tenants/{0}/context/project-structure.md' -f $activeTenant)
        }
    }
}

foreach ($scope in $rootsToCheck) {
    $clonedRepositories = @()
    if (Test-Path -LiteralPath $scope.Proy -PathType Container) {
        $clonedRepositories = @(Get-ChildItem -LiteralPath $scope.Proy -Directory |
            Where-Object { $_.Name -notlike '.*' })
    }
    $totalClonedCount += $clonedRepositories.Count

    if ($clonedRepositories.Count -gt 0) {
        $structureText = ''
        if (Test-Path -LiteralPath $scope.Doc -PathType Leaf) {
            $structureText = Read-FaenaText -Path $scope.Doc
        }
        else {
            [void] $undocumented.Add(('falta {0}' -f $scope.DocLabel))
        }

        foreach ($repository in $clonedRepositories) {
            if ($structureText -notmatch [regex]::Escape($repository.Name)) {
                [void] $undocumented.Add(('{0}{1} no aparece en {2}' -f $scope.Label, $repository.Name, $scope.DocLabel))
            }
        }
    }
}

Add-CheckResult -Name 'proyecto-visibility' -Ok ($undocumented.Count -eq 0) `
    -Detail ('{0} repositorio(s) en Proyecto/, {1} sin documentar' -f $totalClonedCount, $undocumented.Count) `
    -Lines @($undocumented)

# --------------------------------------------------------------------------
# 7. Referencias a rutas
# --------------------------------------------------------------------------

$knownRefs = @{}
if (Test-Path -LiteralPath $knownRefsPath -PathType Leaf) {
    foreach ($line in (Read-FaenaText -Path $knownRefsPath) -split "\r?\n") {
        $candidate = $line.Trim()
        if (-not $candidate -or $candidate.StartsWith('#')) { continue }
        $knownRefs[$candidate] = $true
    }
}

$pathPattern = [regex]'(?<![\w.-])((?:skills|rules|agents|commands|scripts|tasks/context)/[A-Za-z0-9_./-]+)'
$brokenRefs = @{}
$knownBrokenRefs = @{}
$scannedCount = 0

foreach ($document in @(Get-FaenaRepositoryFiles -Filter '*.md') + @(Get-FaenaRepositoryFiles -Filter '*.mdc') + @(Get-ChildItem -LiteralPath $repoRoot -File -Filter '.cursorrules' -ErrorAction SilentlyContinue)) {
    $scannedCount++
    $relative = Get-FaenaRelativePath $document.FullName
    $text = Read-FaenaText -Path $document.FullName
    $lineNumber = 0

    foreach ($sourceLine in ($text -split "\r?\n")) {
        $lineNumber++
        foreach ($match in $pathPattern.Matches($sourceLine)) {
            $candidatePath = $match.Groups[1].Value.TrimEnd('/')
            if (-not $candidatePath) { continue }

            # Ignorar prefijos de glob (`skills/abp-*/`) y plantillas.
            $afterMatch = $match.Index + $match.Length
            if ($afterMatch -lt $sourceLine.Length -and $sourceLine[$afterMatch] -eq '*') { continue }
            if ($candidatePath.EndsWith('-') -or $candidatePath.EndsWith('.')) { continue }

            # Solo rutas de archivo: "agents/commands" o "rules/docs" en prosa no son rutas.
            $lastSegment = ($candidatePath -split '/')[-1]
            if ($lastSegment -notmatch '\.') { continue }

            # Los docs de skills describen el repo del cliente, no el harness.
            if ($relative -like 'skills/*' -and $candidatePath -like 'scripts/*') { continue }

            if (Test-FaenaPathExact -RelativePath $candidatePath) { continue }

            if ($knownRefs.ContainsKey($candidatePath)) {
                if (-not $knownBrokenRefs.ContainsKey($candidatePath)) {
                    $knownBrokenRefs[$candidatePath] = ('{0}:{1}' -f $relative, $lineNumber)
                }
                continue
            }

            if (-not $brokenRefs.ContainsKey($candidatePath)) {
                $brokenRefs[$candidatePath] = New-Object System.Collections.ArrayList
            }
            $reference = '{0}:{1}' -f $relative, $lineNumber
            if (-not $brokenRefs[$candidatePath].Contains($reference)) {
                [void] $brokenRefs[$candidatePath].Add($reference)
            }
        }
    }
}

$brokenLines = New-Object System.Collections.ArrayList
foreach ($path in ($brokenRefs.Keys | Sort-Object)) {
    [void] $brokenLines.Add(('NUEVA  {0}  <- {1}' -f $path, ($brokenRefs[$path] -join ', ')))
}
foreach ($path in ($knownBrokenRefs.Keys | Sort-Object)) {
    [void] $brokenLines.Add(('CONOCIDA  {0}  <- {1}' -f $path, $knownBrokenRefs[$path]))
}

Add-CheckResult -Name 'path-references' -Ok ($brokenRefs.Count -eq 0) `
    -Detail ('{0} documentos escaneados, {1} rutas rotas nuevas, {2} conocidas' -f $scannedCount, $brokenRefs.Count, $knownBrokenRefs.Count) `
    -Lines @($brokenLines)

# --------------------------------------------------------------------------
# Reporte
# --------------------------------------------------------------------------

$failures = @($script:Results | Where-Object { -not $_.Ok })

Write-Host ''
Write-Host 'Faena harness validation' -ForegroundColor Cyan
Write-Host ('root: {0}' -f $repoRoot)
Write-Host ''

foreach ($result in $script:Results) {
    if ($result.Ok) {
        Write-Host ('[PASS] {0,-16} {1}' -f $result.Name, $result.Detail) -ForegroundColor Green
    }
    else {
        Write-Host ('[FAIL] {0,-16} {1}' -f $result.Name, $result.Detail) -ForegroundColor Red
    }
    foreach ($line in $result.Lines) {
        $color = if ($line.StartsWith('CONOCIDA')) { 'Yellow' } else { 'Red' }
        Write-Host ('       {0}' -f $line) -ForegroundColor $color
    }
}

Write-Host ''
if ($failures.Count -eq 0) {
    Write-Host 'OK: harness integro.' -ForegroundColor Green
    exit 0
}

Write-Host ('FALLARON {0} chequeo(s).' -f $failures.Count) -ForegroundColor Red
exit 1
