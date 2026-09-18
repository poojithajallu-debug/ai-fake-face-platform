"""
Unit and integration tests for POST /api/predict mock inference endpoint.
"""

import io
from PIL import Image
import pytest
from app import create_app


@pytest.fixture
def client():
    """Create a test client fixture for the Flask application."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def create_test_image_bytes(format_name: str = "PNG", color=(100, 150, 200)) -> io.BytesIO:
    """Helper to generate an in-memory image for upload testing."""
    img = Image.new("RGB", (64, 64), color=color)
    buffer = io.BytesIO()
    img.save(buffer, format=format_name)
    buffer.seek(0)
    return buffer


def test_predict_valid_png(client):
    """Test POST /api/predict with a valid PNG image."""
    img_bytes = create_test_image_bytes("PNG")
    data = {
        "image": (img_bytes, "test_face.png", "image/png")
    }

    response = client.post(
        "/api/predict",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data is not None
    assert json_data["success"] is True
    assert json_data["prediction"] in ("Real", "Fake")
    assert 0.0 <= json_data["real_probability"] <= 1.0
    assert 0.0 <= json_data["fake_probability"] <= 1.0
    assert abs((json_data["real_probability"] + json_data["fake_probability"]) - 1.0) < 0.01
    assert 0.0 <= json_data["confidence_score"] <= 100.0
    assert 0.0 <= json_data["trust_score"] <= 100.0
    assert json_data["verification_id"].startswith("v_")
    assert "Mock" in json_data["message"]
    assert any("Mock" in w for w in json_data["warnings"])
    assert json_data["gradcam_image"].startswith("data:image/png;base64,")
    assert json_data["lime_image"].startswith("data:image/png;base64,")


def test_predict_valid_jpeg(client):
    """Test POST /api/predict with a valid JPEG image."""
    img_bytes = create_test_image_bytes("JPEG")
    data = {
        "image": (img_bytes, "test_face.jpg", "image/jpeg")
    }

    response = client.post(
        "/api/predict",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["face_detected"] is True


def test_predict_invalid_file_type(client):
    """Test POST /api/predict with an invalid non-image file type (text file)."""
    text_buffer = io.BytesIO(b"This is a text file, not an image.")
    data = {
        "image": (text_buffer, "test.txt", "text/plain")
    }

    response = client.post(
        "/api/predict",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] is False
    assert "Unsupported" in json_data["error"] or "extension" in json_data["error"]


def test_predict_missing_image_field(client):
    """Test POST /api/predict when form field 'image' is missing."""
    response = client.post(
        "/api/predict",
        data={},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] is False
    assert "image" in json_data["error"]


def test_predict_empty_image(client):
    """Test POST /api/predict with an empty 0-byte file."""
    empty_buffer = io.BytesIO(b"")
    data = {
        "image": (empty_buffer, "empty.png", "image/png")
    }

    response = client.post(
        "/api/predict",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] is False
    assert "empty" in json_data["error"].lower()
