@echo off
REM Finance Backend Startup Script for Windows

echo.
echo =====================================
echo  Finance Dashboard Backend
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements (if needed)
echo Checking dependencies...
pip install -q -r requirements.txt

REM Start the server
echo.
echo Starting FastAPI server on http://localhost:8000
echo.
echo Documentation available at:
echo   - Swagger UI: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
