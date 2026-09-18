# System Architecture & Technical Specification

## Project: AI Fake Face Detection and Trust Verification Platform
**Mobile Application**: VeraFace  
**Academic Context**: B.Tech Final-Year EPICS Capstone Project  
**Document Version**: 1.0 (Phase 0 Baseline)

---

## 1. System Overview

The **AI Fake Face Detection and Trust Verification Platform** is designed as a client-server distributed system. The user interacts through a modern mobile application (**VeraFace**), while compute-heavy deep learning inference, explainability generation, and report compilation run on a containerized or virtualized Python/Flask backend.

```text
┌────────────────────────────────────────────────────────┐
│               VeraFace Mobile App (Flutter)            │
│  [Camera / Gallery] ──► [Preview] ──► [Results / XAI]  │
└───────────────────────────┬────────────────────────────┘
                            │  HTTPS / REST (JSON + Multipart)
                            ▼
┌────────────────────────────────────────────────────────┐
│             Flask REST Backend (Python 3.10+)          │
│  • Request Validation & Rate Limiting                  │
│  • Ephemeral Image Storage (/uploads)                  │
│  • Mode Switch (MOCK_MODE vs REAL_MODEL)               │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│               AI Inference & Explainability            │
│  1. Face Detection & Preprocessing (OpenCV / MTCNN)    │
│  2. Hybrid DeFaX Model (EfficientNet-B0 + Swin-T)      │
│  3. Temperature Scaling Probability Calibration        │
│  4. Trust Score Formulation Engine                     │
│  5. Visual Attribution: Grad-CAM & LIME                │
│  6. PDF Verification Report Generator                  │
└────────────────────────────────────────────────────────┘
```

### End-to-End Workflow:
1. **Acquisition**: The user captures a photo via device camera or selects an existing portrait from the gallery in **VeraFace**.
2. **Transmission**: The app packages the image file into a `multipart/form-data` HTTP POST request to the `/api/predict` endpoint.
3. **Ingestion & Validation**: The Flask server checks MIME type, payload size (up to 10 MB), and saves the image to a temporary UUID-keyed storage path.
4. **AI Inference & Explanation**:
   - The face region is cropped, normalized, and evaluated by the hybrid DeFaX neural network.
   - Raw logits are converted to calibrated confidence probabilities.
   - A multi-factor Trust Score is computed.
   - Heatmaps (Grad-CAM) and perturbation masks (LIME) are rendered.
5. **Response Delivery**: The server returns a structured JSON payload containing the classification (`Real` or `Fake`), confidence percentage, trust score, base64/URL links to heatmaps, and a report generation ID.
6. **Presentation**: VeraFace renders the results on an intuitive verdict screen with visual interactive explanation overlays and an option to download the PDF report.

---

## 2. AI Model Pipeline (DeFaX-Style Hybrid Architecture)

State-of-the-art generative models (e.g., StyleGAN2, StyleGAN3, Latent Diffusion) produce images with highly coherent global anatomy but subtle high-frequency boundary flaws, or conversely, pristine local textures with irregular contextual geometries (such as mismatched earrings or asymmetric pupils). 

To capture both failure modes, this project adopts a **DeFaX-inspired dual-branch hybrid network**:

```text
                     Input Image (224 × 224 × 3)
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
   ┌───────────────────────────┐     ┌───────────────────────────┐
   │ EfficientNet-B0 (CNN)     │     │ Swin Transformer Tiny     │
   │ Captures local textures,  │     │ Captures long-range       │
   │ high-frequency artifacts, │     │ spatial context, global   │
   │ blended edges, skin pores │     │ facial symmetry, anatomy  │
   └─────────────┬─────────────┘     └─────────────┬─────────────┘
                 │ Local Tokens                    │ Global Tokens
                 │ (B, N1, D)                      │ (B, N2, D)
                 └────────────────┬────────────────┘
                                  ▼
                 ┌─────────────────────────────────┐
                 │ Multi-Head Cross-Attention      │
                 │ Queries: CNN Local Features     │
                 │ Keys/Values: Swin Global Context│
                 └────────────────┬────────────────┘
                                  ▼
                 ┌─────────────────────────────────┐
                 │ Feature Concatenation & Pooling │
                 └────────────────┬────────────────┘
                                  ▼
                 ┌─────────────────────────────────┐
                 │ Multi-Layer Perceptron (MLP)    │
                 │ LayerNorm -> Dropout -> Linear  │
                 └────────────────┬────────────────┘
                                  ▼
                    Binary Logits: [z_real, z_fake]
```

