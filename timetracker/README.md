# Time Tracker

A lightweight Windows 11 stopwatch application with a minimal, clean UI.

## Features

- **Multiple Stopwatches**: Create and manage multiple stopwatches simultaneously
- **Editable Labels**: Click on any stopwatch label to rename it
- **Start/Pause/Stop**: Full control over each stopwatch
- **Persistent Storage**: All stopwatch times are saved automatically and restored when you reopen the app
- **Lightweight**: Uses only Python's built-in tkinter library - no heavy dependencies
- **Auto-save on Close**: Running stopwatches are automatically stopped and saved when you close the app

## Requirements

- Python 3.6 or higher (for running from source)
- Windows 11 (or any OS with Python and tkinter support)

## Installation

### Option 1: Install with Installer (Recommended for Distribution)

1. **Download and install Inno Setup** (one-time setup):
   - Download from: https://jrsoftware.org/isdl.php
   - Install to default location

2. **Build the installer**:
   - Double-click `build_installer.bat`
   - This creates `TimeTrackerSetup.exe` in the `dist` folder

3. **Run the installer**:
   - Double-click `TimeTrackerSetup.exe`
   - Follow the installation wizard
   - Choose to create desktop shortcut and add to startup (optional)
   - The app will be installed to `C:\Program Files\Time Tracker\`
   - Data is saved to `%APPDATA%\Time Tracker\` (user-specific)

### Option 2: Run as Portable Executable

1. **Build the executable** (one-time setup):
   - Double-click `build_exe_clean.bat`
   - Or follow instructions in `BUILD_INSTRUCTIONS.md`

2. **Run the app**:
   - Find `Time Tracker.exe` in the `dist` folder
   - Double-click to run (no Python needed!)
   - Data is saved in the same folder as the executable

### Option 3: Run from Source

1. Ensure Python is installed on your system
2. No additional packages needed - uses only Python standard library
3. Run the application:
   ```
   python time_tracker.py
   ```

## Usage

1. **Add a stopwatch**: Click the "+" button in the top right corner

2. **Rename a stopwatch**: Click on the label text and type a new name, then press Enter or click away

3. **Start/Pause**: Click the "Start" button to begin or resume a stopwatch. The button changes to "Pause" when running

4. **Stop**: Click the "Stop" button to pause the stopwatch at its current time

5. **Remove**: Click the "×" button on any stopwatch to remove it

6. **Close**: Simply close the window - all stopwatch states are automatically saved

## Data Storage

Stopwatch data is stored in `stopwatches.json`:
- **Installed version**: `%APPDATA%\Time Tracker\stopwatches.json` (e.g., `C:\Users\YourName\AppData\Roaming\Time Tracker\`)
- **Portable version**: Same directory as the executable
- **Source version**: Same directory as the script

This file is automatically created and updated as you use the app.

## Notes

- The app automatically saves your stopwatch states every time you make a change
- When you close the app, all running stopwatches are stopped and saved to prevent lost time
- When you reopen the app, all stopwatches are restored but start in a paused state

