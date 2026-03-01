@echo off
echo Starting StreamFlix Server...
uvicorn app.main:app --reload
pause
