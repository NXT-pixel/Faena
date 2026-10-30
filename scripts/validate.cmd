@echo off
rem Valida el harness sin pasar por la politica de ejecucion de PowerShell.
rem Uso: .\scripts\validate.cmd
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0validate-faena.ps1" %*
exit /b %ERRORLEVEL%
