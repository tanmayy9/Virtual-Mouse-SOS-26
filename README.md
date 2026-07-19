# Gesture-Controlled Virtual Mouse 

A computer-vision based virtual mouse that lets you control your cursor — move, click, double-click, and scroll — using nothing but hand gestures captured through a webcam. Built as my Summer of Science (SoS) project at IIT Bombay.

📹 **[Watch the demo video](https://drive.google.com/file/d/1A0iK2f2eejzSrw8hmXD0sXRMw30NxAx3/view?usp=sharing)**

---

## Overview

This project follows a structured learning path from CV fundamentals to a complete real-time application:

**Python/NumPy/OpenCV basics → Neural Network & CNN theory → HSV-based color object tracker (midterm) → MediaPipe hand tracking → Gesture-Controlled Virtual Mouse (final project)**

The final system uses **MediaPipe** to detect 21 hand landmarks per frame in real time, interprets specific landmark positions as gestures, and translates them into mouse actions using **PyAutoGUI**.

## Features

| Gesture | Action |
|---|---|
| Index finger movement | Move cursor |
| Thumb–index pinch | Single click |
| Thumb–index double pinch (within 0.4s) | Double click |
| Four fingers raised + vertical movement | Scroll up / down (relative to raise point) |

## Tech Stack

- **MediaPipe** — real-time hand landmark detection (21 points/hand)
- **OpenCV** — webcam capture, frame processing, color-space work (from the midterm tracker)
- **PyAutoGUI** — simulating cursor movement, clicks, and scroll
- **NumPy** — coordinate remapping (`np.interp`) and smoothing

## Engineering Challenges & Fixes

Building a working demo was step one — making it usable required debugging real instability issues:

- **Cursor jitter** → Raw landmark coordinates are noisy frame-to-frame even when the hand is still. Fixed with an **exponential moving average** that blends each new target position with the previous one instead of jumping directly to it.
- **Click flickering** → A single distance threshold for the pinch gesture caused rapid false clicks near the boundary due to natural hand tremor. Fixed with **hysteresis** — separate enter/exit thresholds (0.055 / 0.07) so the pinch state can't flicker.
- **Limited screen reachability** → Directly mapping the full camera frame (0–1) to screen coordinates meant physically reaching the camera's edge was needed to reach screen corners (e.g. window close/minimize buttons). Fixed by defining a smaller **active zone** within the frame and remapping it to the full screen resolution using `np.interp`.

## Project Structure

```
├── main.py                          # Main application: capture loop, gesture detection, mouse control
├── calculation.py                   # Helper geometry functions (angle/distance calculations)
├── SOS_26_Endterm_Report.pdf
├── Virtual Mouse Presentation (1).pdf
└── README.md
```

## Setup

> Requires **Python 3.9–3.12** (MediaPipe does not yet support 3.13+).

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install opencv-python mediapipe pyautogui numpy
python main.py
```

Press **`q`** with the live feed window focused to quit.

## Documentation

-  [End-Term Report](SOS_26_Endterm_Report.pdf)
-  [Presentation Slides](<Virtual Mouse Presentation (1).pdf>)
-  [Demo Video](https://drive.google.com/file/d/1A0iK2f2eejzSrw8hmXD0sXRMw30NxAx3/view?usp=sharing)

## Background

Earlier milestone in this project: an **HSV-based colored object tracker** built with OpenCV, covering frame processing, color-space thresholding, and contour detection — the foundation this final project was built on top of.

---

**Author:** Tanmay
