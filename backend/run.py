"""
Development server runner for TrueFace Flask backend.
Usage:
    python run.py
"""

from app import create_app
from app.config import Config

app = create_app()

if __name__ == "__main__":
    print(f"Starting {Config.APP_NAME} on http://{Config.HOST}:{Config.PORT} (Debug: {Config.DEBUG})")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
