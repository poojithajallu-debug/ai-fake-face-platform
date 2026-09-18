"""
Mock AI Inference Service for TrueFace backend (Phase 2 DEMO/MOCK mode).
Provides deterministic, reproducible fake predictions, confidence/trust calculations,
and synthetic Grad-CAM & LIME explanation placeholders.
"""

import base64
import hashlib
import io
import logging
from typing import Dict, Any, Tuple
import cv2
import numpy as np
from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)


def generate_placeholder_data_uri(label: str, base_color: Tuple[int, int, int]) -> str:
    """
    Generate an in-memory synthetic explanation placeholder PNG encoded as a base64 data URI.

    Args:
        label: Text string to draw on placeholder (e.g. 'Grad-CAM Heatmap (Mock)').
        base_color: RGB tuple for background accent.

    Returns:
        Data URI string: 'data:image/png;base64,...'
    """
    width, height = 256, 256
    img = Image.new("RGB", (width, height), color=(20, 24, 33))
    draw = ImageDraw.Draw(img)

    # Draw gradient or decorative mock grid
    for i in range(0, width, 32):
        draw.line([(i, 0), (i, height)], fill=(35, 42, 56), width=1)
    for j in range(0, height, 32):
        draw.line([(0, j), (width, j)], fill=(35, 42, 56), width=1)

    # Center circle simulating heatmap/feature activation
    center_box = [48, 48, 208, 208]
    draw.ellipse(center_box, outline=base_color, width=3)
    draw.ellipse([70, 70, 186, 186], fill=(*base_color, 80) if len(base_color) == 4 else base_color)

    # Text banner
    draw.rectangle([10, 210, 246, 246], fill=(15, 18, 26))
    draw.text((20, 220), label, fill=(240, 240, 240))

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_str}"


def predict_image_mock(image_cv2: np.ndarray) -> Dict[str, Any]:
    """
    Perform deterministic mock classification on an OpenCV image.

    Uses image metadata (dimensions and mean channel intensities) to derive
    a stable pseudo-random prediction, calibrated probability, and trust score.

    Args:
        image_cv2: numpy.ndarray representing BGR image.

    Returns:
        Dict containing prediction, probabilities, scores, warnings, and placeholder XAI images.
    """
    logger.info("Running mock inference on image (DEMO/MOCK mode)")

    if image_cv2 is None or image_cv2.size == 0:
        h, w, c = 224, 224, 3
        mean_val = 128.0
    else:
        h, w = image_cv2.shape[:2]
        c = image_cv2.shape[2] if len(image_cv2.shape) > 2 else 1
        mean_val = float(np.mean(image_cv2))

    # Compute a deterministic hash based on image shape and mean intensity
    hash_input = f"{h}_{w}_{c}_{mean_val:.4f}".encode("utf-8")
    hash_digest = hashlib.sha256(hash_input).hexdigest()
    hash_int = int(hash_digest[:8], 16)

    # Decide prediction: even -> Fake, odd -> Real
    is_fake = (hash_int % 2 == 0)

    # Generate probabilities in a realistic range (e.g., 0.65 to 0.98)
    primary_prob = 0.65 + ((hash_int % 33) / 100.0)
    primary_prob = round(min(0.98, max(0.60, primary_prob)), 3)
    secondary_prob = round(1.0 - primary_prob, 3)

    if is_fake:
        prediction = "Fake"
        fake_prob = primary_prob
        real_prob = secondary_prob
    else:
        prediction = "Real"
        real_prob = primary_prob
        fake_prob = secondary_prob

    # Confidence score: 0 to 100
    confidence_score = round(max(real_prob, fake_prob) * 100.0, 1)

    # Trust Score: project-defined reliability indicator (formula: confidence * 0.9 + 5 capped at 100)
    trust_score = round(min(100.0, confidence_score * 0.9 + 5.0), 1)

    # Generate synthetic XAI visual placeholders
    gradcam_uri = generate_placeholder_data_uri("Grad-CAM: High Heatmap", (220, 60, 60))
    lime_uri = generate_placeholder_data_uri("LIME: Superpixel Segments", (60, 140, 230))

    return {
        "prediction": prediction,
        "real_probability": real_prob,
        "fake_probability": fake_prob,
        "confidence_score": confidence_score,
        "trust_score": trust_score,
        "face_detected": True,
        "faces_count": 1,
        "gradcam_image": gradcam_uri,
        "lime_image": lime_uri,
        "warnings": ["Mock inference (DEMO mode)"]
    }
