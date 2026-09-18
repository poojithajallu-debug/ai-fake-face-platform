"""
Prediction route blueprint for TrueFace backend.
Exposes POST /api/predict accepting multipart/form-data image uploads.
"""

from datetime import datetime, timezone
import uuid
from flask import Blueprint, request, jsonify

from ..utils.image_utils import validate_image, read_image_as_cv2
from ..services.inference_mock import predict_image_mock

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict", methods=["POST"])
def predict():
    """
    Accept an uploaded face image and return a mock prediction response.

    Form-data:
        image: FileStorage binary image (JPEG or PNG, <= 5 MB)

    Returns:
        JSON response with prediction verdict, confidence, trust score,
        synthetic explanations, and verification metadata.
    """
    # Check for presence of 'image' in multipart files
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "Missing required form-data field 'image'."
        }), 400

    image_file = request.files["image"]

    # Validate image file properties and format
    is_valid, error_message = validate_image(image_file)
    if not is_valid:
        return jsonify({
            "success": False,
            "error": error_message
        }), 400

    # Decode image into OpenCV format
    image_cv2 = read_image_as_cv2(image_file)
    if image_cv2 is None:
        return jsonify({
            "success": False,
            "error": "Failed to decode image. File may be corrupted or unreadable."
        }), 400

    # Run mock inference
    mock_result = predict_image_mock(image_cv2)

    # Generate tracking metadata
    verification_id = f"v_{int(datetime.now(timezone.utc).timestamp())}_{uuid.uuid4().hex[:6]}"
    iso_timestamp = datetime.now(timezone.utc).isoformat()

    response_payload = {
        "success": True,
        "verification_id": verification_id,
        "timestamp": iso_timestamp,
        "prediction": mock_result["prediction"],
        "real_probability": mock_result["real_probability"],
        "fake_probability": mock_result["fake_probability"],
        "confidence_score": mock_result["confidence_score"],
        "trust_score": mock_result["trust_score"],
        "message": "Mock prediction (DEMO mode). Not a real AI detection.",
        "gradcam_image": mock_result["gradcam_image"],
        "lime_image": mock_result["lime_image"],
        "face_detected": mock_result["face_detected"],
        "faces_count": mock_result["faces_count"],
        "warnings": mock_result["warnings"]
    }

    return jsonify(response_payload), 200
