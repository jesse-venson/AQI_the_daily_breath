@echo off
echo ====================================
echo Starting Delhi AQI Frontend Server
echo ====================================
echo.

cd frontend

echo Starting HTTP server...
echo Frontend will be available at: http://localhost:8080
echo.
echo Open your browser and go to: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.

python -m http.server 8080
