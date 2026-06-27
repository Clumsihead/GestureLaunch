# =============================================================================
# detector.py — Gesture Detection Engine for Jarvis Vision V1
# Compatible with mediapipe 0.10.30+ (Tasks API)
# =============================================================================

import os
import sys
import urllib.request
import cv2
import mediapipe as mp
import time
from typing import Optional

import config

# ---------------------------------------------------------------------------
# Model download — the Tasks API requires a .task model file
# ---------------------------------------------------------------------------

MODEL_FILENAME = "hand_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
)

def _ensure_model() -> str:
    """
    Download the hand landmarker model if it isn't already present
    alongside this script. Returns the absolute path to the model file.
    """
    # Place the model next to detector.py
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_FILENAME)

    if not os.path.isfile(model_path):
        print(f"  [MODEL]   '{MODEL_FILENAME}' not found locally.")
        print(f"  [MODEL]   Downloading from Google storage (~18 MB)...")
        try:
            urllib.request.urlretrieve(MODEL_URL, model_path, _download_progress)
            print()  # newline after progress dots
            print(f"  [MODEL]   Saved to: {model_path}")
        except Exception as exc:
            print(f"\n  [ERROR]   Download failed: {exc}")
            print(f"            Download manually from:\n  {MODEL_URL}")
            print(f"            Place '{MODEL_FILENAME}' next to detector.py and re-run.")
            sys.exit(1)
    return model_path


def _download_progress(block_num: int, block_size: int, total_size: int) -> None:
    downloaded = block_num * block_size
    if total_size > 0:
        pct = min(downloaded / total_size * 100, 100)
        bar = int(pct / 5)
        print(f"\r  [MODEL]   [{'#' * bar:<20}] {pct:5.1f}%", end="", flush=True)


# ---------------------------------------------------------------------------
# MediaPipe Tasks API setup
# ---------------------------------------------------------------------------

from mediapipe.tasks import python as _mp_python
from mediapipe.tasks.python import vision as _mp_vision

# For drawing we use OpenCV directly — the old drawing_utils is not reliable
# in 0.10.30+.

# ---------------------------------------------------------------------------
# Landmark index constants (MediaPipe 21-point hand model — same as before)
# ---------------------------------------------------------------------------

WRIST = 0
THUMB_CMC, THUMB_MCP, THUMB_IP, THUMB_TIP       = 1,  2,  3,  4
INDEX_MCP,  INDEX_PIP,  INDEX_DIP,  INDEX_TIP    = 5,  6,  7,  8
MIDDLE_MCP, MIDDLE_PIP, MIDDLE_DIP, MIDDLE_TIP   = 9,  10, 11, 12
RING_MCP,   RING_PIP,   RING_DIP,   RING_TIP     = 13, 14, 15, 16
PINKY_MCP,  PINKY_PIP,  PINKY_DIP,  PINKY_TIP   = 17, 18, 19, 20

# MediaPipe hand connection pairs (same topology as before)
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),       # thumb
    (0,5),(5,6),(6,7),(7,8),       # index
    (0,9),(9,10),(10,11),(11,12),  # middle
    (0,13),(13,14),(14,15),(15,16),# ring
    (0,17),(17,18),(18,19),(19,20),# pinky
    (5,9),(9,13),(13,17),(5,17),   # palm
]


# ---------------------------------------------------------------------------
# Gesture logic
# ---------------------------------------------------------------------------

def _y(landmarks: list, idx: int) -> float:
    """Normalised Y coordinate (0 = top, 1 = bottom)."""
    return landmarks[idx].y


def is_finger_folded(landmarks: list, tip_idx: int, pip_idx: int) -> bool:
    """True when a finger tip is below its PIP joint (finger curled inward)."""
    return _y(landmarks, tip_idx) > _y(landmarks, pip_idx)


def is_thumb_extended(landmarks: list) -> bool:
    """True when THUMB_TIP is clearly above THUMB_IP and THUMB_MCP."""
    tip_y  = _y(landmarks, THUMB_TIP)
    ip_y   = _y(landmarks, THUMB_IP)
    mcp_y  = _y(landmarks, THUMB_MCP)
    margin = 0.04
    return (tip_y < ip_y - margin) and (tip_y < mcp_y - margin)


def is_thumbs_up(landmarks: list) -> bool:
    """
    Thumbs-up = thumb pointing upward AND all four fingers folded.
    Pure landmark geometry — no extra ML model required.
    """
    if not is_thumb_extended(landmarks):
        return False
    return (
        is_finger_folded(landmarks, INDEX_TIP,  INDEX_PIP)
        and is_finger_folded(landmarks, MIDDLE_TIP, MIDDLE_PIP)
        and is_finger_folded(landmarks, RING_TIP,   RING_PIP)
        and is_finger_folded(landmarks, PINKY_TIP,  PINKY_PIP)
    )


# ---------------------------------------------------------------------------
# Landmark drawing (pure OpenCV — no mediapipe drawing_utils dependency)
# ---------------------------------------------------------------------------