### Pipeline Components:
1. **Preprocessing**:
   - Face detection and landmark alignment via Haar cascades / MTCNN.
   - Bounding-box margin expansion (1.2×) to capture synthetic hair/background blending boundaries.
   - Bilinear resizing to $224 \times 224 \times 3$.
   - Z-score normalization using ImageNet statistics ($\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$).
2. **Local Feature Branch (EfficientNet-B0)**:
   - Inverted residual blocks (MBConv) preserve spatial resolution and extract fine-grained frequency artifacts.
3. **Global Context Branch (Swin-Tiny Transformer)**:
   - Shifted-window self-attention models long-range semantic dependencies (pupil geometry, ear alignment, lighting consistency).
4. **Cross-Attention Fusion**:
   - Computes dynamic inter-feature relationships between local convolutional patches and global transformer tokens, emphasizing anomalous regions.
5. **Classification Head**:
   - A 2-layer MLP with GELU activation and dropout producing unnormalized logit outputs: $z = [z_{\text{real}}, z_{\text{fake}}]$.

---

## 3. Confidence Score & Probability Calibration

Modern deep neural networks tend to be poorly calibrated, frequently producing overconfident probabilities ($p > 0.99$) even on ambiguous or adversarial inputs. In forensic verification, raw softmax output does not represent empirical certainty.

### Temperature Scaling Calibration:
Given unnormalized logits $z$, standard softmax computes:

$$\hat{p}_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$$

During Phase 2, post-hoc **Temperature Scaling** is applied using a learned scalar parameter $T > 0$ optimized on the validation set by minimizing negative log-likelihood (NLL):

$$\hat{q}_i = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}$$

- When $T > 1$, the softmax distribution softens, smoothing overconfidence.
- The argmax prediction is invariant to $T$, ensuring classification accuracy is strictly preserved while alignment with empirical accuracy is established.

---

## 4. Trust Score (Project-Defined Reliability Indicator)

> [!IMPORTANT]
> **Academic Note**: The **Trust Score** is a *project-defined heuristic metric* engineered to give end-users a single intuitive reliability rating (0–100%). It reflects the system's operational certainty and data quality—it is **not** an absolute guarantee of legal truth.

### Planned Formulation:
$$\text{Trust Score} = w_1 \cdot C_{\text{calibrated}} + w_2 \cdot Q_{\text{face}} + w_3 \cdot S_{\text{stability}}$$

Where:
- $C_{\text{calibrated}} \in [0, 100]$: Calibrated prediction confidence for the predicted class.
- $Q_{\text{face}} \in [0, 100]$: Face quality assessment score (computed using Laplacian variance for blur/sharpness, lighting uniformity, and face resolution).
- $S_{\text{stability}} \in [0, 100]$: Prediction consistency under minor perturbations (e.g., mild Gaussian blur or horizontal flip test-time augmentation).
- Default weights: $w_1 = 0.50$, $w_2 = 0.30$, $w_3 = 0.20$ ($\sum w_i = 1.0$).

### Interpretation Thresholds:
- **85 – 100%**: High Reliability (optimal face resolution, clear artifacts or pristine authenticity, stable prediction).
- **65 – 84%**: Moderate Reliability (acceptable image quality; secondary verification suggested).
- **< 65%**: Low Reliability (poor resolution, severe blur, or ambiguous features; inconclusive).

---

## 5. Explainable AI (XAI) Framework

To satisfy B.Tech evaluation standards for interpretable AI, predictions are accompanied by dual-modal spatial explanations:

### 1. Grad-CAM (Gradient-weighted Class Activation Mapping)
- **Target**: Final convolutional layer of the EfficientNet-B0 branch.
- **Mechanism**: Calculates the gradients of the predicted class score with respect to feature maps, computing weighted linear combinations followed by ReLU.
- **Output**: A normalized 2D heatmap overlaid onto the original face to highlight areas that steered the classification (e.g., synthetic boundaries around teeth, iris borders, or hair texture).

