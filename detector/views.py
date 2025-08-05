from django.shortcuts import render
from .forms import ImageUploadForm
import cv2
import numpy as np
from django.core.files.storage import FileSystemStorage
import os


# Initialize the FileSystemStorage
fs = FileSystemStorage()

def process_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Image dimensions
    height, width = gray.shape

    # Heuristics for HoughCircles parameters
    dp = 1.5 if max(width, height) > 1000 else 2.0  # Adjust based on resolution
    median_intensity = np.median(gray)
    param1 = 50 if median_intensity > 100 else 30  # Adjust according to brightness
    param2 = 50 if median_intensity > 100 else 30  # Increase for fewer circles

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detect circles using Hough Circles
    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT, dp=dp, minDist=30,
        param1=param1, param2=param2, minRadius=10, maxRadius=60
    )

    circle_count = 0

    # If circles are detected, draw them
    if circles is not None:
        circles = np.uint16(np.around(circles))
        circle_count = circles.shape[1]
        for circle in circles[0, :]:
            center_x, center_y, radius = circle
            cv2.circle(image, (center_x, center_y), radius, (0, 0, 255), 2)
            cv2.circle(image, (center_x, center_y), 2, (0, 255, 0), 3)

    return image, circle_count

def index(request):
    """
    Main view that handles both GET (display form) and POST (process image) requests.
    
    GET: Display the upload form
    POST: Process uploaded image and display results
    """
    context = {'form': ImageUploadForm()}
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Handle the uploaded image
                uploaded_image = request.FILES['image']
                
                # Save the original image
                img_name = fs.save(uploaded_image.name, uploaded_image)
                img_path = fs.path(img_name)
                
                # Process the image to detect circles
                processed_img, circle_count = process_image(img_path)
                
                # Save the processed image
                processed_img_name = 'processed_' + img_name
                processed_img_path = os.path.join(fs.location, 'processed', processed_img_name)
                
                # Ensure the processed directory exists
                os.makedirs(os.path.dirname(processed_img_path), exist_ok=True)
                
                # Save the processed image
                cv2.imwrite(processed_img_path, processed_img)
                
                # Update context with results
                context.update({
                    'form': form,
                    'original_image_url': fs.url(img_name),
                    'processed_image_url': fs.url('processed/' + processed_img_name),
                    'circle_count': circle_count,
                    'success': True
                })
                
            except Exception as e:
                # Handle any errors during image processing
                context.update({
                    'form': form,
                    'error': f'Error processing image: {str(e)}'
                })
        else:
            # Form validation failed
            context.update({
                'form': form,
                'error': 'Please upload a valid image file.'
            })
    
    return render(request, 'index.html', context)
