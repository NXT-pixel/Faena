# Launcher: normalizes smart quotes in analyze-imports.ps1 and runs it.
# Use this if you get "string is missing the terminator" when running analyze-imports.ps1 directly.
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $scriptDir "analyze-imports.ps1"
$content = [System.IO.File]::ReadAllText($scriptPath)
foreach ($code in 0x201C,0x201D,0x201E,0x201F,0x2033,0x2036) { $content = $content -replace [char]$code,[char]0x22 }
foreach ($code in 0x2018,0x2019,0x201A,0x201B) { $content = $content -replace [char]$code,[char]0x27 }
$temp = [System.IO.Path]::GetTempFileName() + ".ps1"
[System.IO.File]::WriteAllText($temp, $content)
try { & $temp @args } finally { Remove-Item $temp -ErrorAction SilentlyContinue }
