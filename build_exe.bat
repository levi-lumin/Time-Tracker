@echo off
echo Building Time Tracker executable...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo.
echo Creating executable...
pyinstaller --onefile --windowed --name "Time Tracker" --icon=NONE --add-data "stopwatches.json;." time_tracker.py

echo.
echo Build complete! The executable is in the 'dist' folder.
echo.
pause

