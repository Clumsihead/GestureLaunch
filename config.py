# =============================================================================
# config.py — Jarvis Vision V1 Configuration
# =============================================================================
# Edit this file to match your system paths before running the project.
# =============================================================================

# ---------------------------------------------------------------------------
# APPLICATION PATHS
# Edit these to match the actual locations on your Windows machine.
# ---------------------------------------------------------------------------

BRAVE_PATH: str = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

# ChatGPT is launched via Windows shell (Start Menu shortcut), not a path.
# Leave CHATGPT_USE_SHELL = True unless you know the direct .exe path.
CHATGPT_USE_SHELL: bool = True
CHATGPT_SHELL_CMD: str = "start ChatGPT"

CLAUDE_PATH = ""  # not used — Claude is a UWP app
CLAUDE_USE_SHELL = True
CLAUDE_SHELL_CMD = "start shell:AppsFolder\\Claude_pzs8sxrjxfjjc!Claude"

SPOTIFY_PATH: str = (
    r"C:\Users\mihir\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
    r"\Spotify.lnk"
)

# ---------------------------------------------------------------------------
# PROCESS NAMES
# Used to detect whether each application is already running.
# ---------------------------------------------------------------------------

BRAVE_PROCESS_NAME: str = "brave.exe"
CHATGPT_PROCESS_NAME: str = "ChatGPT.exe"
CLAUDE_PROCESS_NAME: str = "claude.exe"
SPOTIFY_PROCESS_NAME: str = "Spotify.exe"

# ---------------------------------------------------------------------------
# CAMERA SETTINGS
# ---------------------------------------------------------------------------

CAMERA_INDEX: int = 0          # 0 = default webcam; change if you have multiple
CAMERA_WIDTH: int = 640        # Preview window width  (pixels)
CAMERA_HEIGHT: int = 480       # Preview window height (pixels)
CAMERA_FPS: int = 30           # Target capture frame-rate

# ---------------------------------------------------------------------------
# GESTURE DETECTION SETTINGS
# ---------------------------------------------------------------------------

# How many consecutive frames the thumbs-up must be held before triggering.
# Reduces false positives. At 30 FPS, 8 frames ≈ ~0.27 seconds.
GESTURE_CONFIRM_FRAMES: int = 8

# Seconds to wait after launching apps before resuming gesture detection.
COOLDOWN_SECONDS: int = 15

# MediaPipe confidence thresholds (0.0 – 1.0)
MIN_DETECTION_CONFIDENCE: float = 0.75
MIN_TRACKING_CONFIDENCE: float = 0.75

# ---------------------------------------------------------------------------
# UI SETTINGS
# ---------------------------------------------------------------------------

PREVIEW_WINDOW_NAME: str = "Jarvis Vision V1  |  Press Q to quit"

# Overlay text colours  (BGR format used by OpenCV)
COLOR_GREEN: tuple = (0, 230, 0)
COLOR_YELLOW: tuple = (0, 220, 220)
COLOR_RED: tuple = (0, 0, 230)
COLOR_WHITE: tuple = (255, 255, 255)
COLOR_BLACK: tuple = (0, 0, 0)
COLOR_CYAN: tuple = (220, 220, 0)
