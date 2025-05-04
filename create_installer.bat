@echo off
setlocal enabledelayedexpansion

:: Clear temporary directory
rmdir /S /Q ".\temp" 2>nul
mkdir ".\temp" 2>nul

:: Copy the root files directly to temp folder
copy ".\__init__.py" ".\temp\" >nul
copy ".\blender_manifest.toml" ".\temp\" >nul

:: Copy the src directory with all subdirectories (this includes all modules)
if exist ".\src\" (
    xcopy /S /E /Y ".\src" ".\temp\src\" >nul
    echo Copied src directory with modules
) else (
    echo WARNING: src directory not found! Addon will not work correctly.
)

:: Copy icons folder if it exists
if exist ".\icons\" (
    mkdir ".\temp\icons" 2>nul
    xcopy /S /E /Y ".\icons" ".\temp\icons\" >nul
    echo Copied icons folder
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
pause
