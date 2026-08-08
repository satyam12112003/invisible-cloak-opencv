# 🪄 Invisible Cloak

A real-time **Invisible Cloak application** built with Python and OpenCV. The project uses computer vision, color segmentation, and background replacement techniques to create an illusion where a selected colored object appears invisible in the live camera feed.

## ✨ Features

* 🎥 Real-time camera feed
* 🪄 Invisible cloak effect
* 🎨 Color-based segmentation
* 🖼️ Background capture and replacement
* ⚡ Real-time image processing
* 🧩 Modular project architecture
* 🖥️ Simple and interactive interface
* 📸 Screenshot-ready output

## 🛠️ Tech Stack

| Technology            | Purpose                              |
| --------------------- | ------------------------------------ |
| 🐍 Python             | Core programming language            |
| 👁️ OpenCV            | Computer vision & image processing   |
| 🔢 NumPy              | Numerical and image-array operations |
| 🎨 Color Segmentation | Detecting the cloak/object           |
| 📷 Webcam             | Real-time video input                |

## 📂 Project Structure

```text
Invisible Cloak/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/
│   └── screenshots/
│
└── src/
    ├── __init__.py
    ├── config.py
    ├── camera.py
    ├── segmentation.py
    └── ui.py
```

### 📄 File Description

* **`app.py`** — Main entry point of the application.
* **`requirements.txt`** — Contains the required Python dependencies.
* **`config.py`** — Stores application and computer-vision configuration.
* **`camera.py`** — Handles webcam initialization and video capture.
* **`segmentation.py`** — Performs color detection and segmentation.
* **`ui.py`** — Handles the user interface and output display.
* **`assets/screenshots/`** — Stores project screenshots and visual assets.
* **`.gitignore`** — Specifies files and folders that should not be committed to GitHub.

## 🧠 How It Works

The Invisible Cloak effect is created using a simple computer vision pipeline:

```text
Webcam
   ↓
Capture Background
   ↓
Read Live Frame
   ↓
Color Detection
   ↓
Create Mask
   ↓
Replace Detected Area
   ↓
Combine With Background
   ↓
Display Invisible Effect
```

### 🔍 Processing Steps

1. The webcam captures the live video.
2. A clean background frame is captured before the cloak is detected.
3. The application converts the current frame into a suitable color space.
4. The target cloak color is detected using color thresholds.
5. A mask is generated for the detected region.
6. The detected region is replaced with the corresponding background area.
7. The final frame is displayed in real time.

## 🚀 Getting Started

### Prerequisites

Make sure Python is installed on your system.

Check your Python version:

```bash
python --version
```

### 1. Clone the Repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

```bash
cd "Invisible Cloak"
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Project

```bash
python app.py
```

Then follow the instructions displayed by the application.



## 🎯 Learning Objectives

This project demonstrates practical concepts of:

* Computer Vision
* OpenCV
* Image Processing
* Color Detection
* Image Masking
* Background Replacement
* Real-Time Video Processing
* Python Project Structuring

## 🔮 Future Improvements

Some possible improvements for future versions:

* 🤖 AI-based object segmentation
* 🎨 Multiple cloak color support
* 📹 Video recording
* 📸 Capture screenshots directly from the application
* 🎚️ Adjustable color thresholds
* ⚡ Improved processing performance
* 📱 Responsive web interface
* 🎭 Advanced background effects

## 🧪 Project Status

**Status:** ✅ Completed / Working

The project is primarily developed as a computer-vision learning project and can be extended with more advanced segmentation and AI techniques.

## 👨‍💻 Author

### Satyam Jaiswal

Computer Science & Engineering Student

GitHub: **[@satyam12112003](https://github.com/satyam12112003)**

## ⭐ Contributing

Contributions, suggestions, and improvements are welcome.

If you find this project interesting, consider giving the repository a ⭐ on GitHub.

## 📜 License

This project is available for educational and personal use.

---

> 🪄 **Invisible Cloak — Turning Computer Vision Into Magic.**
