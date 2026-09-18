"""
Health check route blueprint.
Provides a simple liveness probe indicating service operational status.
"""

from flask import Blueprint, current_app, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    """Return health status and basic application metadata."""
    app_name = current_app.config.get("APP_NAME", "VeraFace Backend")
    return jsonify({
        "status": "ok",
        "app": app_name,
        "model_loaded": False
    })
