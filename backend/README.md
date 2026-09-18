# VeraFace Backend – Phase 2

Minimal, modular, and runnable Flask backend for the **AI Fake Face Detection and Trust Verification Platform (VeraFace)**.  
Includes service health monitoring and a mock inference endpoint (`/api/predict`) operating in **DEMO/MOCK mode**.

---

## 🚀 Overview

Phase 2 capabilities:
- **Application Factory**: Pattern (`create_app`) in `app/main.py`.
- **Health Check**: `GET /health` endpoint verifying service liveness.
- **Mock Inference API**: `POST /api/predict` handling `multipart/form-data` uploads.
- **Image Validation**: Size bounds (<= 5 MB), MIME inspection (JPEG/PNG), and file integrity verification.
- **Deterministic Mock Model**: Computes reproducible real/fake probabilities, confidence scores, and heuristic trust scores based on image features.
- **Visual Explainability Placeholders**: Synthetic base64 PNG data URIs for Grad-CAM heatmaps and LIME superpixel segmentations.

---

## 🛠️ Setup & Running (Windows PowerShell)

Follow these steps from the project root:

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

### 6. Run automated test suite
```powershell
pytest
```

---

## 🔍 API Endpoints & Usage

Once started, the Flask server listens on `http://127.0.0.1:5000`.

### 1. Health Check (`GET /health`)
```powershell
curl http://127.0.0.1:5000/health
```

**Response**:
```json
{
  "app": "VeraFace Backend",
  "model_loaded": false,
  "status": "ok"
}
```

---

### 2. POST /api/predict (Mock Inference – VeraFace)

Accepts an image upload in `multipart/form-data` format and returns a complete, schema-compliant verification result.

#### Request Example (cURL):
```powershell
curl -X POST http://127.0.0.1:5000/api/predict -F "image=@sample_face.png"
```

#### Request Example (PowerShell):
```powershell
$form = @{ image = Get-Item "path\to\sample_face.png" }
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/predict" -Method Post -Form $form
```

#### Successful Response (HTTP 200):
```json
{
  "success": true,
  "verification_id": "v_1726656000_3a4b5c",
  "timestamp": "2026-09-18T10:45:00.000000+00:00",
  "prediction": "Fake",
  "real_probability": 0.12,
  "fake_probability": 0.88,
  "confidence_score": 88.0,
  "trust_score": 84.2,
  "message": "VeraFace mock prediction (DEMO mode). Not a real AI detection.",
  "gradcam_image": "data:image/png;base64,iVBORw0KGgo...",
  "lime_image": "data:image/png;base64,iVBORw0KGgo...",
  "face_detected": true,
  "faces_count": 1,
  "warnings": [
    "Mock inference (DEMO mode)"
  ]
}
```

#### Validation Error Response (HTTP 400):
```json
{
  "success": false,
  "error": "Unsupported file extension. Allowed extensions: .jpg, .jpeg, .png."
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
│   ├── routes/             # Blueprint routes
│   │   ├── __init__.py
│   │   ├── health.py       # Health check route (/health)
│   │   └── predict.py      # Face prediction route (/api/predict)
│   ├── services/           # Service layer
│   │   ├── __init__.py
│   │   └── inference_mock.py # Mock AI prediction & XAI generation
│   └── utils/              # Helper utilities
│       ├── __init__.py
│       └── image_utils.py  # Image validation & decoding
├── model/                  # AI model weights (Phase 3+)
├── uploads/                # Ephemeral image upload directory
├── reports/                # Generated verification reports
├── tests/                  # Automated test suite
│   ├── test_health.py      # Health endpoint tests
│   └── test_predict_mock.py# Prediction endpoint tests
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
├── run.py                  # Local dev server entrypoint
├── .env.example            # Environment variables template
└── README.md               # Backend documentation and run instructions
```