def _draw_hand(frame, landmarks: list) -> None:
    """Draw hand skeleton onto frame using OpenCV primitives."""
    h, w = frame.shape[:2]

    # Convert normalised coords to pixel coords
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

    # Draw connections
    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, pts[a], pts[b], (80, 200, 80), 2, cv2.LINE_AA)

    # Draw landmark dots
    for i, (px, py) in enumerate(pts):
        radius = 5 if i in (THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP) else 3
        cv2.circle(frame, (px, py), radius, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(frame, (px, py), radius, (0, 150, 255),   1,  cv2.LINE_AA)


# ---------------------------------------------------------------------------
# Overlay helpers
# ---------------------------------------------------------------------------

def _draw_status_bar(frame, status_text: str, color: tuple) -> None:
    h, w  = frame.shape[:2]
    bar_h = 44
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - bar_h), (w, h), config.COLOR_BLACK, -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)
    cv2.putText(frame, status_text, (14, h - 13),
                cv2.FONT_HERSHEY_SIMPLEX, 0.72, color, 2, cv2.LINE_AA)
    hint = "Q  quit"
    (tw, _), _ = cv2.getTextSize(hint, cv2.FONT_HERSHEY_SIMPLEX, 0.48, 1)
    cv2.putText(frame, hint, (w - tw - 14, h - 13),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, config.COLOR_WHITE, 1, cv2.LINE_AA)


def _draw_title(frame) -> None:
    cv2.putText(frame, "JARVIS  V1", (12, 30),
                cv2.FONT_HERSHEY_DUPLEX, 0.80, config.COLOR_CYAN, 2, cv2.LINE_AA)


def _draw_cooldown_overlay(frame, remaining: float) -> None:
    h, w  = frame.shape[:2]
    text  = f"Cooldown  {remaining:.0f}s"
    (tw, _), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.60, 2)
    cv2.putText(frame, text, (w - tw - 12, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.60, config.COLOR_YELLOW, 2, cv2.LINE_AA)


def _draw_confirm_bar(frame, confirmed: int, required: int) -> None:
    if confirmed == 0:
        return
    h, w   = frame.shape[:2]
    bar_w  = 180
    bar_h  = 10
    x, y   = 12, h - 65
    filled = int(bar_w * confirmed / required)
    cv2.rectangle(frame, (x, y), (x + bar_w, y + bar_h), config.COLOR_WHITE, 1)
    cv2.rectangle(frame, (x, y), (x + filled, y + bar_h), config.COLOR_GREEN, -1)


# ---------------------------------------------------------------------------
# Main detector class
# ---------------------------------------------------------------------------

class GestureDetector:
    """
    Owns the webcam and MediaPipe HandLandmarker session (Tasks API).
    Call read_frame() each loop iteration.
    """

    def __init__(self) -> None:
        self._cap:            Optional[cv2.VideoCapture]              = None
        self._landmarker:     Optional[_mp_vision.HandLandmarker]     = None
        self._confirm_count:  int   = 0
        self._cooldown_until: float = 0.0

        self._init_camera()
        self._init_mediapipe()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _init_camera(self) -> None:
        cap = cv2.VideoCapture(config.CAMERA_INDEX)
        if not cap.isOpened():
            raise RuntimeError(
                f"[ERROR] Cannot open camera at index {config.CAMERA_INDEX}.\n"
                "        Make sure your webcam is connected and not used by another app."
            )
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  config.CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS,          config.CAMERA_FPS)
        self._cap = cap

    def _init_mediapipe(self) -> None:
        model_path = _ensure_model()

        base_options = _mp_python.BaseOptions(model_asset_path=model_path)
        options = _mp_vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=_mp_vision.RunningMode.IMAGE,
            num_hands=1,
            min_hand_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
        )
        self._landmarker = _mp_vision.HandLandmarker.create_from_options(options)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start_cooldown(self) -> None:
        self._cooldown_until = time.time() + config.COOLDOWN_SECONDS
        self._confirm_count  = 0

    @property
    def in_cooldown(self) -> bool:
        return time.time() < self._cooldown_until

    @property
    def cooldown_remaining(self) -> float:
        return max(0.0, self._cooldown_until - time.time())

    def read_frame(self):
        """
        Capture one frame, run detection, draw overlays.

        Returns (gesture_fired: bool, frame: np.ndarray | None).
        gesture_fired is True for exactly one frame when thumbs-up is confirmed.
        """
        ret, frame = self._cap.read()
        if not ret or frame is None:
            return False, None

        frame         = cv2.flip(frame, 1)   # mirror for natural feel
        gesture_fired = False

        if self.in_cooldown:
            status_text  = "  Cooldown - resuming soon"
            status_color = config.COLOR_YELLOW
            _draw_cooldown_overlay(frame, self.cooldown_remaining)

        else:
            # Convert BGR → RGB and wrap in MediaPipe Image
            rgb      = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result   = self._landmarker.detect(mp_image)

            thumbs_up_this_frame = False

            if result.hand_landmarks:
                for hand_lm in result.hand_landmarks:
                    _draw_hand(frame, hand_lm)
                    if is_thumbs_up(hand_lm):
                        thumbs_up_this_frame = True

            if thumbs_up_this_frame:
                self._confirm_count += 1
                if self._confirm_count >= config.GESTURE_CONFIRM_FRAMES:
                    gesture_fired        = True
                    self._confirm_count  = 0
                status_text  = "  Thumbs Up Detected!"
                status_color = config.COLOR_GREEN
            else:
                self._confirm_count = 0
                status_text  = "  Waiting for thumbs up..."
                status_color = config.COLOR_WHITE

            _draw_confirm_bar(frame, self._confirm_count, config.GESTURE_CONFIRM_FRAMES)

        _draw_title(frame)
        _draw_status_bar(frame, status_text, status_color)
        return gesture_fired, frame

    def release(self) -> None:
        if self._cap        is not None: self._cap.release()
        if self._landmarker is not None: self._landmarker.close()