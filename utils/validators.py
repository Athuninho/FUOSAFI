"""
FUOSAFI - Input & File Upload Validation Utilities
"""

import os
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image
import config

def validate_image_upload(uploaded_file) -> Tuple[bool, str]:
    """
    Validates uploaded image file:
    - Check file size limit (<= 10MB)
    - Check file extension
    - Check actual image headers using Pillow
    """
    if uploaded_file is None:
        return True, ""  # Optional or checked elsewhere
        
    # Check size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > config.MAX_IMAGE_SIZE_MB:
        return False, f"Image size ({file_size_mb:.1f} MB) exceeds maximum allowed limit of {config.MAX_IMAGE_SIZE_MB} MB."

    # Check extension
    ext = Path(uploaded_file.name).suffix.lower().lstrip(".")
    if ext not in config.ALLOWED_IMAGE_EXTENSIONS:
        return False, f"File format '.{ext}' is not supported. Supported formats: {', '.join(config.ALLOWED_IMAGE_EXTENSIONS)}."

    # Validate image header integrity with Pillow
    try:
        uploaded_file.seek(0)
        img = Image.open(uploaded_file)
        img.verify()
        uploaded_file.seek(0)
    except Exception:
        return False, "The uploaded file is corrupted or not a valid image file."

    return True, ""

def validate_coordinates(lat: float, lon: float) -> Tuple[bool, str]:
    """
    Validates geographical latitude and longitude coordinates.
    """
    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (ValueError, TypeError):
        return False, "Latitude and longitude must be valid decimal numbers."

    if not (-90.0 <= lat_f <= 90.0):
        return False, f"Latitude {lat_f} is out of bounds (-90 to +90 degrees)."

    if not (-180.0 <= lon_f <= 180.0):
        return False, f"Longitude {lon_f} is out of bounds (-180 to +180 degrees)."

    return True, ""
