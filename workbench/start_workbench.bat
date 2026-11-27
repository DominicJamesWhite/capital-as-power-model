@echo off
rem Starts the workbench and opens it in the web browser. Close this window to stop it.
set "PY=%~dp0..\..\..\..\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" "%~dp0server.py"
pause
