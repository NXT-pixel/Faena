@echo off
setlocal
cd /d "%~dp0\.."
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0import-tenants.ps1" %*
if errorlevel 1 (
    echo.
    echo Error al importar los tenants.
    pause
)
endlocal
