#define MyAppName "Dashboard de Atenciones"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Dashboard de Atenciones"
#define MyAppExeName "DashboardAtenciones.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-47A8-9012-B3C4D5E6F701}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\DashboardAtenciones
DefaultGroupName={#MyAppName}
PrivilegesRequired=lowest
OutputDir=..\..\installer
OutputBaseFilename=DashboardAtenciones-Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "..\..\dist\DashboardAtenciones\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{userprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{userdesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el escritorio"; GroupDescription: "Accesos directos:"
