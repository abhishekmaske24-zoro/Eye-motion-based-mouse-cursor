# Eye-Controlled Mouse Cursor 🖱️👁️

A real-time eye-based cursor control system built using Computer Vision.  
The application tracks eye movement and blinks to control mouse movement, clicks, and scrolling.

## Features
- Cursor movement using eye position
- Left eye blink → Left click
- Right eye blink → Right click
- Eye movement up/down → Scroll
- Smooth cursor motion with dead zone filtering

## Tech Stack
- Python
- OpenCV
- MediaPipe Face Mesh
- PyAutoGUI

## How It Works
- Uses MediaPipe Face Mesh to detect facial landmarks
- Calculates eye center movement for cursor positioning
- Detects blinks using eye landmark distances
- Maps eye movement to screen coordinates in real time

## Installation
```bash
pip install opencv-python mediapipe pyautogui
