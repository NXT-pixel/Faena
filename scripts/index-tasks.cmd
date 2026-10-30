@echo off
rem Genera tasks/INDEX.md (local, no versionado) sin pasar por la politica de ejecucion.
rem Uso: .\scripts\index-tasks.cmd
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-tasks-index.ps1" %*
exit /b %ERRORLEVEL%
