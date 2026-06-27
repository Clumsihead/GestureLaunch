@echo off
:: =============================================================================
:: launch_workspace.bat — Jarvis Vision V1
:: Launches all workspace apps. Assigned to Ctrl+Alt+J via setup_hotkey.py
:: =============================================================================

:: ---- Brave Browser ----------------------------------------------------------
tasklist /FI "IMAGENAME eq brave.exe" 2>NUL | find /I "brave.exe" >NUL
if errorlevel 1 (
    start "" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    echo [LAUNCH] Brave Browser
) else (
    echo [SKIP]   Brave Browser already running
)

:: ---- ChatGPT ----------------------------------------------------------------
tasklist /FI "IMAGENAME eq ChatGPT.exe" 2>NUL | find /I "ChatGPT.exe" >NUL
if errorlevel 1 (
    start ChatGPT
    echo [LAUNCH] ChatGPT
) else (
    echo [SKIP]   ChatGPT already running
)

:: ---- Claude Desktop (UWP) ---------------------------------------------------
tasklist /FI "IMAGENAME eq claude.exe" 2>NUL | find /I "claude.exe" >NUL
if errorlevel 1 (
    start shell:AppsFolder\Claude_pzs8sxrjxfjjc!Claude
    echo [LAUNCH] Claude Desktop
) else (
    echo [SKIP]   Claude Desktop already running
)

:: ---- Spotify ----------------------------------------------------------------
tasklist /FI "IMAGENAME eq Spotify.exe" 2>NUL | find /I "Spotify.exe" >NUL
if errorlevel 1 (
    start "" "C:\Users\mihir\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Spotify.lnk"
    echo [LAUNCH] Spotify
) else (
    echo [SKIP]   Spotify already running
)

echo.
echo Done.