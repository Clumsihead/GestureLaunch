# =============================================================================
# main.py — Entry Point for Jarvis Vision V1
# =============================================================================
# Run with:
#     python main.py
#
# Jarvis will auto-close after AUTO_CLOSE_SECONDS seconds.
# Press Q inside the preview window — or Ctrl+C — to quit early.
# =============================================================================

import sys
import threading
import time

import cv2

import config
from detector import GestureDetector
from launcher import launch_workspace

# ---------------------------------------------------------------------------
# Auto-close timeout (seconds)
# ---------------------------------------------------------------------------
AUTO_CLOSE_SECONDS = 45

# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

BANNER = """
=============================================
      _____    _    ______      ________
     |_   _|  / \\  |  _ \\ \\   / /  ____|
       | |   / _ \\ | |_) \\ \\ / /| |__
       | |  / ___ \\|  _ < \\ V / |  __|
      _| |_/ /   \\ \\ |_) | | |  | |____
     |_____/_/     \\_\\____/  |_|  |______|

            V I S I O N   V 1
=============================================
"""

def print_banner() -> None:
    print(BANNER)


# ---------------------------------------------------------------------------
# Workspace launch thread
# ---------------------------------------------------------------------------

def _launch_in_thread(detector: GestureDetector) -> None:
    """Launch apps in background so the preview loop is never blocked."""
    launch_workspace()
    detector.start_cooldown()


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run() -> None:
    print_banner()
    print("  Initializing camera...")

    try:
        detector = GestureDetector()
    except RuntimeError as exc:
        print(str(exc))
        sys.exit(1)

    print("  Camera Ready.")
    print(f"  Waiting for thumbs up...  (auto-closing in {AUTO_CLOSE_SECONDS}s)")
    print(f"  Press Q in the preview window to quit early.\n")

    launch_pending = False
    start_time     = time.time()

    try:
        while True:

            # ---------------------------------------------------------------
            # Auto-close after AUTO_CLOSE_SECONDS
            # ---------------------------------------------------------------
            elapsed   = time.time() - start_time
            remaining = AUTO_CLOSE_SECONDS - elapsed

            if remaining <= 0:
                print(f"\n  [{AUTO_CLOSE_SECONDS}s elapsed]  Auto-closing Jarvis...")
                break

            gesture_fired, frame = detector.read_frame()

            if frame is None:
                time.sleep(0.05)
                continue

            # ---------------------------------------------------------------
            # Draw countdown timer in the preview window
            # ---------------------------------------------------------------
            _draw_countdown(frame, remaining)

            # ---------------------------------------------------------------
            # Gesture trigger
            # ---------------------------------------------------------------
            if gesture_fired and not launch_pending:
                print("  Gesture Detected!")
                launch_pending = True
                thread = threading.Thread(
                    target=_launch_in_thread,
                    args=(detector,),
                    daemon=True,
                )
                thread.start()

            if launch_pending and detector.in_cooldown:
                launch_pending = False

            # ---------------------------------------------------------------
            # Show preview
            # ---------------------------------------------------------------
            cv2.imshow(config.PREVIEW_WINDOW_NAME, frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q"), 27):
                print("\n  Quit signal received.  Shutting down Jarvis...")
                break

    except KeyboardInterrupt:
        print("\n  Ctrl+C detected.  Shutting down Jarvis...")

    finally:
        detector.release()
        cv2.destroyAllWindows()
        print("  Goodbye.\n")


def _draw_countdown(frame, remaining: float) -> None:
    """Draw a small countdown timer in the bottom-right of the preview."""
    import cv2
    h, w = frame.shape[:2]
    text = f"Auto-close: {remaining:.0f}s"
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.50, 1)
    x = w - tw - 14
    y = h - 55
    # Subtle dark backing
    cv2.rectangle(frame, (x - 4, y - th - 4), (x + tw + 4, y + 4),
                  config.COLOR_BLACK, -1)
    # Colour shifts red in the last 10 seconds
    color = config.COLOR_RED if remaining <= 10 else config.COLOR_WHITE
    cv2.putText(frame, text, (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, color, 1, cv2.LINE_AA)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run()