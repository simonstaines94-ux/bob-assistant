@echo off
title BOB Assistant - Setup
color 0A
echo.
echo =============================================
echo   BOB Assistant - Installing packages...
echo =============================================
echo.
pip install pyttsx3 psutil requests
echo.
echo =============================================
echo   Done! Starting Bob...
echo =============================================
echo.
python bob_assistant.py
pause
