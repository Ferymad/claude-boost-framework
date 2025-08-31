@echo off
REM Windows-specific Installation Test for Claude Boost
REM Tests NPM and Python installation on Windows

echo 🧪 Claude Boost Windows Installation Test
echo ==========================================

set TIMESTAMP=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set LOG_DIR=test-installation\logs
set TEST_DIR=test-installation\temp_test_%TIMESTAMP%

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%TEST_DIR%" mkdir "%TEST_DIR%"

echo Platform: Windows
echo Test Directory: %TEST_DIR%
echo Log Directory: %LOG_DIR%
echo.

REM Check Node.js and npm
echo 🔍 Checking Prerequisites...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found
    echo FAIL - Node.js not found >> "%LOG_DIR%\windows_test_%TIMESTAMP%.log"
    goto :error
) else (
    for /f %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✅ Node.js %NODE_VERSION% found
    echo PASS - Node.js %NODE_VERSION% found >> "%LOG_DIR%\windows_test_%TIMESTAMP%.log"
)

npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm not found
    echo FAIL - npm not found >> "%LOG_DIR%\windows_test_%TIMESTAMP%.log"
    goto :error
) else (
    for /f %%i in ('npm --version') do set NPM_VERSION=%%i
    echo ✅ npm %NPM_VERSION% found
    echo PASS - npm %NPM_VERSION% found >> "%LOG_DIR%\windows_test_%TIMESTAMP%.log"
)

REM Check Python (optional)
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️ Python not found (fallback unavailable)
        echo WARN - Python not found >> "%LOG_DIR%\windows_test_%TIMESTAMP%.log"
        set PYTHON_AVAILABLE=false
    ) else (
        for /f %%i in ('python3 --version') do set PYTHON_VERSION=%%i
        echo ✅ %PYTHON_VERSION% found
        echo PASS - %PYTHON_VERSION% found >> "%LOG_DIR%\windows_test_%TIMESTAMP%.log"
        set PYTHON_AVAILABLE=true
        set PYTHON_CMD=python3
    )
) else (
    for /f %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo ✅ %PYTHON_VERSION% found
    echo PASS - %PYTHON_VERSION% found >> "%LOG_DIR%\windows_test_%TIMESTAMP%.log"
    set PYTHON_AVAILABLE=true
    set PYTHON_CMD=python
)

REM Test NPM package creation
echo.
echo 📦 Testing NPM Package Creation...
cd claude-boost
npm pack >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm pack failed
    echo FAIL - npm pack failed >> "..\%LOG_DIR%\windows_test_%TIMESTAMP%.log"
    cd ..
    goto :error
) else (
    for %%f in (*.tgz) do set TARBALL=%%f
    echo ✅ Package created: %TARBALL%
    echo PASS - Package created: %TARBALL% >> "..\%LOG_DIR%\windows_test_%TIMESTAMP%.log"
    move "%TARBALL%" "..\%TEST_DIR%\" >nul
)
cd ..

REM Test local installation
echo.
echo ⚙️ Testing Local Installation...
cd "%TEST_DIR%"
npm install %TARBALL% --prefix .\npm_test >npm_install.log 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm install failed
    echo FAIL - npm install failed >> "..\%LOG_DIR%\windows_test_%TIMESTAMP%.log"
    cd ..
    goto :error
) else (
    echo ✅ NPM installation completed
    echo PASS - NPM installation completed >> "..\%LOG_DIR%\windows_test_%TIMESTAMP%.log"
)

REM Test CLI binary (Windows uses .cmd files)
if exist "npm_test\claude-boost.cmd" (
    echo ✅ CLI binary found
    echo PASS - CLI binary found >> "..\%LOG_DIR%\windows_test_%TIMESTAMP%.log"
) else (
    echo ❌ CLI binary not found
    echo FAIL - CLI binary not found >> "..\%LOG_DIR%\windows_test_%TIMESTAMP%.log"
)

cd ..

REM Test Python installation if available
if "%PYTHON_AVAILABLE%"=="true" (
    echo.
    echo 🐍 Testing Python Installation...
    cd "%TEST_DIR%"
    %PYTHON_CMD% -m venv python_test_env >python_venv.log 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        echo FAIL - Failed to create virtual environment >> "..\%LOG_DIR%\windows_test_%TIMESTAMP%.log"
    ) else (
        call python_test_env\Scripts\activate.bat
        pip install ..\..\claude-boost\ >python_install.log 2>&1
        if %errorlevel% neq 0 (
            echo ❌ pip install failed
            echo FAIL - pip install failed >> "..\..\%LOG_DIR%\windows_test_%TIMESTAMP%.log"
        ) else (
            echo ✅ Python installation completed
            echo PASS - Python installation completed >> "..\..\%LOG_DIR%\windows_test_%TIMESTAMP%.log"
        )
        call deactivate >nul 2>&1
    )
    cd ..
)

REM Cleanup
echo.
echo 🧹 Cleanup...
if exist "%TEST_DIR%" rmdir /s /q "%TEST_DIR%"

echo.
echo 📊 Windows Test Summary
echo ======================
echo Results logged to: %LOG_DIR%\windows_test_%TIMESTAMP%.log
type "%LOG_DIR%\windows_test_%TIMESTAMP%.log"

REM Check if any tests failed
findstr "FAIL" "%LOG_DIR%\windows_test_%TIMESTAMP%.log" >nul
if %errorlevel% equ 0 (
    echo.
    echo ❌ Some tests failed on Windows
    exit /b 1
) else (
    echo.
    echo ✅ All Windows tests passed!
    exit /b 0
)

:error
echo.
echo ❌ Windows installation test failed
exit /b 1