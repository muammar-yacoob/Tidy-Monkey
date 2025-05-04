@echo off
setlocal enabledelayedexpansion

:: Clear temporary directory
rmdir /S /Q ".\temp" 2>nul
mkdir ".\temp" 2>nul

:: Copy the root files to temp
copy ".\__init__.py" ".\temp\" >nul
copy ".\blender_manifest.toml" ".\temp\" >nul

:: Create src directory
mkdir ".\temp\src" 2>nul
copy ".\src\__init__.py" ".\temp\src\" >nul

:: Create zip with correct structure
if exist ".\TidyMonkey.zip" del /F ".\TidyMonkey.zip"
powershell -Command "Compress-Archive -Path '.\temp\*' -DestinationPath '.\TidyMonkey.zip' -Force"

:: Clean up
rmdir /S /Q ".\temp"

echo Package created: TidyMonkey.zip
echo.
echo Installation instructions:
echo 1. Open Blender 4.x
echo 2. Go to Edit -^> Preferences -^> Add-ons -^> Install...
echo 3. Select the TidyMonkey.zip file
echo 4. Enable the addon by checking the box next to it
echo.
pause 