# AI Fake Face Detection and Trust Verification Platform (TrueFace)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B.svg)](https://flutter.dev/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C.svg)](https://pytorch.org/)

An end-to-end deepfake detection and reliability assessment system comprising a hybrid CNN–Transformer deep learning backend and a user-friendly mobile application named **TrueFace**.

---

## 📌 Problem Statement

With recent breakthroughs in Generative Adversarial Networks (GANs like StyleGAN) and diffusion models, hyper-realistic synthetic face images are increasingly indistinguishable from genuine photographs. While these technologies enable creative applications, malicious actors exploit them for identity theft, social engineering, disinformation campaigns, and financial fraud. 

Existing detection tools often suffer from:
1. **Black-box predictions**: Outputs lacking interpretability or spatial attribution.
2. **Overconfidence**: Miscalibrated models providing high confidence on out-of-distribution or perturbed inputs.
3. **Inaccessibility**: Absence of intuitive, mobile-first verification workflows for everyday users and non-expert investigators.

There is a critical academic and societal need for an accessible, explainable, and calibrated verification platform that not only classifies an image as Real or Fake, but also quantifies prediction reliability and provides visual evidence.

---

## 🎯 Project Objectives

1. **Robust Real vs. Fake Classification**: Accurately detect synthetic facial imagery using a hybrid architecture capturing both local textural artifacts and global structural context.
2. **Calibrated Confidence Scoring**: Mitigate overconfidence via post-hoc calibration (Temperature Scaling) so probabilities reflect true empirical likelihood.
3. **Trust Score Formulation**: Compute a project-defined composite reliability indicator combining calibrated confidence, face image quality, and prediction stability.
4. **Visual Explainability**: Generate visual attribution maps via Grad-CAM (convolutional feature localization) and LIME (interpretable superpixel perturbations).
5. **Automated Verification Reports**: Synthesize classification verdicts, confidence, trust metrics, and visual explanations into downloadable/exportable verification reports (PDF).
6. **Intuitive Mobile Experience (TrueFace)**: Deliver a responsive, Android-first Flutter application allowing users to capture/upload faces, inspect explanations, and maintain scan histories.

---

## 🏗️ High-Level System Architecture

```text
  TrueFace (Flutter Mobile App)
            │
            ▼ HTTPS / HTTP (REST API)
  Flask REST API (Python)
            │
            ▼
  AI Inference Service (PyTorch)
    ├─ DeFaX Model (EfficientNet-B0 + Swin-Tiny + Cross-Attention)
    ├─ Confidence Calibration (Temperature Scaling)
    ├─ Trust Score (Project-defined reliability indicator)
    ├─ Grad-CAM + LIME Explainability Engine
    └─ Verification Report Generator (PDF)
```

The system is decoupled into two independent layers:
- **Client Tier**: Flutter mobile application (`mobile/`) communicating over standard REST JSON contracts.
- **Service Tier**: Python/Flask API (`backend/`) orchestrating image preprocessing, PyTorch inference, explainability engines, and report generation.

---

## 💻 Technology Stack

### Backend & AI Inference
- **Language**: Python 3.10+
- **API Framework**: Flask, Flask-CORS
- **Deep Learning Framework**: PyTorch, Torchvision, `timm` (PyTorch Image Models)
- **Computer Vision & Preprocessing**: OpenCV (`cv2`), Pillow (PIL)
- **Evaluation & Calibration**: scikit-learn, NumPy, SciPy
- **Explainability**: `pytorch-grad-cam`, `lime`
- **Document Generation**: ReportLab / FPDF2

### Mobile Client (TrueFace)
- **Framework**: Flutter (Dart) targeting Android (first-class) & cross-platform
- **Networking**: `http` package with standard REST contracts
- **Image Handling**: `image_picker` for camera and gallery integration
- **Local Persistence**: `hive` / `sqflite` for off-line scan history

### Model Training & Research
- **Framework**: PyTorch with GPU acceleration (CUDA)
- **Experimentation**: Jupyter Notebooks (`model_training/notebooks/`)
- **Dataset Management**: Torchvision datasets and custom PyTorch `Dataset` loaders

---

## 📊 Dataset Strategy

The training and evaluation pipeline utilizes the benchmark **140K Real and Fake Faces Dataset**:
- **Real Faces**: Sampled from the Flickr-Faces-HQ (FFHQ) dataset at high resolution.
- **Fake Faces**: Generated via StyleGAN (NVIDIA research), containing characteristic synthesis artifacts.
- **Dataset Partitioning**:
  - **Training Set**: 100,000 images (50K Real, 50K Fake) — Balanced training.
  - **Validation Set**: 20,000 images (10K Real, 10K Fake) — Hyperparameter tuning and temperature scaling calibration.
  - **Test Set**: 20,000 images (10K Real, 10K Fake) — Unseen evaluation.
- **Cross-Dataset & Generalization Testing**: Planned external validation against secondary datasets (e.g., FaceForensics++, Celeb-DF) to benchmark real-world domain shifts.

---

## 📂 Project Repository Structure

```text
ai-fake-face-platform/
│
├── backend/                  # Flask REST API and AI inference service
│   ├── app/                  # Application factory, routes, and helpers
│   ├── model/                # Model wrappers, weights, and architectures
│   ├── uploads/              # Transient storage for incoming face images
│   ├── reports/              # Generated PDF verification reports
│   └── tests/                # Automated backend unit and integration tests
│
├── mobile/                   # TrueFace Flutter mobile application
│
├── model_training/           # Deep learning model development & training
│   ├── datasets/             # Dataset loaders, manifests, and scripts
│   ├── training/             # PyTorch training loops and configs
│   ├── evaluation/           # Metrics, calibration, and ROC-AUC evaluators
│   └── notebooks/            # Exploratory analysis and prototyping
│
├── docs/                     # Architectural specs, API docs, and guides
│   └── architecture.md       # Detailed technical architecture specification
│
├── .gitignore                # Git ignore configuration
└── README.md                 # Project documentation and setup guide
```

---

## ⚠️ Important Notes & Academic Disclaimers

1. **Trust Score Definition**: The **Trust Score** is a *project-defined reliability indicator* designed to combine model confidence, image quality, and prediction consistency into an interpretable 0–100 index. It is **not** a universal mathematical certainty or legal guarantee of authenticity.
2. **Decoupled Architecture & Mock Mode**: The backend initially operates in **DEMO/MOCK mode**, returning realistic schema-compliant responses. This permits concurrent frontend development and end-to-end testing. When the trained PyTorch model is integrated, the mobile app requires zero code modifications.
3. **Privacy & Ethical Usage**: Uploaded images are processed transiently for verification purposes only, respecting user privacy.

---

## 👥 Contributors & Academic Context

Developed as a **B.Tech Final-Year EPICS (Engineering Projects in Community Service)** Capstone Project.
- **Project Title**: AI Fake Face Detection and Trust Verification Platform
- **Application Name**: TrueFace
- **Target Audience**: Students, researchers, digital forensics investigators, and academic examiners.
