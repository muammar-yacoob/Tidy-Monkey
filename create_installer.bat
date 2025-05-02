@echo off
setlocal enabledelayedexpansion

mkdir ".\temp\TidyMonkey" 2>nul

for /R %%f in (*.py) do (copy "%%f" ".\temp\TidyMonkey\" >nul)

powershell -Command "Compress-Archive -Path '.\temp\TidyMonkey' -DestinationPath '.\TidyMonkeyInstaller.zip' -Force"

rmdir /S /Q ".\temp"