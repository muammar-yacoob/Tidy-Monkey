@echo off
setlocal enabledelayedexpansion

:: Delete existing zip files
if exist ".\tidy_monkey.zip" del /F ".\tidy_monkey.zip"

:: Clean up any cached Python files - more thorough cleanup
echo Cleaning up Python cache files...
for /d /r "." %%d in (__pycache__) do @if exist "%%d" (
    echo Removing: %%d
    rd /s /q "%%d"
)
for /r "." %%f in (*.pyc) do @if exist "%%f" (
    echo Removing: %%f
    del /f /q "%%f"
)

:: Ensure all needed subdirectories have an __init__.py file
for /d /r ".\src" %%i in (*) do (
    if not exist "%%i\__init__.py" (
        echo # Auto-generated file > "%%i\__init__.py"
    )
)

:: Check if manifest file exists
if not exist "blender_manifest.toml" (
    echo Error: blender_manifest.toml not found!
    exit /b 1
)

:: Attempt to uninstall existing addon first
echo Attempting to uninstall existing addon...
"%programfiles%\Blender Foundation\Blender 4.4\blender.exe" --background --python-expr "import bpy; bpy.ops.preferences.addon_disable(module='tidy_monkey'); bpy.ops.preferences.addon_remove(module='tidy_monkey')" 2>nul

:: Build the extension using Blender's command line tool
echo Building extension...
"%programfiles%\Blender Foundation\Blender 4.4\blender.exe" --background --python-expr "import bpy; bpy.ops.preferences.addon_disable(module='tidy_monkey')" --command extension build --source-dir . --output-filepath tidy_monkey.zip --valid-tags="" --verbose

if %ERRORLEVEL% NEQ 0 (
    echo Error: Extension build failed!
    exit /b 1
)

echo.
echo Package created: tidy_monkey.zip
echo.
echo Installation instructions:
echo 1. Open Blender 4.x
echo 2. Go to Edit -^> Preferences -^> Add-ons -^> Install...
echo 3. Select the tidy_monkey.zip file
echo 4. Enable the addon
echo.
pause
