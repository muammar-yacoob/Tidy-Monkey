@echo off
setlocal enabledelayedexpansion

:: Clear temporary directory
rmdir /S /Q ".\temp" 2>nul
mkdir ".\temp" 2>nul

:: Copy all files from tidy_monkey directory preserving structure
xcopy /S /E /Y ".\tidy_monkey" ".\temp\tidy_monkey\" >nul

:: Copy the root __init__.py
copy ".\__init__.py" ".\temp\" >nul

:: Copy the manifest file to root level
copy ".\blender_manifest.toml" ".\temp\" >nul

:: Delete existing zip file first
if exist ".\TidyMonkeyInstaller.zip" del /F ".\TidyMonkeyInstaller.zip"

:: Create zip with correct structure
powershell -Command "Compress-Archive -Path '.\temp\*' -DestinationPath '.\TidyMonkeyInstaller.zip' -Force"

:: Clean up
rmdir /S /Q ".\temp"

echo Package created: TidyMonkeyInstaller.zip
