⭕ Advanced Circle Detection Web Application
This project is a Django-based web application that allows users to upload images and detect circles within them using advanced computer vision techniques. It employs sophisticated preprocessing, multi-scale Hough Circle Transform, and robust post-processing to achieve high precision in circle detection.

✨ Features
Image Upload: Easily upload images through a user-friendly web interface.

Advanced Preprocessing: Images undergo adaptive contrast enhancement (CLAHE), noise reduction (Bilateral Filtering), and morphological operations to optimize them for circle detection.

Multi-Scale Circle Detection: Utilizes the Hough Circle Transform with multiple parameter sets to detect circles of varying sizes and clarity.

Robust Duplicate Removal: Implements a quality-scoring system and Non-Maximum Suppression (NMS) to eliminate redundant or overlapping circle detections, ensuring a clean output.

Visual Output: Displays the original image alongside the processed image with detected circles, their centers, and radii highlighted.

Error Handling: Comprehensive error handling for invalid image formats, sizes, and processing failures.

Performance Optimization: Includes image resizing for very large inputs to prevent performance bottlenecks.

🚀 Technologies Used
Django: Web framework for building the application.

OpenCV (cv2): Core library for image processing and circle detection.

NumPy: Essential for numerical operations, especially with image arrays.

Pillow (PIL): Used for robust image loading and format handling.

Python: The primary programming language.

🛠️ Setup Instructions
Follow these steps to get the project up and running on your local machine.

Prerequisites
Python 3.8+

pip (Python package installer)

Installation Steps
Clone the Repository (if applicable):

git clone <your-repository-url>
cd <your-project-directory>

Create a Virtual Environment (Recommended):

python -m venv venv

Activate the Virtual Environment:

On Windows:

.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Install Dependencies:

pip install django opencv-python numpy Pillow

Set up Django Project:

Navigate into your Django project directory (where manage.py is located):

cd your_django_project_name # e.g., cd circle_detector_app

Apply migrations:

python manage.py migrate

Create Media Directories:
Ensure you have media and media/processed directories in your project's root (or as configured in settings.py) for storing uploaded and processed images.

mkdir -p media/processed

Run the Development Server:

python manage.py runserver

The application will be accessible at http://127.0.0.1:8000/.

💡 How It Works
The core of the circle detection is handled by the process_image_with_error_handling function, which orchestrates the following steps:

validate_and_prepare_image:

Loads the image using Pillow for broad format support.

Converts the image to OpenCV's BGR format.

Performs basic validation (e.g., minimum dimensions) and resizes very large images to a manageable size (e.g., max 2000x2000 pixels) to prevent performance issues.

enhanced_preprocessing:

Converts the image to grayscale.

Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to improve local contrast, especially in images with varying lighting.

Uses Adaptive Bilateral Filtering for noise reduction, which is excellent at smoothing images while preserving sharp edges—crucial for circle detection.

Performs light Gaussian Blurring and Morphological Operations (Opening and Closing) to further clean the image and remove small artifacts.

advanced_circle_detection:

Applies the Hough Circle Transform (cv2.HoughCircles) using multiple sets of parameters (dp, param1, param2, minDist, minRadius, maxRadius). This multi-strategy approach helps in detecting circles under different conditions (e.g., faint, clear, various sizes).

minDist is carefully tuned to prevent multiple detections of the same circle.

remove_duplicate_circles (Non-Maximum Suppression - NMS): This critical step filters out redundant circle detections. It first scores each detected circle based on its quality (using calculate_circle_quality) and then iteratively selects the highest-quality circles, suppressing any overlapping lower-quality detections.

calculate_circle_quality:

Evaluates a circle's quality based on:

Edge Density: How well the circle's perimeter aligns with strong edges in the image.

Intensity Uniformity: How consistent the pixel intensities are within the circle.

Radius Reasonableness: A score based on how close the detected radius is to an expected ideal radius.

Drawing Results: The detected circles (with their centers and radii) are drawn onto a copy of the original image using distinct colors for better visualization.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements or bug fixes, please open an issue or submit a pull request.

📄 License
This project is open-source and available under the MIT License.
