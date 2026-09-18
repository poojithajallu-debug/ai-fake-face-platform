"""
Unit test for TrueFace Flask backend health endpoint.
"""

from app import create_app


def test_health_endpoint():
    """Test that GET /health returns status ok, correct app name, and model_loaded=False."""
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/health")
        assert response.status_code == 200

        data = response.get_json()
        assert data is not None
        assert data["status"] == "ok"
        assert data["app"] == "TrueFace Backend"
        assert data["model_loaded"] is False


def test_root_endpoint():
    """Test that GET / returns welcome message and health endpoint link."""
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200

        data = response.get_json()
        assert data is not None
        assert "Welcome to TrueFace Backend API" in data["message"]
        assert data["health_check"] == "/health"
