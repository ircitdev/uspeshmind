@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Успешный Mind — 3D WebGL Сервер
echo ========================================================
echo   Успешный Mind (3D Particles and Interactive WebGL)
echo ========================================================
python server.py
if %ERRORLEVEL% NEQ 0 (
    "C:\Users\user\.local\bin\python.exe" server.py
)
pause
