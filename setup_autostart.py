# =============================================================================
# setup_autostart.py — Register / Remove Jarvis Vision from Windows Startup
# =============================================================================
# Run once:
#     python setup_autostart.py          → installs autostart
#     python setup_autostart.py remove   → removes autostart
# =============================================================================

import os
import sys
import tempfile

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_DIR   = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT   = os.path.join(PROJECT_DIR, "main.py")
BAT_PATH      = os.path.join(PROJECT_DIR, "start_jarvis.bat")

STARTUP_DIR   = os.path.join(
    os.environ.get("APPDATA", ""),
    "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
)
SHORTCUT_PATH = os.path.join(STARTUP_DIR, "JarvisVision.lnk")


# ---------------------------------------------------------------------------
# Step 1 — Create .bat launcher
# ---------------------------------------------------------------------------

def create_bat() -> None:
    python_exe  = sys.executable
    bat_content = f'@echo off\ncd /d "{PROJECT_DIR}"\n"{python_exe}" "{MAIN_SCRIPT}"\n'
    with open(BAT_PATH, "w") as f:
        f.write(bat_content)
    print(f"  [OK]  Batch launcher created:\n        {BAT_PATH}")


# ---------------------------------------------------------------------------
# Step 2 — Create .lnk shortcut via a temp .ps1 file
#           (avoids all quoting / space issues with -Command "...")
# ---------------------------------------------------------------------------

def create_shortcut() -> None:
    if not os.path.isdir(STARTUP_DIR):
        print(f"  [ERROR]  Startup folder not found:\n           {STARTUP_DIR}")
        sys.exit(1)

    # Write a real .ps1 file — no shell escaping needed at all
    ps_lines = [
        "$ws  = New-Object -ComObject WScript.Shell",
        f'$s   = $ws.CreateShortcut("{SHORTCUT_PATH}")',
        f'$s.TargetPath      = "{BAT_PATH}"',
        f'$s.WorkingDirectory = "{PROJECT_DIR}"',
        "$s.WindowStyle      = 7",   # 7 = minimised
        '$s.Description      = "Jarvis Vision V1 autostart"',
        "$s.Save()",
    ]

    # Write to a temp file
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
        os.unlink(tmp.name)   # always clean up the temp file

    if exit_code == 0 and os.path.isfile(SHORTCUT_PATH):
        print(f"  [OK]  Startup shortcut created:\n        {SHORTCUT_PATH}")
    else:
        print(f"  [ERROR]  Shortcut creation failed (exit code {exit_code}).")
        print()
        print("  ── Manual fallback ──────────────────────────────────────────")
        print(f"  1. Open File Explorer and go to:")
        print(f"     {STARTUP_DIR}")
        print(f"  2. Copy this file into that folder:")
        print(f"     {BAT_PATH}")
        print("  That's all — Windows will run the .bat on every login.")
        print("  ─────────────────────────────────────────────────────────────")


# ---------------------------------------------------------------------------
# Remove autostart
# ---------------------------------------------------------------------------

def remove_autostart() -> None:
    removed_any = False
    for path, label in [(SHORTCUT_PATH, "startup shortcut"), (BAT_PATH, "batch launcher")]:
        if os.path.isfile(path):
            os.remove(path)
            print(f"  [OK]  Removed {label}:\n        {path}")
            removed_any = True
        else:
            print(f"  [--]  Not found: {path}")
    if not removed_any:
        print("  Nothing to remove — Jarvis autostart was not installed.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    action = sys.argv[1].lower() if len(sys.argv) > 1 else "install"
    print()

    if action == "remove":
        print("  === Removing Jarvis Vision from Windows Startup ===\n")
        remove_autostart()
    else:
        print("  === Installing Jarvis Vision to Windows Startup ===\n")
        create_bat()
        create_shortcut()
        print()
        print("  Jarvis will now launch automatically every time you log in.")
        print("  It will auto-close after 45 seconds (configurable in main.py).")
        print()
        print("  To remove autostart later, run:")
        print("      python setup_autostart.py remove")
    print()


if __name__ == "__main__":
    main()