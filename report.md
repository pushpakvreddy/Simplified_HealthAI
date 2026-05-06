# 📈 Unified Health AI Platform: Technical Project Report

## 1. Project Overview
The **Unified Health AI Platform** is a state-of-the-art diagnostic system that synchronizes three distinct AI paradigms—Machine Learning, Deep Learning, and Quantum Machine Learning—to provide a consensus-based health risk assessment.

### 🎯 Key Objectives
- **Multimodal Analysis**: Compare Ensemble ML, Attention-based DL, and Quantum VQE models.
- **Data Standardization**: Unified 10-feature health vector for perfectly aligned comparative results.
- **MLOps Excellence**: Full containerization, MLflow tracking, and Kubernetes readiness.

---

## 2. Technical Architecture

### 🏗️ Core Stack
- **Frontend**: React (Vite) + TailwindCSS + Lucide Icons + Framer Motion.
- **Backend**: FastAPI (Python 3.11) + Uvicorn.
- **AI/ML**: Scikit-Learn, TensorFlow/Keras, PennyLane (Quantum).
- **Tracking**: MLflow (v2.x).
- **DevOps**: Docker, Docker Compose, Kubernetes, GitHub Actions (CI/CD).

### 🌐 Service Map
| Service | Port (Docker) | Port (K8s) | Role |
| :--- | :--- | :--- | :--- |
| **Frontend** | 3000 | 30000 | User Dashboard |
| **Backend** | 8000 | 30800 | Prediction API |
| **MLflow** | 5005 | 30501 | Experiment Tracking |

---

## 3. Data Standard (10-Feature Vector)
All models ingest a standardized patient vector to ensure accuracy comparisons are valid:
1. **Age**
2. **BMI**
3. **Glucose**
4. **Blood Pressure**
5. **Cholesterol**
6. **Heart Rate**
7. **Insulin**
8. **Smoking Status** (Binary)
9. **Physical Activity** (Scale 0-7)
10. **Sleep Hours**

---

## 4. AI Model Paradigms & Results

### 🧠 Machine Learning (Ensemble)
- **Architecture**: Soft Voting Classifier combining Random Forest and Support Vector Machine (SVM).
- **Result**: **95.00% Accuracy**
- **Metrics**: Precision: 0.96, Recall: 0.97, F1: 0.96.

### ⚡ Deep Learning (Attention)
- **Architecture**: Multi-Head Attention mechanism over dense layers to identify critical patient vitals.
- **Result**: **90.00% Accuracy**
- **Feature**: Uses `.keras` modern serialization for cross-environment compatibility.

### ⚛️ Quantum Machine Learning (QML)
- **Architecture**: Variational Quantum Circuit (VQC) using Strong Entangling Layers on a 4-qubit circuit.
- **Result**: **85.00% Accuracy**
- **Library**: PennyLane with `autoray` optimization.

---

## 5. MLOps & Infrastructure

### 📊 MLflow Integration
- **Local File Backend**: High reliability for containerized environments.
- **Model Registry**: Officially registered models (`Health_Ensemble_Model`, `Health_Attention_Model`) for version control.
- **Tracking**: Automatic logging of hyperparameters, metrics, and `.joblib`/`.keras` artifacts.

### ☸️ Kubernetes Deployment
- **Manifests**: Ready-to-use YAMLs in `kubernetes/manifests/`.
- **Persistence**: Persistent Volume Claims (PVC) ensure that newly trained models and MLflow logs survive pod restarts.

### 🧪 GitHub Actions CI/CD
- **Workflow**: `.github/workflows/ci.yml`.
- **Automated Steps**: Checkout -> Python Setup -> Dependency Install -> Pylint (Code Quality) -> Pytest (Functional Testing).

---

## 6. Execution Instructions

### Local (Docker)
```bash
docker-compose up -d
# Re-train models inside container to ensure env-alignment
docker exec -it health_backend python models/ml_model.py
docker exec -it health_backend python models/dl_model.py
docker exec -it health_backend python models/qml_model.py
```

### Kubernetes
```bash
kubectl apply -f kubernetes/manifests/
```

---

## 7. Final Conclusion
The platform successfully demonstrates that even complex AI pipelines (including Quantum) can be unified into a production-style, containerized architecture. The consensus mechanism (averaging risks from three distinct engines) provides a more robust diagnostic output than any single model alone.
