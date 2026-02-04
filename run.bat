@echo off
echo ===================================
echo Job Portal Application Launcher
echo ===================================
echo.

echo Checking dependencies...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo Flask is not installed. Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting the Job Portal application...
echo Access the application at: http://localhost:5000
echo.
echo Default Admin Credentials:
echo   Email: admin@jobportal.com
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo ===================================
echo.

python app.py
pause
