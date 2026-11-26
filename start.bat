@echo off
cd /d "%~dp0"
where py >nul 2>&1
if errorlevel 1 (
  python -m portal
) else (
  py -3 -m portal
)
if errorlevel 1 pause
