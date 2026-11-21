@echo off
setlocal
cd /d "%~dp0\.."
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0export-tenants.ps1" %*
if errorlevel 1 (
    echo.
    echo Error al exportar los tenants.
    pause
)
endlocal
