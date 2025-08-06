from django.shortcuts import render
from .forms import ImageUploadForm
import cv2
import numpy as np
from django.core.files.storage import FileSystemStorage
import os

# Initialize the FileSystemStorage
fs = FileSystemStorage()

def adaptive_preprocessing(image):
    """
    Advanced preprocessing to enhance circle detection accuracy.
    Applies multiple techniques based on image characteristics.
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # Calculate image statistics
    mean_intensity = np.mean(gray)
    std_intensity = np.std(gray)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) for better contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Adaptive denoising based on image characteristics
    if std_intensity < 30:  # Low contrast image
        # Apply stronger denoising
        denoised = cv2.bilateralFilter(enhanced, 9, 80, 80)
    else:
        # Apply moderate denoising
        denoised = cv2.bilateralFilter(enhanced, 5, 50, 50)
    
    # Edge-preserving smoothing
    blurred = cv2.GaussianBlur(denoised, (5, 5), 1.5)
    
    # Morphological operations to clean up the image
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    cleaned = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)
    
    return cleaned, mean_intensity, std_intensity

def multi_scale_circle_detection(image, min_radius=10, max_radius=60):
    """
    Multi-scale circle detection with parameter optimization and filtering.
    Uses multiple detection passes and validation to improve accuracy.
    """
    height, width = image.shape
    all_circles = []
    
    # Preprocess the image
    processed_img, mean_intensity, std_intensity = adaptive_preprocessing(image)
    
    # Define multiple parameter sets for different scenarios
    param_sets = [
        # Standard parameters
        {
            'dp': 1.2,
            'param1': max(50, int(mean_intensity * 0.4)),
            'param2': max(25, int(mean_intensity * 0.2)),
            'minRadius': min_radius,
            'maxRadius': max_radius
        },
        # Sensitive parameters (more circles)
        {
            'dp': 1.5,
            'param1': max(30, int(mean_intensity * 0.3)),
            'param2': max(20, int(mean_intensity * 0.15)),
            'minRadius': min_radius,
            'maxRadius': max_radius
        },
        # Conservative parameters (fewer false positives)
        {
            'dp': 1.0,
            'param1': max(60, int(mean_intensity * 0.5)),
            'param2': max(35, int(mean_intensity * 0.25)),
            'minRadius': min_radius,
            'maxRadius': max_radius
        }
    ]
    
    # Run detection with different parameter sets
    for params in param_sets:
        circles = cv2.HoughCircles(
            processed_img,
            cv2.HOUGH_GRADIENT,
            dp=params['dp'],
            minDist=max(20, min_radius),
            param1=params['param1'],
            param2=params['param2'],
            minRadius=params['minRadius'],
            maxRadius=params['maxRadius']
        )
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            all_circles.extend(circles)
    
    if not all_circles:
        return np.array([]), 0
    
    # Convert to numpy array for processing
    all_circles = np.array(all_circles)
    
    # Remove duplicate circles using non-maximum suppression
    filtered_circles = []
    overlap_threshold = 0.3
    
    # Sort circles by parameter strength (we'll use radius as a proxy)
    sorted_indices = np.argsort(all_circles[:, 2])[::-1]  # Sort by radius, largest first
    
    for i in sorted_indices:
        current_circle = all_circles[i]
        x1, y1, r1 = current_circle
        
        # Check if this circle overlaps significantly with any already accepted circle
        is_duplicate = False
        for accepted_circle in filtered_circles:
            x2, y2, r2 = accepted_circle
            
            # Calculate distance between centers
            distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            
            # Calculate overlap ratio
            min_radius = min(r1, r2)
            if distance < min_radius * (1 + overlap_threshold):
                is_duplicate = True
                break
        
        if not is_duplicate:
            # Additional validation: check if circle is well-formed
            if is_valid_circle(processed_img, x1, y1, r1):
                filtered_circles.append(current_circle)
    
    return np.array(filtered_circles), len(filtered_circles)

def is_valid_circle(image, x, y, radius):
    """
    Validate if a detected circle is likely to be a real circle.
    Uses edge density and symmetry checks.
    """
    height, width = image.shape
    
    # Check if circle is within image bounds
    if (x - radius < 0 or x + radius >= width or 
        y - radius < 0 or y + radius >= height):
        return False
    
    # Extract region of interest
    roi = image[max(0, y-radius):min(height, y+radius+1), 
                max(0, x-radius):min(width, x+radius+1)]
    
    if roi.size == 0:
        return False
    
    # Apply edge detection to the ROI
    edges = cv2.Canny(roi, 50, 150)
    
    # Create a circular mask
    mask = np.zeros_like(edges)
    center_roi = (min(radius, roi.shape[1]//2), min(radius, roi.shape[0]//2))
    cv2.circle(mask, center_roi, radius-2, 255, 2)
    
    # Calculate edge density along the circular boundary
    masked_edges = cv2.bitwise_and(edges, mask)
    edge_pixels = np.sum(masked_edges > 0)
    boundary_pixels = np.sum(mask > 0)
    
    if boundary_pixels == 0:
        return False
    
    edge_density = edge_pixels / boundary_pixels
    
    # A good circle should have reasonable edge density
    return edge_density > 0.1

def process_image(image_path):
    """
    Enhanced image processing with improved circle detection.
    """
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use the enhanced multi-scale circle detection
    circles, circle_count = multi_scale_circle_detection(gray)
    
    # Draw detected circles on the original image
    if len(circles) > 0:
        for (x, y, r) in circles:
            # Draw the circle outline
            cv2.circle(image, (x, y), r, (0, 0, 255), 2)
            # Draw the circle center
            cv2.circle(image, (x, y), 2, (0, 255, 0), 3)
            # Add radius text
            cv2.putText(image, f'r={r}', (x-10, y-r-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    
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