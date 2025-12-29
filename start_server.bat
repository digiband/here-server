@echo off
cd /d "%~dp0"
echo Starting Here Server...
echo Server: http://localhost:8847
echo API docs: http://localhost:8847/docs
echo Press Ctrl+C to stop.
echo.
python -m uvicorn src.api.server:app --host 0.0.0.0 --port 8847 --reload
