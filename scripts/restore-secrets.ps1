# ==============================================================================
# Script de Restauración de Secretos para growthhacking.PrototypeZero
# ==============================================================================
param (
    [string]$SourcePath = "C:\Users\santi\Downloads\PrototypeZero-Secrets\PrototypeZero-Secrets",
    [string]$TargetPath = "$PSScriptRoot\..\Proyecto\growthhacking.PrototypeZero"
)

Write-Host "Restaurando secretos desde: $SourcePath" -ForegroundColor Cyan
Write-Host "Hacia: $TargetPath" -ForegroundColor Cyan

if (-not (Test-Path $SourcePath)) {
    Write-Error "No se encontro el directorio de secretos en: $SourcePath"
    exit 1
}

$files = Get-ChildItem -Path $SourcePath -File -Recurse

foreach ($file in $files) {
    $relPath = $file.FullName.Substring($SourcePath.Length).TrimStart('\', '/')
    $destFile = Join-Path $TargetPath $relPath
    $destDir = Split-Path $destFile -Parent

    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    Copy-Item -Path $file.FullName -Destination $destFile -Force
    Write-Host "✔ Restaurado: $relPath" -ForegroundColor Green
}

Write-Host "`nTodos los secretos y certificados han sido aplicados exitosamente." -ForegroundColor Green
