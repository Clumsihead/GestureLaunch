# 🤖 Jarvis Vision V1

A lightweight Windows desktop assistant that watches your webcam for a **👍 Thumbs Up** gesture and instantly launches your full daily workspace — no clicks, no voice, no fuss.

> Show your thumb. Watch your world open.

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9%2B-green?style=flat-square)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.30%2B-orange?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows-informational?style=flat-square&logo=windows)

---

## 📋 Table of Contents

- [What It Does](#-what-it-does)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [How to Run](#-how-to-run)
- [Autostart on Boot](#-autostart-on-boot)
- [Keyboard Shortcut](#-keyboard-shortcut-ctrlaltj)
- [How Gesture Detection Works](#-how-gesture-detection-works)
- [The Preview Window](#-the-preview-window)
- [Troubleshooting](#-troubleshooting)

---

## ✨ What It Does

| Step | What Happens |
|------|-------------|
| 1 | Jarvis starts and opens your webcam |
| 2 | It watches for a **👍 Thumbs Up** gesture |
| 3 | Gesture confirmed → workspace launches |
| 4 | Brave, ChatGPT, Claude Desktop, Spotify open |
| 5 | Jarvis auto-closes after **45 seconds** |
| 6 | Optionally auto-launches on every Windows login |
| 7 | Press **Ctrl+Alt+J** anytime to launch manually |

---

## 📁 Project Structure

```
JarvisVision/
│
├── main.py                 ← Entry point — run this
├── detector.py             ← Webcam + MediaPipe gesture logic
├── launcher.py             ← App launching + duplicate checking
├── config.py               ← ⚙️  ALL your settings live here
├── launch_workspace.bat    ← Standalone bat to open all apps
├── setup_autostart.py      ← Adds Jarvis to Windows Startup
├── setup_hotkey.py         ← Assigns Ctrl+Alt+J shortcut
├── requirements.txt        ← Python dependencies
└── README.md               ← This file
```

---

## 🖥️ Requirements

- **Windows 10 / 11**
- **Python 3.12+** → [Download](https://www.python.org/downloads/)
- **A webcam** (built-in or USB)
- The apps you want to launch already installed:
  - [Brave Browser](https://brave.com)
  - [ChatGPT Desktop](https://openai.com/chatgpt/download/)
  - [Claude Desktop](https://claude.ai/download)
  - [Spotify](https://www.spotify.com/download)

---

## 📦 Installation

### 1 — Clone the repository

```bash
git clone https://github.com/your-username/JarvisVision.git
cd JarvisVision
```

### 2 — Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3 — Install dependencies

```bash
python -m pip install -r requirements.txt
```

> **Note:** On first run, Jarvis will automatically download the MediaPipe hand landmark model (~18 MB) from Google and save it locally. This only happens once.

---

## ⚙️ Configuration

> This is the most important step. Open `config.py` and update the values to match your system before running anything.

### 🔧 Step 1 — Find your app paths

Run these commands in PowerShell to find the correct paths:

```powershell
# Find Brave
ls "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

# Find Claude Desktop AppID (if installed from Microsoft Store)
Get-StartApps | Where-Object {$_.Name -like "*Claude*"}

# Find Spotify shortcut
ls "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Spotify.lnk"
```

### 🔧 Step 2 — Edit `config.py`

Open `config.py` and change these values:

```python
# ─── Brave Browser ────────────────────────────────────────────────────────────
# Full path to brave.exe on your machine
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"


# ─── ChatGPT Desktop ──────────────────────────────────────────────────────────
# ChatGPT is a Store app — the shell command below works without a path
CHATGPT_USE_SHELL = True
CHATGPT_SHELL_CMD = "start ChatGPT"


# ─── Claude Desktop ───────────────────────────────────────────────────────────
# If Claude is installed from the Microsoft Store (UWP app):
#   1. Run in PowerShell:  Get-StartApps | Where-Object {$_.Name -like "*Claude*"}
#   2. Copy the AppID from the output (e.g. Claude_pzs8sxrjxfjjc!Claude)
#   3. Leave CLAUDE_PATH empty and set CLAUDE_USE_SHELL = True
#
CLAUDE_PATH      = ""           # leave empty for Store/UWP installs
CLAUDE_USE_SHELL = True
CLAUDE_SHELL_CMD = "start shell:AppsFolder\\Claude_pzs8sxrjxfjjc!Claude"
#                                              ^^^^^^^^^^^^^^^^^^^^^^^^
#                                              Replace with YOUR AppID


# ─── Spotify ──────────────────────────────────────────────────────────────────
# Point this to your Spotify shortcut (.lnk) or executable (.exe)
SPOTIFY_PATH = r"C:\Users\YOUR_USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Spotify.lnk"
#                       ^^^^^^^^^^^^^
#                       Replace with your Windows username


# ─── Process names (used to skip already-running apps) ────────────────────────
BRAVE_PROCESS_NAME   = "brave.exe"
CHATGPT_PROCESS_NAME = "ChatGPT.exe"
CLAUDE_PROCESS_NAME  = "claude.exe"
SPOTIFY_PROCESS_NAME = "Spotify.exe"


# ─── Camera ───────────────────────────────────────────────────────────────────
CAMERA_INDEX = 0    # 0 = default webcam. Change to 1, 2… if you have multiple.


# ─── Timing ───────────────────────────────────────────────────────────────────
COOLDOWN_SECONDS     = 15   # seconds before gesture re-arms after launching
GESTURE_CONFIRM_FRAMES = 8  # frames gesture must be held (reduces false triggers)
```

### 🔧 Step 3 — Edit `launch_workspace.bat`

Open `launch_workspace.bat` and update the two hardcoded paths:

```bat
:: Line 14 — Brave path
start "" "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

:: Line 30 — Spotify shortcut path
start "" "C:\Users\YOUR_USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Spotify.lnk"
```

Replace `YOUR_USERNAME` with your actual Windows username (same one you see in `C:\Users\`).

---

## ▶️ How to Run

```bash
# Make sure you are in the project folder
cd JarvisVision

# Activate virtual environment if you created one
venv\Scripts\activate

# Launch Jarvis
python main.py
```

You will see:

```
  Initializing camera...
  Camera Ready.
  Waiting for thumbs up...  (auto-closing in 45s)
```

A preview window opens showing your webcam feed. Hold up a **👍** and your workspace launches. Jarvis auto-closes after 45 seconds.

**To quit early:** press `Q` in the preview window or `Ctrl+C` in the terminal.

---

## 🚀 Autostart on Boot

Want Jarvis to launch automatically every time you log into Windows?

```bash
python setup_autostart.py
```

Output you should see:
```
  [OK]  Batch launcher created: ...\start_jarvis.bat
  [OK]  Startup shortcut created: ...\Startup\JarvisVision.lnk
```

**To remove autostart:**
```bash
python setup_autostart.py remove
```

---

## ⌨️ Keyboard Shortcut (Ctrl+Alt+J)

Want to launch your workspace instantly from anywhere without using the camera?

```bash
python setup_hotkey.py
```

This creates a **"Jarvis Workspace"** shortcut on your Desktop and assigns `Ctrl+Alt+J` to it globally. Press it from anywhere in Windows — even when Jarvis isn't running — to open all your apps.

> If the hotkey doesn't work immediately, log out and back in once to let Windows register it.

---

## 👁️ How Gesture Detection Works

Jarvis uses **MediaPipe Hands** to map 21 landmark points on your hand in real time. The thumbs-up check is pure geometry — no extra ML model needed.

```
Hand landmarks used:

   THUMB_TIP  (4)  ← must be above THUMB_IP and THUMB_MCP
   THUMB_IP   (3)
   THUMB_MCP  (2)

   INDEX_TIP  (8)  ← must be below INDEX_PIP   (finger folded)
   MIDDLE_TIP (12) ← must be below MIDDLE_PIP  (finger folded)
   RING_TIP   (16) ← must be below RING_PIP    (finger folded)
   PINKY_TIP  (20) ← must be below PINKY_PIP   (finger folded)
```

**Thumbs Up = thumb tip pointing up + all 4 fingers curled down**

To prevent accidental triggers, the gesture must be held for **8 consecutive frames** (~0.25 seconds). A green progress bar in the preview window shows accumulation.

### Tuning sensitivity

| Feeling | Fix |
|---------|-----|
| Triggers too easily | Increase `GESTURE_CONFIRM_FRAMES` in `config.py` |
| Hard to trigger | Decrease `GESTURE_CONFIRM_FRAMES` or `MIN_DETECTION_CONFIDENCE` |
| Detects wrong hand | Make sure only one hand is visible |

---

## 🖼️ The Preview Window

| Element | What it shows |
|---------|--------------|
| Green skeleton | MediaPipe hand landmarks drawn live |
| Bottom bar | Status: *Waiting…* / *Thumbs Up Detected!* / *Cooldown…* |
| Top-left | JARVIS V1 label |
| Top-right | Cooldown countdown (when active) |
| Bottom-right | Auto-close countdown in seconds |
| Green bar | Gesture confirmation progress |

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named 'mediapipe'` | Run `python -m pip install -r requirements.txt` |
| `Cannot open camera at index 0` | Set `CAMERA_INDEX = 1` in `config.py` |
| Wrong app opens (e.g. CLI instead of Desktop) | Check process name with Task Manager and update the path in `config.py` |
| Claude CLI opens instead of Claude Desktop | Use the UWP shell command — see [Configuration](#-configuration) |
| Gesture not detected | Ensure good lighting; keep thumb clearly pointing upward |
| Apps open twice | Check `BRAVE_PROCESS_NAME` etc. match what Task Manager shows |
| Hotkey Ctrl+Alt+J not working | Log out and back in; hotkeys need a session restart to register |
| Model download fails | Download `hand_landmarker.task` manually from [Google](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task) and place it next to `detector.py` |
| PowerShell script blocked | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell |

---

## 📄 License

MIT — do whatever you want with it.

---

*Built with Python · OpenCV · MediaPipe · psutil*
