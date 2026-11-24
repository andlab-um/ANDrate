@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
    py -3 setup_and_run.py %*
) else (
    python setup_and_run.py %*
)
if errorlevel 1 (
    echo Setup failed. Install Python 3.12 from https://www.python.org/downloads/ if needed.
    pause
    exit /b 1
)
