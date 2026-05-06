# Unified Health AI Platform

A clean, standardized full-stack AI platform demonstrating Machine Learning, Deep Learning, and Quantum Machine Learning for health risk prediction.

## 🚀 Overview
This project provides a unified interface to compare predictions from three different AI paradigms:
- **Classical ML**: RandomForest + SVM Ensemble.
- **Deep Learning**: Attention-based Neural Network (Keras).
- **Quantum ML**: Variational Quantum Circuit (PennyLane).

All models are trained on the same `health_data.csv` dataset and tracked using **MLflow**.

## 📁 Structure
- `backend/`: FastAPI server for unified inference.
- `frontend/`: React + Tailwind dashboard.
- `models/`: Python scripts for ML/DL/QML training.
- `datasets/`: Shared health data.
- `tests/`: Pytest suite for API and models.
- `docs/`: Documentation and setup guides.

## 🛠️ Setup & Installation

### 1. Environment Setup
```bash
pip install -r requirements.txt
```

### 2. Generate Data & Train Models
```bash
# Generate synthetic dataset
# (Data is already generated in datasets/health_data.csv)

# Train all models (logs to MLflow)
python models/ml_model.py
python models/dl_model.py
python models/qml_model.py
```

### 3. Run MLflow
The platform uses MLflow for MLOps tracking. View all experiments at:
[http://localhost:5001](http://localhost:5001)

### 4. Run Backend
```bash
uvicorn backend.app:app --reload
```

### 5. Run Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing
```bash
pytest
```

## 📜 License
MIT License
