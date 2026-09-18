"""
Configuration settings for VeraFace Flask backend.
Loads settings from environment variables with sensible defaults for development.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


class Config:
    """Base application configuration."""

    # Debug mode flag (defaults to True for local development)
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")

    # Server binding host
    HOST = os.getenv("FLASK_HOST", "127.0.0.1")

    # Server port
    PORT = int(os.getenv("FLASK_PORT", "5000"))

    # Human-readable application name
    APP_NAME = os.getenv("FLASK_APP_NAME", "VeraFace Backend")
