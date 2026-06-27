# =============================================================================
# launcher.py — Application Launcher for Jarvis Vision V1
# =============================================================================
# Responsible for:
#   • Checking whether each application is already running (via psutil)
#   • Launching applications that are not yet open
#   • Providing a clean log for each launch attempt
# =============================================================================

import os
import subprocess
import time
from typing import Optional

import psutil  # type: ignore

import config


# ---------------------------------------------------------------------------
# Process detection
# ---------------------------------------------------------------------------

def _is_process_running(process_name: str) -> bool:
    """
    Return True if any running process has the given name (case-insensitive).
    Uses psutil to iterate over the live process list.
    """
    target = process_name.lower()
    for proc in psutil.process_iter(attrs=["name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == target:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process may have died between iteration steps — skip it.
            pass
    return False


# ---------------------------------------------------------------------------
# Individual app launchers
# ---------------------------------------------------------------------------

def _launch_brave() -> None:
    """Launch Brave Browser if it is not already running."""
    label = "Brave Browser"
    if _is_process_running(config.BRAVE_PROCESS_NAME):
        print(f"  [SKIP]    {label} is already running.")
        return

    path = config.BRAVE_PATH
    if not os.path.isfile(path):
        print(f"  [ERROR]   {label} executable not found at: {path}")
        print(f"            Edit BRAVE_PATH in config.py and try again.")
        return

    try:
        subprocess.Popen([path], shell=False)
        print(f"  [LAUNCH]  {label}  ✓")
    except OSError as exc:
        print(f"  [ERROR]   Failed to launch {label}: {exc}")


def _launch_chatgpt() -> None:
    """
    Launch ChatGPT Desktop.
    Because ChatGPT is typically a UWP / store app, we use the Windows
    'start' shell command which resolves Start-Menu shortcuts correctly.
    """
    label = "ChatGPT Desktop"
    if _is_process_running(config.CHATGPT_PROCESS_NAME):
        print(f"  [SKIP]    {label} is already running.")
        return

    try:
        subprocess.Popen(config.CHATGPT_SHELL_CMD, shell=True)
        print(f"  [LAUNCH]  {label}  ✓")
    except OSError as exc:
        print(f"  [ERROR]   Failed to launch {label}: {exc}")


def _launch_claude() -> None:
    label = "Claude Desktop"
    if _is_process_running(config.CLAUDE_PROCESS_NAME):
        print(f"  [SKIP]    {label} is already running.")
        return
    try:
        subprocess.Popen(
            "start shell:AppsFolder\\Claude_pzs8sxrjxfjjc!Claude",
            shell=True
        )
        print(f"  [LAUNCH]  {label}  ✓")
    except OSError as exc:
        print(f"  [ERROR]   Failed to launch {label}: {exc}")


def _launch_spotify() -> None:
    """
    Launch Spotify.
    Spotify is typically installed as a Start-Menu shortcut (.lnk).
    We use 'start' with the shell so Windows resolves the .lnk correctly.
    """
    label = "Spotify"
    if _is_process_running(config.SPOTIFY_PROCESS_NAME):
        print(f"  [SKIP]    {label} is already running.")
        return

    path = config.SPOTIFY_PATH

    # If the path is a .lnk or a directory, use the shell 'start' command.
    use_shell_start = path.endswith(".lnk") or os.path.isdir(path)

    if use_shell_start:
        # Resolve: if it's a directory, assume Spotify.lnk lives inside it.
        if os.path.isdir(path):
            lnk = os.path.join(path, "Spotify.lnk")
        else:
            lnk = path

        if not os.path.exists(lnk):
            print(f"  [ERROR]   {label} shortcut not found at: {lnk}")
            print(f"            Edit SPOTIFY_PATH in config.py and try again.")
            return

        try:
            subprocess.Popen(f'start "" "{lnk}"', shell=True)
            print(f"  [LAUNCH]  {label}  ✓")
        except OSError as exc:
            print(f"  [ERROR]   Failed to launch {label}: {exc}")
    else:
        # Direct .exe path
        if not os.path.isfile(path):
            print(f"  [ERROR]   {label} executable not found at: {path}")
            print(f"            Edit SPOTIFY_PATH in config.py and try again.")
            return
        try:
            subprocess.Popen([path], shell=False)
            print(f"  [LAUNCH]  {label}  ✓")
        except OSError as exc:
            print(f"  [ERROR]   Failed to launch {label}: {exc}")


# ---------------------------------------------------------------------------
# Main workspace launcher — called by main.py
# ---------------------------------------------------------------------------

def launch_workspace() -> None:
    """
    Launch all workspace applications in sequence.
    Each launcher is independent; a failure in one does not stop the others.
    A small delay between launches avoids hammering the system all at once.
    """
    print()
    print("  ┌─────────────────────────────────┐")
    print("  │   Opening Workspace…             │")
    print("  └─────────────────────────────────┘")

    _launch_brave()
    time.sleep(0.6)

    _launch_chatgpt()
    time.sleep(0.6)

    _launch_claude()
    time.sleep(0.6)

    _launch_spotify()

    print()
    print(f"  Workspace launched.  Cooldown: {config.COOLDOWN_SECONDS}s")
    print()
