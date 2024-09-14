; Inno Setup Script for Video Compressor App

[Setup]
; General information about the installation
AppName=Video Compressor
AppVersion=1.0
DefaultDirName={pf}\VideoCompressor   ; Install to Program Files\VideoCompressor
DefaultGroupName=VideoCompressor
OutputBaseFilename=VideoCompressorSetup
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\compress.exe   ; Icon used in Add/Remove Programs
; Ensure the installer is for 32-bit or 64-bit systems
ArchitecturesInstallIn64BitMode=x64

[Files]
; Main executable (the actual Python app compiled into .exe) - for --onefile PyInstaller
Source: "dist\compress.exe"; DestDir: "{app}"; Flags: ignoreversion

; Hidden additional dependencies (e.g., ffmpeg)
Source: "C:\ffmpeg\bin\ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Create a shortcut on the desktop
Name: "{userdesktop}\Video Compressor"; Filename: "{app}\compress.exe"; WorkingDir: "{app}"

; Create a shortcut in the Start Menu
Name: "{autoprograms}\Video Compressor"; Filename: "{app}\compress.exe"; WorkingDir: "{app}"

[Run]
; Run the app after installation completes (optional)
Filename: "{app}\compress.exe"; Description: "Launch Video Compressor"; Flags: nowait postinstall skipifsilent
