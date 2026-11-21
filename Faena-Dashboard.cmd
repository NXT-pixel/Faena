@echo off
setlocal
cd /d "%~dp0"
title Faena Live Companion Dashboard

echo ====================================================================
echo             Iniciando Faena Live Companion Dashboard...
echo ====================================================================

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python scripts\dashboard\server.py
    goto end
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py scripts\dashboard\server.py
    goto end
)

echo [ERROR] No se encontro Python en el PATH.
echo Instala Python o ejecuta scripts\dashboard\server.py manualmente.
pause

:end
