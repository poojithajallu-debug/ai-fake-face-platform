"""
Flask application factory for TrueFace backend.
Initializes the Flask app, attaches configuration, and registers route blueprints.
"""

from flask import Flask, jsonify
from .config import Config
from .routes.health import health_bp
from .routes.predict import predict_bp


def create_app(config_class=Config):
    """
    Create and configure an instance of the Flask application.

    Args:
        config_class: Configuration class to load settings from.

    Returns:
        Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register route blueprints
    app.register_blueprint(health_bp, url_prefix="")
    app.register_blueprint(predict_bp, url_prefix="/api")

    @app.route("/", methods=["GET"])
    def root():
        """Root welcome endpoint providing basic API information."""
        return jsonify({
            "message": "Welcome to TrueFace Backend API",
            "version": "1.0.0",
            "health_check": "/health",
            "endpoints": {
                "health": "/health",
                "predict": "/api/predict"
            }
        })

    return app
