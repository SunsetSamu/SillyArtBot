@echo off
title Python Script Runner
color 0A

:main
cls
echo Running Python script...
C:\Python312\python.exe main.py
echo.
pause
cls
goto main