### 2. LIME (Local Interpretable Model-agnostic Explanations)
- **Target**: Black-box inference over the combined model.
- **Mechanism**: Segments the image into superpixels using SLIC (Simple Linear Iterative Clustering). Randomly perturbs subsets of superpixels and fits a sparse linear surrogate model to quantify positive and negative superpixel contributions.
- **Output**: Visual segment highlights showing positive evidence (supporting the verdict) and negative evidence (contradicting the verdict).

### Mobile Visualization:
VeraFace displays an interactive toggle slider allowing users to slide between the raw image, Grad-CAM heatmap, and LIME superpixel boundaries, complete with an explanation legend.

---

## 6. Backend API Design

The backend is built with Python 3.10 and Flask. It includes a decoupled configuration flag (`APP_MODE=MOCK` vs `APP_MODE=REAL`) enabling full API functionality prior to final model training.

### Core Endpoints:

#### 1. `GET /health`
- **Purpose**: Liveness and service readiness probe.
- **Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "mode": "MOCK",
  "timestamp": "2026-09-18T10:30:00Z"
}
```

#### 2. `POST /api/predict`
- **Content-Type**: `multipart/form-data`
- **Parameters**: `image` (binary image file)
- **Response**:
```json
{
  "request_id": "8f3c7a2b-1a9e-4e6f-b2c3-9d4e5f6a7b8c",
  "prediction": "Fake",
  "confidence_score": 94.8,
  "trust_score": 88.5,
  "metrics": {
    "calibrated_probability": 0.948,
    "raw_probability": 0.982,
    "face_quality_score": 85.0,
    "stability_score": 92.0
  },
  "explanations": {
    "gradcam_url": "/api/explanations/8f3c7a2b.../gradcam.png",
    "lime_url": "/api/explanations/8f3c7a2b.../lime.png"
  },
  "report_url": "/api/report/8f3c7a2b-1a9e-4e6f-b2c3-9d4e5f6a7b8c"
}
```

#### 3. `GET /api/report/<id>`
- **Purpose**: Generates and downloads a branded PDF verification report including timestamps, verdict, confidence, trust breakdown, and visual explanation heatmaps.

---

## 7. VeraFace Mobile Application Overview

VeraFace is an Android-first mobile application written in Flutter (Dart), engineered with clean architecture principles.

### Key Screens & User Journey:
1. **Splash Screen**: App branding, system initialization, backend connectivity check.
2. **Home Screen**: Overview, quick actions, educational cards explaining deepfakes.
3. **Upload / Camera Screen**: Image capture with on-screen face alignment guide or gallery picker.
4. **Preview & Crop Screen**: Face verification, framing confirmation, crop adjustment.
5. **Analysis / Loading Screen**: Animated scanning animation with progressive step indicators ("Detecting Face", "Evaluating Neural Features", "Computing Trust Score").
6. **Result Screen**: Prominent Real/Fake verdict badge, calibrated confidence meter, and trust score gauge.
7. **Explanations Screen**: Interactive image viewer with toggle tabs for Original, Grad-CAM, and LIME overlays.
8. **Report Viewer**: Embedded PDF view with download/share capabilities.
9. **History Screen**: Chronological log of previous scans stored locally via Hive/sqflite.
10. **About & Ethics Screen**: Project motivation, EPICS team credits, limitations disclaimer.

---

## 8. Security, Privacy & Operational Guardrails

- **Ephemeral Storage**: Uploaded images are stored in a dedicated `uploads/` directory with automatic TTL cleanup after 1 hour. No biometric face templates are retained permanently on the server.
- **Input Validation**: Strict MIME inspection (JPEG, PNG only) and 10 MB payload limits to prevent buffer overrun or arbitrary file uploads.
- **Rate Limiting**: Flask-Limiter integration preventing automated abuse (e.g., maximum 30 requests/minute per IP).
- **Data Protection**: Clear privacy policy and disclaimer inside the VeraFace app highlighting that images are processed strictly for real-time verification.
