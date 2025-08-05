from django import forms
from django.core.validators import FileExtensionValidator


class ImageUploadForm(forms.Form):
    """
    Form for uploading images for circle detection.
    Accepts common image formats: JPG, JPEG, PNG, BMP, TIFF.
    """
    image = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp', 'tiff'])
        ],
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            'accept': 'image/*'
        }),
        help_text='Upload an image file (JPG, PNG, BMP, TIFF) to detect circles.'
    )
