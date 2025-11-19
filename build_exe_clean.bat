@echo off
echo Building Time Tracker executable (clean build)...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo.
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "Time Tracker.spec" del "Time Tracker.spec"

echo.
echo Creating executable...
pyinstaller --onefile --windowed --name "Time Tracker" --icon=NONE time_tracker.py

echo.
echo Build complete! The executable is in the 'dist' folder.
echo You can now run 'Time Tracker.exe' by double-clicking it.
echo.
pause

