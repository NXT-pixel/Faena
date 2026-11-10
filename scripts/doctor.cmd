@echo off
rem Diagnostica el entorno de Faena sin pasar por la politica de ejecucion.
rem Uso: .\scripts\doctor.cmd [-Network]
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0doctor.ps1" %*
exit /b %ERRORLEVEL%
