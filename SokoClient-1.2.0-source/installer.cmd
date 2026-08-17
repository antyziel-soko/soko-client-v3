@echo off
setlocal
set "APPDIR=%LOCALAPPDATA%\SokoClient"
if not exist "%APPDIR%" mkdir "%APPDIR%"
copy /Y "%~dp0SokoClient.exe" "%APPDIR%\SokoClient.exe" >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$desktop=[Environment]::GetFolderPath('Desktop'); $link=(New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $desktop 'SokoClient.lnk')); $link.TargetPath=Join-Path $env:LOCALAPPDATA 'SokoClient\SokoClient.exe'; $link.WorkingDirectory=Split-Path $link.TargetPath; $link.IconLocation=$link.TargetPath; $link.Save()"
start "" "%APPDIR%\SokoClient.exe"
