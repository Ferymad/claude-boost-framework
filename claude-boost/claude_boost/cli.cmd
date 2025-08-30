@echo off
REM Windows batch wrapper for Claude Code Boost
REM Handles Windows-specific Python detection

echo 🚀 Claude Code Boost v1.0.1 - Windows Compatibility Mode
echo.

REM Try py launcher first (recommended for Windows)
py --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo ✅ Using Python Launcher (py)
    py "%~dp0cli.py" %*
    goto :EOF
)

REM Try python command
python --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo ✅ Using python command
    python "%~dp0cli.py" %*
    goto :EOF
)

REM Try python3 command
python3 --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo ✅ Using python3 command
    python3 "%~dp0cli.py" %*
    goto :EOF
)

REM No Python found
echo ❌ Error: Python not found. Please install Python 3.8 or higher.
echo.
echo Installation options:
echo   1. Microsoft Store: Search for "Python" and install Python 3.11+
echo   2. Official: https://python.org/downloads
echo   3. Chocolatey: choco install python
echo   4. Scoop: scoop install python
echo.
echo After installation, run: npx claude-boost init
pause
exit /b 1