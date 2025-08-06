# ⭕ Advanced Circle Detection Web Application

A Django-based web application that enables users to upload images and automatically detect circles using advanced computer vision techniques. The system incorporates preprocessing, multi-scale Hough Circle Transform, and robust post-processing (including NMS and scoring) for highly accurate results.

---

## 📌 Table of Contents
- [✨ Features](#-features)
- [🚀 Technologies Used](#-technologies-used)
- [🛠️ Setup Instructions](#-setup-instructions)
- [⚙️ How It Works – Image Processing Pipeline](#-how-it-works--image-processing-pipeline)
- [👤 Author](#-author)

---

## ✨ Features

- 🖼️ **Image Upload** – Simple web interface for uploading images.
- 🧪 **Advanced Preprocessing** – Uses CLAHE, Bilateral Filtering, Gaussian Blur, and Morphological operations.
- 🔍 **Multi-Scale Circle Detection** – Uses different `cv2.HoughCircles()` parameter sets to detect varied circle sizes and contrasts.
- 🧠 **Duplicate Removal (NMS)** – Applies Non-Maximum Suppression and circle quality scoring to eliminate overlaps.
- 👁️ **Visual Output** – Highlights detected circles on the image for intuitive verification.
- ⚠️ **Error Handling** – Detects and handles invalid inputs, oversized files, and processing issues.
- 🚀 **Performance Optimized** – Automatically resizes large images to prevent memory overload and lag.

---

## 🚀 Technologies Used

| Technology   | Description                            |
|--------------|----------------------------------------|
| Python 3.8+  | Programming Language                    |
| Django       | Web Framework                           |
| OpenCV       | Image processing & HoughCircles         |
| NumPy        | Matrix and image data handling          |
| Pillow (PIL) | Image format handling and conversion    |

---

## 🛠️ Setup Instructions

### ✅ Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

---

### 🧩 Installation Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/vatsalsavaliya/circle-detection-app.git
   cd circle-detection-app

2.  **Create and Activate Virtual Environment**

    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    * **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```


3.  **Install Dependencies**

    ```bash
    pip install django opencv-python numpy Pillow
    ```


4.  **Apply Migrations**

    ```bash
    cd circle_detection_app
    python manage.py migrate
    ```



5.  **Create Media Folders**

    ```bash
    mkdir -p media/processed
    ```





6.  **Run the Development Server**

    ```bash
    python manage.py runserver
    ```



7.  Access the Web App
		Visit: http://127.0.0.1:8000/




---

**⚙️ How It Works – Image Processing Pipeline**

1️⃣ process_image_with_error_handling()
Main entry point for image processing with validation and exceptions.


2️⃣ validate_and_prepare_image()
Loads image using PIL.

Converts to OpenCV-compatible format.

Validates size and resizes if >2000x2000 pixels.


3️⃣ enhanced_preprocessing()
Converts image to grayscale.

Applies:

CLAHE (Contrast Limited Adaptive Histogram Equalization)

Bilateral Filter (for noise reduction)

Gaussian Blur

Morphological operations (opening/closing)


4️⃣ advanced_circle_detection()
Runs HoughCircles with multiple parameter sets.

Adjusts minDist, param1, param2, minRadius, and maxRadius.


5️⃣ remove_duplicate_circles()
Uses calculate_circle_quality() for each circle.

Applies Non-Maximum Suppression to remove overlaps.


6️⃣ calculate_circle_quality()
Based on:

Edge Density

Intensity Uniformity

Radius Reasonableness


7️⃣ Visualization
Draws circles on image with different colors and center markers.




👤 Author
Vatsal Hareshbhai Savaliya
🎓 B.Tech in Information Technology (7th Semester)

🏫 Anand Agricultural University, Gujarat, India

📧 Email: vatsalsavaliya03@gmail.com

🔗 GitHub: https://github.com/Savaliya03

🔗 LinkedIn: https://www.linkedin.com/in/vatsal-savaliya-587bab281


💬 Open an Issue on GitHub

