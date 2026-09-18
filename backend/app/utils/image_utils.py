"""
Image utility functions for VeraFace backend.
Provides upload validation, MIME checking, size bounds, and OpenCV decoding.
"""

from typing import Tuple, Optional
import io
import cv2
import numpy as np
from PIL import Image

# Maximum allowed upload size: 5 Megabytes
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

# Permitted MIME types
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

# Permitted file extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def validate_image(file_storage) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded file for presence, extension, MIME type, size, and image integrity.

    Args:
        file_storage: Werkzeug FileStorage instance from request.files['image'].

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is None.
    """
    if file_storage is None or not getattr(file_storage, "filename", ""):
        return False, "No image file provided in request (expected form field 'image')."

    filename = file_storage.filename.lower()
    has_valid_ext = any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)
    if not has_valid_ext:
        return False, f"Unsupported file extension. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}."

    # Validate MIME type header
    content_type = getattr(file_storage, "content_type", "").lower()
    if content_type and content_type not in ALLOWED_MIME_TYPES:
        return False, f"Unsupported Content-Type '{content_type}'. Allowed types: image/jpeg, image/png."

    # Validate file size
    file_storage.seek(0, io.SEEK_END)
    size_bytes = file_storage.tell()
    file_storage.seek(0)

    if size_bytes == 0:
        return False, "Uploaded image file is empty (0 bytes)."

    if size_bytes > MAX_FILE_SIZE_BYTES:
        max_mb = MAX_FILE_SIZE_BYTES / (1024 * 1024)
        return False, f"Image size exceeds maximum limit of {max_mb:.1f} MB."

    # Verify actual image content via PIL to prevent non-image or corrupted files
    try:
        header_bytes = file_storage.read(size_bytes)
        file_storage.seek(0)
        img = Image.open(io.BytesIO(header_bytes))
        img.verify()  # Verifies file format integrity without decoding entire image
        if img.format not in ("JPEG", "PNG"):
            return False, f"Invalid image format: expected JPEG or PNG, received {img.format}."
    except Exception as exc:
        file_storage.seek(0)
        return False, f"Failed to parse image file: {str(exc)}"

    return True, None


def read_image_as_cv2(file_storage) -> Optional[np.ndarray]:
    """
    Read uploaded FileStorage bytes and decode into an OpenCV BGR numpy array.

    Args:
        file_storage: Werkzeug FileStorage instance.

    Returns:
        numpy.ndarray representing image in BGR format, or None if decoding fails.
    """
    try:
        file_storage.seek(0)
        file_bytes = file_storage.read()
        file_storage.seek(0)

        np_arr = np.frombuffer(file_bytes, np.uint8)
        img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return img_bgr
    except Exception:
        return None
