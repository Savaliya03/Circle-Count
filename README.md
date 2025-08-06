****⭕ Advanced Circle Detection Web Application****
This project is a Django-based web application that allows users to upload images and detect circles within them using advanced computer vision techniques. It leverages sophisticated preprocessing, multi-scale Hough Circle Transform, and robust post-processing to achieve high precision in circle detection.

✨ Features
🖼️ Image Upload – Upload images through a user-friendly web interface.

🧪 Advanced Preprocessing – CLAHE, Bilateral Filtering, and Morphological Operations for optimal input enhancement.

🔍 Multi-Scale Circle Detection – Detects circles using multiple sets of Hough Circle Transform parameters.

🧠 Duplicate Removal (NMS) – Applies quality scoring and Non-Maximum Suppression to remove overlapping or redundant circles.

👁️ Visual Output – Displays both original and processed image with circles highlighted.

⚠️ Error Handling – Handles invalid formats, large images, and runtime errors.

🚀 Performance Optimized – Automatically resizes large images to avoid performance issues.

🚀 Technologies Used
Python 3.8+

Django – Web framework

OpenCV (cv2) – Image processing and circle detection

NumPy – Numerical image operations

Pillow (PIL) – Image loading and format support

🛠️ Setup Instructions
✅ Prerequisites
Python 3.8+

pip (Python package manager)

🔧 **Installation**
Clone the Repository

git clone https://github.com/vatsalsavaliya/circle-detection-app.git
cd circle-detection-app

Create and Activate Virtual Environment
Windows:

python -m venv venv
.\venv\Scripts\activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate

Install Dependencies

pip install django opencv-python numpy Pillow

Apply Django Migrations

cd circle_detection_app
python manage.py migrate

Create Media Directories

mkdir -p media/processed

Run the Development Server

python manage.py runserver

Access the Application
Open your browser and go to:
http://127.0.0.1:8000/

⚙️ How It Works – Image Processing Pipeline
🔄 process_image_with_error_handling()
validate_and_prepare_image

Loads the image using Pillow.

Converts to OpenCV BGR format.

Validates and resizes large images (>2000x2000 px).

enhanced_preprocessing

Converts to grayscale.

Applies CLAHE for contrast enhancement.

Uses Bilateral Filter and Gaussian Blur.

Applies Morphological Operations.

advanced_circle_detection

Runs cv2.HoughCircles() with multiple configurations.

Detects circles of varying sizes and strengths.

Tunes minDist to avoid nearby duplicate detections.

remove_duplicate_circles()

Scores each circle with calculate_circle_quality().

Applies NMS to select high-quality, non-overlapping circles.

calculate_circle_quality()

Edge Density: Strength of edges along the circle.

Intensity Uniformity: Brightness consistency within the circle.

Radius Reasonableness: How close the radius is to expected values.

Visualization

Circles are drawn with unique colors on the processed image.

📷 Demo Screenshot (Optional)
You can add a screenshot here showing before/after detection results.

🤝 Contributing
We welcome contributions!

Fork the repository

Create a new branch

Make your changes

Submit a pull request

📄 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute it.

👤 Author
Vatsal Hareshbhai Savaliya
🎓 B.Tech (Information Technology), 7th Semester
📍 Anand Agricultural University, Gujarat, India
📧 Email: vatsalsavaliya03@gmail.com
🔗 GitHub: https://github.com/Savaliya03
🔗 LinkedIn: https://www.linkedin.com/in/vatsal-savaliya-587bab281

📬 Contact
For queries, suggestions, or feedback:

Open an issue on this repo

Email me directly at vatsalsavaliya03@gmail.com
