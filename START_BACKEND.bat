@echo off
echo ===================================
echo Starting Delhi AQI Backend Server
echo ===================================
echo.

cd backend

echo Checking dependencies...
python -c "import flask, flask_cors" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    pip install flask flask-cors
)

echo.
echo Starting Flask API server...
echo Backend will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python api.py
