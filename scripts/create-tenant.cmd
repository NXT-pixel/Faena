@echo off
setlocal
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0create-tenant.ps1" %*
exit /b %ERRORLEVEL%
