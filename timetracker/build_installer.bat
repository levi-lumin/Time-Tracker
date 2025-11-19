@echo off
echo ========================================
echo Time Tracker - Installer Builder
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

REM Check if Inno Setup is installed
set "INNO_PATH="
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "INNO_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" (
    set "INNO_PATH=C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 5\ISCC.exe" (
    set "INNO_PATH=C:\Program Files\Inno Setup 5\ISCC.exe"
)

if "%INNO_PATH%"=="" (
    echo.
    echo ERROR: Inno Setup not found!
    echo.
    echo Please install Inno Setup from:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo After installing, run this script again.
    echo.
    pause
    exit /b 1
)

echo Step 1: Building executable...
echo.
if exist build rmdir /s /q build
if not exist dist mkdir dist
if exist "Time Tracker.spec" del "Time Tracker.spec"

pyinstaller --onefile --windowed --name "Time Tracker" --icon=NONE time_tracker.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to build executable!
    pause
    exit /b 1
)

echo.
echo Step 2: Creating installer...
echo.

REM Ensure dist folder exists
if not exist dist mkdir dist

REM Close any running instances of the installer
echo Checking for running installer processes...
taskkill /F /IM TimeTrackerSetup.exe 2>nul
if errorlevel 1 (
    echo No running installer found.
) else (
    echo Closed running installer.
)
timeout /t 2 /nobreak >nul

REM Try to remove old installer if it exists
if exist "dist\TimeTrackerSetup.exe" (
    echo Attempting to remove old installer...
    attrib -r "dist\TimeTrackerSetup.exe" 2>nul
    del /F /Q "dist\TimeTrackerSetup.exe" 2>nul
    if exist "dist\TimeTrackerSetup.exe" (
        echo WARNING: Could not delete old installer. It may be in use.
        echo Please close any programs using the file and try again.
        timeout /t 3 /nobreak >nul
    ) else (
        echo Old installer removed successfully.
    )
)

"%INNO_PATH%" installer.iss

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create installer!
    echo.
    echo Possible causes:
    echo - The installer file is open in another program
    echo - Windows Defender is scanning the file
    echo - Another build process is running
    echo.
    echo Try closing any programs that might be using the file and run again.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo The installer is located at:
echo dist\TimeTrackerSetup.exe
echo.
echo You can now distribute this installer to install
echo Time Tracker on any Windows computer.
echo.
pause

