#Requires -Version 5.1
<#
    Logica compartida del catalogo de skills de Faena.

    La usan:
      scripts/build-skills-index.ps1   escribe  skills/README.md
      scripts/validate-faena.ps1       verifica que el catalogo este al dia

    Una skill es una carpeta directa bajo skills/ que contiene un archivo
    SKILL.md (extension sin distinguir mayusculas aqui; la validacion de
    mayusculas exactas la hace validate-faena.ps1).

    Metadatos: front matter YAML con `name` y `description` obligatorios.
#>

$script:BeginMarker = '<!-- BEGIN:skills -->'
$script:EndMarker = '<!-- END:skills -->'
$script:Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Read-FaenaText {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Path
    )
    return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

function ConvertFrom-FaenaFrontMatter {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Text
    )

    $frontMatter = @{}
    $match = [regex]::Match($Text, '(?s)^---\r?\n(.*?)\r?\n---')
    if (-not $match.Success) { return $frontMatter }

    $currentKey = $null
    foreach ($line in ($match.Groups[1].Value -split "\r?\n")) {
        if ($line -match '^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$') {
            $currentKey = $matches[1].ToLowerInvariant()
            $frontMatter[$currentKey] = $matches[2].Trim()
        }
        elseif ($currentKey -and $line.Trim().Length -gt 0) {
            # Continuacion de un valor multilinea.
            $frontMatter[$currentKey] = ($frontMatter[$currentKey] + ' ' + $line.Trim()).Trim()
        }
    }

    return $frontMatter
}

function Get-FaenaSkills {
    param(
        [Parameter(Mandatory = $true)]
        [string] $SkillsDirectory
    )

    $skills = New-Object System.Collections.ArrayList
    if (-not (Test-Path -LiteralPath $SkillsDirectory -PathType Container)) { return @() }

    foreach ($directory in (Get-ChildItem -LiteralPath $SkillsDirectory -Directory | Sort-Object Name)) {
        $skillFile = Get-ChildItem -LiteralPath $directory.FullName -File |
            Where-Object { $_.Name -ieq 'SKILL.md' } |
            Select-Object -First 1
        if (-not $skillFile) { continue }

        $frontMatter = ConvertFrom-FaenaFrontMatter -Text (Read-FaenaText -Path $skillFile.FullName)

        $declaredName = ''
        if ($frontMatter.ContainsKey('name')) { $declaredName = $frontMatter['name'] }

        $description = ''
        if ($frontMatter.ContainsKey('description')) { $description = $frontMatter['description'] }
        $description = ($description -replace '\r?\n', ' ') -replace '\s{2,}', ' '
        $description = $description.Trim() -replace '\|', '\|'

        [void] $skills.Add([pscustomobject] @{
            Name         = $directory.Name
            DeclaredName = $declaredName
            Description  = $description
            FileName     = $skillFile.Name
            RelativePath = 'skills/' + $directory.Name + '/' + $skillFile.Name
        })
    }

    return $skills
}

function Get-FaenaSkillsCatalogMarkdown {
    param(
        [Parameter(Mandatory = $true)]
        [string] $SkillsDirectory
    )

    $skills = @(Get-FaenaSkills -SkillsDirectory $SkillsDirectory)
    $lines = New-Object System.Collections.ArrayList

    [void] $lines.Add('_Generado por `scripts/build-skills-index.ps1`. No editar a mano._')
    [void] $lines.Add('')
    [void] $lines.Add('**' + $skills.Count + ' skills disponibles.**')
    [void] $lines.Add('')
    [void] $lines.Add('| Skill | Descripcion |')
    [void] $lines.Add('| :--- | :--- |')

    foreach ($skill in $skills) {
        $description = $skill.Description
        if (-not $description) { $description = '_(sin description en el front matter)_' }
        $row = '| [`' + $skill.Name + '`](' + $skill.Name + '/SKILL.md) | ' + $description + ' |'
        [void] $lines.Add($row)
    }

    return ($lines -join "`n")
}

function Update-FaenaSkillsCatalog {
    param(
        [Parameter(Mandatory = $true)]
        [string] $SkillsDirectory,

        [Parameter(Mandatory = $true)]
        [string] $CatalogPath,

        [switch] $Check
    )

    $block = $script:BeginMarker + "`n" +
        (Get-FaenaSkillsCatalogMarkdown -SkillsDirectory $SkillsDirectory) + "`n" +
        $script:EndMarker

    $current = ''
    if (Test-Path -LiteralPath $CatalogPath -PathType Leaf) {
        $current = Read-FaenaText -Path $CatalogPath
    }

    $currentNormalized = $current -replace "`r`n", "`n"

    $startIndex = $currentNormalized.IndexOf($script:BeginMarker)
    $endIndex = $currentNormalized.IndexOf($script:EndMarker)

    if ($startIndex -ge 0 -and $endIndex -gt $startIndex) {
        $updated = $currentNormalized.Substring(0, $startIndex) + $block +
            $currentNormalized.Substring($endIndex + $script:EndMarker.Length)
    }
    else {
        $updated = $currentNormalized.TrimEnd() + "`n`n" + $block + "`n"
    }

    if ($Check) {
        if ($currentNormalized -cne $updated) {
            throw 'El catalogo de skills esta desactualizado. Ejecuta: .\scripts\build-skills-index.ps1'
        }
        return $false
    }

    if ($currentNormalized -ceq $updated) { return $false }

    [System.IO.File]::WriteAllText($CatalogPath, $updated, $script:Utf8NoBom)
    return $true
}
