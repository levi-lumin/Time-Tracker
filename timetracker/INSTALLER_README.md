# Building the Time Tracker Installer

This guide explains how to create a professional Windows installer for Time Tracker.

## Prerequisites

1. **Python** (already installed if you're reading this)
2. **PyInstaller** (will be installed automatically)
3. **Inno Setup** - Download and install from: https://jrsoftware.org/isdl.php
   - Choose the "Inno Setup" version (free, open source)
   - During installation, make sure to install to the default location

## Building the Installer

1. **Double-click `build_installer.bat`**
   - This script will:
     - Build the executable
     - Create the installer using Inno Setup
     - Output: `dist\TimeTrackerSetup.exe`

2. **The installer will be created in the `dist` folder**

## What the Installer Does

The installer (`TimeTrackerSetup.exe`) will:

✅ **Install to Program Files**
   - Creates `C:\Program Files\Time Tracker\`
   - Installs `Time Tracker.exe` there

✅ **Create Desktop Shortcut** (optional)
   - User can choose to create a desktop shortcut during installation

✅ **Add to Startup** (optional)
   - User can choose to start Time Tracker automatically when Windows starts

✅ **Save Data to AppData**
   - Stopwatch data (`stopwatches.json`) is saved to:
     `C:\Users\[YourUsername]\AppData\Roaming\Time Tracker\`
   - This ensures the app works even though it's installed in Program Files
   - Each user has their own data

## Distributing the Installer

The `TimeTrackerSetup.exe` file can be:
- Shared with other users
- Uploaded to a website
- Distributed via email, USB drive, etc.

Users just need to:
1. Run `TimeTrackerSetup.exe`
2. Follow the installation wizard
3. Choose whether to create desktop shortcut and add to startup
4. Start using Time Tracker!

## Manual Build Steps (if batch file doesn't work)

1. Build the executable:
   ```
   pyinstaller --onefile --windowed --name "Time Tracker" time_tracker.py
   ```

2. Create the installer:
   - Open Inno Setup Compiler
   - File → Open → Select `installer.iss`
   - Build → Compile

## Troubleshooting

**"Inno Setup not found" error:**
- Make sure Inno Setup is installed to the default location
- Or edit `build_installer.bat` and update the path to `ISCC.exe`

**Installer doesn't run:**
- Right-click the installer → Run as Administrator
- The installer requires admin rights to install to Program Files

**App doesn't start on login:**
- Check if you selected the "Start when Windows starts" option during installation
- You can manually add it: Win+R → `shell:startup` → Create shortcut to `Time Tracker.exe`

