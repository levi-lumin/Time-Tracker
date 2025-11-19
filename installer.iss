; Inno Setup Script for Time Tracker
; This script creates an installer that:
; - Installs to Program Files
; - Creates desktop shortcut
; - Adds to Windows startup

#define AppName "Time Tracker"
#define AppVersion "1.0"
#define AppPublisher "Time Tracker"
#define AppExeName "Time Tracker.exe"

[Setup]
; App information
AppId={{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
LicenseFile=
OutputDir=dist
OutputBaseFilename=TimeTrackerSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

; UI
SetupIconFile=
WizardImageFile=
WizardSmallImageFile=

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startup"; Description: "Start {#AppName} when Windows starts"; GroupDescription: "Startup Options"; Flags: unchecked

[Files]
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Note: stopwatches.json will be created in AppData on first run

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: startup

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create AppData folder if it doesn't exist
    // (The app will create it, but we can ensure it exists)
  end;
end;

