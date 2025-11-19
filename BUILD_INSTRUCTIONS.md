# Building Time Tracker Executable

This guide will help you create a standalone executable file that can be run by double-clicking, without needing Python installed.

## Method 1: Using the Batch Script (Easiest)

1. **Double-click** `build_exe_clean.bat`
   - This will automatically install PyInstaller if needed
   - Clean any previous builds
   - Create a new executable

2. Once complete, find `Time Tracker.exe` in the `dist` folder

3. You can move `Time Tracker.exe` anywhere you want and run it by double-clicking

## Method 2: Manual Build

1. **Install PyInstaller** (if not already installed):
   ```
   pip install pyinstaller
   ```

2. **Build the executable**:
   ```
   pyinstaller --onefile --windowed --name "Time Tracker" time_tracker.py
   ```

3. The executable will be in the `dist` folder

## Notes

- The executable will be a single `.exe` file (no installer needed)
- The first time you run it, Windows Defender might show a warning (this is normal for unsigned executables)
- The `stopwatches.json` file will be created in the same folder as the executable when you first run it
- You can delete the `build` folder and `.spec` file after building - they're only needed during the build process

## Troubleshooting

- If you get an error about tkinter, make sure Python is installed with tkinter support (usually included by default)
- If the executable is large, that's normal - it includes Python and all dependencies
- If Windows blocks the executable, right-click it → Properties → Unblock → OK

