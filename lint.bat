@echo off
REM Linting script for TidyMonkey Blender addon (Windows)

echo 🔍 Running Python linting checks...
echo.

set errors=0

REM 1. Check Python syntax
echo 1️⃣  Checking Python syntax...
python -m py_compile __init__.py src\**\*.py 2>nul
if %errorlevel% equ 0 (
    echo ✓ Syntax check passed
) else (
    echo ✗ Syntax errors found
    python -m py_compile __init__.py src\**\*.py
    set /a errors+=1
)
echo.

REM 2. Run flake8
echo 2️⃣  Running flake8...
where flake8 >nul 2>nul
if %errorlevel% equ 0 (
    flake8 . --count --show-source --statistics
    if %errorlevel% equ 0 (
        echo ✓ Flake8 passed
    ) else (
        echo ⚠ Flake8 found issues
        set /a errors+=1
    )
) else (
    echo ⚠ flake8 not installed. Install with: pip install -r dev-requirements.txt
)
echo.

REM 3. Run pylint
echo 3️⃣  Running pylint...
where pylint >nul 2>nul
if %errorlevel% equ 0 (
    pylint __init__.py src\ --rcfile=pyproject.toml 2>nul
    if %errorlevel% equ 0 (
        echo ✓ Pylint passed
    ) else (
        echo ⚠ Pylint found issues
    )
) else (
    echo ⚠ pylint not installed. Install with: pip install -r dev-requirements.txt
)
echo.

REM 4. Run mypy
echo 4️⃣  Running mypy type checking...
where mypy >nul 2>nul
if %errorlevel% equ 0 (
    mypy src\ --config-file=pyproject.toml 2>nul
    if %errorlevel% equ 0 (
        echo ✓ Type checking passed
    ) else (
        echo ⚠ Type checking found issues
    )
) else (
    echo ⚠ mypy not installed. Install with: pip install -r dev-requirements.txt
)
echo.

REM Summary
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if %errors% equ 0 (
    echo ✓ All critical checks passed!
    exit /b 0
) else (
    echo ✗ Found %errors% critical issue(s)
    exit /b 1
)
