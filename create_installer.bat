@echo off
setlocal enabledelayedexpansion

:: Clear temporary directory
rmdir /S /Q ".\temp" 2>nul
mkdir ".\temp" 2>nul

:: 1. Create directory structure (use manifest file name - not blender_manifest.toml)
copy ".\blender_manifest.toml" ".\temp\manifest.toml" >nul

:: 2. Create addon directory matching the id from manifest
mkdir ".\temp\tidy_monkey" 2>nul

:: 3. Create the primary __init__.py file (must have register/unregister)
copy ".\__init__.py" ".\temp\tidy_monkey\" >nul

:: 4. Copy source files
if exist ".\src\" (
    xcopy /S /E /Y ".\src" ".\temp\tidy_monkey\src\" >nul
)

:: 5. Copy icons if they exist
if exist ".\icons\" (
    xcopy /S /E /Y ".\icons" ".\temp\tidy_monkey\icons\" >nul
)

:: Ensure all needed subdirectories have an __init__.py file
for /d /r ".\temp\tidy_monkey" %%i in (*) do (
    if not exist "%%i\__init__.py" (
        echo # Auto-generated file > "%%i\__init__.py"
    )
)

:: Delete existing zip file first
if exist ".\TidyMonkeyInstaller.zip" del /F ".\TidyMonkeyInstaller.zip"

:: Create zip with correct structure
powershell -Command "Compress-Archive -Path '.\temp\*' -DestinationPath '.\TidyMonkeyInstaller.zip' -Force"

:: Clean up
rmdir /S /Q ".\temp"

echo Package created: TidyMonkeyInstaller.zip
echo.
echo Installation instructions:
echo 1. Open Blender 4.x
echo 2. Go to Edit -^> Preferences -^> Add-ons -^> Install...
echo 3. Select the TidyMonkeyInstaller.zip file
echo 4. Enable the addon
echo.
:: pause
