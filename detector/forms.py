from django import forms
from django.core.validators import FileExtensionValidator


class ImageUploadForm(forms.Form):
    """
    Enhanced form for uploading images for circle detection.
    Accepts common image formats: JPG, JPEG, PNG, BMP, TIFF.
    Includes modern styling and validation.
    """
    image = forms.ImageField(
        label="Choose Image",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp', 'tiff'])
        ],
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-700 file:mr-4 file:py-3 file:px-6 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-gradient-to-r file:from-blue-50 file:to-purple-50 file:text-blue-700 hover:file:from-blue-100 hover:file:to-purple-100 cursor-pointer transition-all duration-300',
            'accept': 'image/*',
            'id': 'image-upload'
        }),
        help_text='Upload an image containing circular objects (JPG, PNG, BMP, TIFF) - Maximum 10MB'
    )
