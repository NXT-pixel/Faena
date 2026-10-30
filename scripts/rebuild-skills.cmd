@echo off
rem Regenera skills/README.md sin pasar por la politica de ejecucion de PowerShell.
rem Uso: .\scripts\rebuild-skills.cmd [-Check]
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-skills-index.ps1" %*
exit /b %ERRORLEVEL%
