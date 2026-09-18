# TrueFace Backend – Phase 1

Minimal and modular Flask backend skeleton exposing a `/health` endpoint for the **AI Fake Face Detection and Trust Verification Platform (TrueFace)**.

---

## 🚀 Overview

Phase 1 provides:
- Application factory pattern (`create_app`) in `app/main.py`.
- Centralized configuration with environment variable support in `app/config.py`.
- Modular route blueprint structure (`app/routes/health.py`).
- Development server entrypoint (`run.py`).

---

## 🛠️ Setup & Running (Windows PowerShell)

Follow these steps from the root of the project:

### 1. Navigate to the backend directory
```powershell
cd backend
```

### 2. Create and activate a Python virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

### 3. Install required dependencies
```powershell
pip install -r requirements.txt
```

### 4. (Optional) Configure environment variables
You can copy `.env.example` to `.env` to customize settings:
```powershell
copy .env.example .env
```

### 5. Start the development server
```powershell
python run.py
```

---

## 🔍 Expected Behavior & Verification

Once started, the Flask server will listen on `http://127.0.0.1:5000`.

### Health Check Endpoint
Send an HTTP GET request to verify the service status:

```powershell
curl http://127.0.0.1:5000/health
```

Or in PowerShell:
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/health
```

### Expected Response:
```json
{
  "app": "TrueFace Backend",
  "model_loaded": false,
  "status": "ok"
}
```

---

## 📂 Backend Directory Structure

```text
backend/
├── app/
│   ├── __init__.py         # Package init exposing create_app
│   ├── main.py             # Flask application factory
│   ├── config.py           # Configuration settings
│   └── routes/             # Blueprint routes
│       ├── __init__.py
│       └── health.py       # Health check route (/health)
├── model/                  # AI model checkpoints & definitions (Phase 2+)
├── uploads/                # Ephemeral image upload directory
├── reports/                # Generated verification reports
├── tests/                  # Automated test cases
├── requirements.txt        # Python package dependencies
├── run.py                  # Local dev server entrypoint
├── .env.example            # Environment variables template
└── README.md               # Backend documentation and run instructions
```
