@echo off
setlocal enabledelayedexpansion

mkdir ".\temp\TidyMonkey" 2>nul
mkdir ".\temp\TidyMonkey\icons" 2>nul

for /R %%f in (*.py) do (copy "%%f" ".\temp\TidyMonkey\" >nul)

:: Copy the manifest file
copy "blender_manifest.toml" ".\temp\TidyMonkey\" >nul

:: Copy icon files (if any)
for %%f in (icons\*.*) do (copy "%%f" ".\temp\TidyMonkey\icons\" >nul 2>nul)

:: Delete existing zip file first to ensure it's completely rebuilt
if exist ".\TidyMonkeyInstaller.zip" del /F ".\TidyMonkeyInstaller.zip"

powershell -Command "Compress-Archive -Path '.\temp\TidyMonkey' -DestinationPath '.\TidyMonkeyInstaller.zip' -Force"

rmdir /S /Q ".\temp"
