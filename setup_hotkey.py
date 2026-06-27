# =============================================================================
# setup_hotkey.py — Assign Ctrl+Alt+J to launch_workspace.bat
# =============================================================================
# Run once:
#     python setup_hotkey.py
#
# Creates a shortcut on your Desktop pointing to launch_workspace.bat
# with Ctrl+Alt+J set as the global hotkey.
#
# Windows only registers shortcut hotkeys when the .lnk lives on the
# Desktop or in the Start Menu — that's why we put it on the Desktop.
# =============================================================================

import os
import sys
import tempfile

PROJECT_DIR   = os.path.dirname(os.path.abspath(__file__))
BAT_PATH      = os.path.join(PROJECT_DIR, "launch_workspace.bat")
DESKTOP       = os.path.join(os.path.expanduser("~"), "Desktop")
SHORTCUT_PATH = os.path.join(DESKTOP, "Jarvis Workspace.lnk")
HOTKEY        = "Ctrl+Alt+J"


def create_shortcut() -> None:
    if not os.path.isfile(BAT_PATH):
        print(f"  [ERROR]  Cannot find:\n           {BAT_PATH}")
        print(f"           Make sure launch_workspace.bat is in the same folder.")
        sys.exit(1)

    ps_lines = [
        "$ws = New-Object -ComObject WScript.Shell",
        f'$s  = $ws.CreateShortcut("{SHORTCUT_PATH}")',
        f'$s.TargetPath       = "{BAT_PATH}"',
        f'$s.WorkingDirectory = "{PROJECT_DIR}"',
        f'$s.Hotkey           = "{HOTKEY}"',
        "$s.WindowStyle       = 7",        # 7 = minimised (no console flash)
        '$s.Description       = "Launch Jarvis Workspace"',
        "$s.Save()",
    ]

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".ps1", delete=False, encoding="utf-8"
    )
    tmp.write("\n".join(ps_lines))
    tmp.close()

    try:
        exit_code = os.system(
            f'powershell -NoProfile -ExecutionPolicy Bypass -File "{tmp.name}"'
        )
    finally:
        os.unlink(tmp.name)

    print()
    if exit_code == 0 and os.path.isfile(SHORTCUT_PATH):
        print(f"  [OK]  Shortcut created on Desktop:")
        print(f"        {SHORTCUT_PATH}")
        print()
        print(f"  [OK]  Hotkey assigned:  Ctrl + Alt + J")
        print()
        print("  Press Ctrl+Alt+J anywhere in Windows to launch your workspace.")
        print("  (You may need to log out and back in for the hotkey to activate.)")
    else:
        print(f"  [ERROR]  Shortcut creation failed (exit code {exit_code}).")
        print()
        print("  ── Manual fallback ──────────────────────────────────────────")
        print(f"  1. Right-click launch_workspace.bat → Send to → Desktop (shortcut)")
        print(f"  2. Right-click the new Desktop shortcut → Properties")
        print(f"  3. Click in the 'Shortcut key' box and press Ctrl+Alt+J")
        print(f"  4. Click OK")
        print("  ─────────────────────────────────────────────────────────────")
    print()


if __name__ == "__main__":
    print()
    print("  === Setting up Ctrl+Alt+J hotkey for Jarvis Workspace ===")
    print()
    create_shortcut()