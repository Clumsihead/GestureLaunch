# 👋 GestureLaunch

> **Skip the clicks. Show a 👍. Launch your workspace.**

GestureLaunch is a **computer vision workspace launcher** built with **Python**, **OpenCV**, and **MediaPipe**.

Instead of manually opening your everyday applications, GestureLaunch recognizes a simple **👍 thumbs-up gesture** through your webcam and launches your configured workspace automatically.

For users who prefer a manual trigger, GestureLaunch also includes a **global keyboard shortcut** (`Ctrl + Alt + J`) that launches the exact same workspace instantly.

---

# ✨ Features

* 👍 Real-time thumbs-up gesture recognition
* 🚀 Launch multiple desktop applications with a single gesture
* ⌨️ Manual workspace launcher using **Ctrl + Alt + J**
* 🛑 Prevent duplicate application launches
* ⏳ Configurable cooldown system
* ⚙️ Simple configuration through `config.py`
* 👁️ Live webcam preview
* 🖥️ Built specifically for Windows

---

# 🎥 Demo

> *(Replace this section with a GIF or short video after recording one.)*

```
Camera Ready...

Waiting for 👍

        👍

Gesture Detected!

Launching Workspace...

✓ Brave
✓ ChatGPT
✓ Claude
✓ Spotify

Workspace Ready 🚀
```

---

# 📂 Project Structure

```text
GestureLaunch/

├── config.py
├── detector.py
├── launcher.py
├── main.py
├── launch_workspace.bat
├── setup_hotkey.py
├── setup_autostart.py
├── requirements.txt
└── README.md
```

---

# 🛠 Technologies Used

* Python
* OpenCV
* MediaPipe
* psutil

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/GestureLaunch.git
cd GestureLaunch
```

Install the required packages

```bash
pip install -r requirements.txt
```

---

# ⚙️ Configuration

Open **config.py** and configure:

* Brave Browser path
* Claude Desktop path
* Spotify path
* Camera index
* Cooldown duration
* Gesture confirmation frames

ChatGPT launches through the Windows Start Menu, so no executable path is required.

---

# ▶️ Usage

Start GestureLaunch

```bash
python main.py
```

GestureLaunch will:

1. Initialize the webcam.
2. Detect your hand in real time.
3. Wait for a 👍 gesture.
4. Launch your configured workspace.
5. Enter cooldown before listening again.

---

# ⌨️ Manual Launcher

GestureLaunch also includes **launch_workspace.bat**.

This script launches the exact same workspace without using the webcam and is intended to be used with the included keyboard shortcut setup.

Default shortcut:

```
Ctrl + Alt + J
```

This gives you two ways to launch your workspace:

* 👋 Gesture Mode
* ⌨️ Keyboard Shortcut Mode

Both methods launch the same configured applications.

---

# 🧠 How It Works

GestureLaunch uses **MediaPipe Hands** to detect **21 hand landmarks** from the webcam.

Instead of using a trained gesture classifier, it analyzes the landmark positions to determine whether:

* 👍 Thumb is extended
* 👇 Index finger is folded
* 👇 Middle finger is folded
* 👇 Ring finger is folded
* 👇 Pinky finger is folded

When the gesture is held for several consecutive frames, the workspace launcher is triggered.

This lightweight geometric approach keeps the project responsive while avoiding the need for custom machine learning models.

---

# 🗺️ Roadmap

## Current

* ✅ Gesture recognition
* ✅ Workspace launcher
* ✅ Keyboard shortcut launcher
* ✅ Duplicate process prevention
* ✅ Cooldown system

## Planned

* ⬜ Face recognition (owner verification)
* ⬜ Transparent HUD overlay
* ⬜ System tray application
* ⬜ Custom gesture support
* ⬜ Multiple workspace profiles
* ⬜ Plugin system
* ⬜ AI integration

---

# 💡 Why I Built This

This project started with a simple question:

> **Can I launch my workspace without clicking through multiple applications every day?**

The original idea relied on sound detection using claps and finger snaps. However, modern laptops aggressively filter those sounds through built-in noise suppression, making the approach unreliable.

Instead of fighting the hardware, I switched to computer vision.

The result is GestureLaunch—a lightweight workspace launcher that uses a single thumbs-up gesture (or a keyboard shortcut) to instantly open my daily development environment.

---

# 🤝 Contributing

Suggestions, improvements, and pull requests are always welcome.

If you have an idea that could make GestureLaunch better, feel free to open an issue or submit a pull request.

---

# 📄 License

This project is licensed under the MIT License.

---

⭐ If you found this project interesting, consider giving it a star!
