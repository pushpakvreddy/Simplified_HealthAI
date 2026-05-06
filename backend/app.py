from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import tensorflow as tf
import pennylane as qml
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Unified Health AI Platform API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Model Loading Logic ---
MODELS_PATH = 'models/saved_models'

# ML Model
ml_model = None
ml_scaler = None
try:
    if os.path.exists(f'{MODELS_PATH}/ml_ensemble_model.joblib'):
        ml_model = joblib.load(f'{MODELS_PATH}/ml_ensemble_model.joblib')
        ml_scaler = joblib.load(f'{MODELS_PATH}/ml_scaler.joblib')
        print("ML Model loaded successfully.")
except Exception as e:
    print(f"Error loading ML Model: {e}")

# DL Model
dl_model = None
dl_scaler = None
try:
    if os.path.exists(f'{MODELS_PATH}/dl_attention_model.keras'):
        dl_model = tf.keras.models.load_model(f'{MODELS_PATH}/dl_attention_model.keras')
        dl_scaler = joblib.load(f'{MODELS_PATH}/dl_scaler.joblib')
        print("DL Model loaded successfully.")
except Exception as e:
    print(f"Error loading DL Model: {e}")

# QML Model
qml_data = None
qml_scaler = None
try:
    if os.path.exists(f'{MODELS_PATH}/qml_model_data.joblib'):
        qml_data = joblib.load(f'{MODELS_PATH}/qml_model_data.joblib')
        qml_scaler = joblib.load(f'{MODELS_PATH}/qml_scaler.joblib')
        print("QML Model loaded successfully.")
except Exception as e:
    print(f"Error loading QML Model: {e}")

# QML Circuit for Inference
n_qubits = 4
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def qml_circuit_inference(weights, features):
    qml.AngleEmbedding(features, wires=range(n_qubits))
    qml.StronglyEntanglingLayers(weights, wires=range(n_qubits))
    return qml.expval(qml.PauliZ(0))

# --- API Models ---
class PatientFeatures(BaseModel):
    age: float
    bmi: float
    glucose: float
    blood_pressure: float
    cholesterol: float
    heart_rate: float
    insulin: float
    smoking: int
    physical_activity: int
    sleep_hours: float

# --- Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Unified Health AI Platform Backend is running!"}

@app.post("/analyze")
async def analyze_health(features: PatientFeatures):
    data = np.array([[
        features.age, features.bmi, features.glucose, features.blood_pressure,
        features.cholesterol, features.heart_rate, features.insulin,
        features.smoking, features.physical_activity, features.sleep_hours
    ]])

    results = {}

    # ML Inference
    if ml_model and ml_scaler:
        scaled_data = ml_scaler.transform(data)
        ml_pred = ml_model.predict_proba(scaled_data)[0][1]
        results["ml_prediction"] = {
            "risk_score": float(ml_pred),
            "label": "High Risk" if ml_pred > 0.5 else "Low Risk"
        }
    else:
        results["ml_prediction"] = "Model not loaded"

    # DL Inference
    if dl_model and dl_scaler:
        scaled_data = dl_scaler.transform(data)
        dl_pred = dl_model.predict(scaled_data)[0][0]
        results["dl_prediction"] = {
            "risk_score": float(dl_pred),
            "label": "High Risk" if dl_pred > 0.5 else "Low Risk"
        }
    else:
        results["dl_prediction"] = "Model not loaded"

    # QML Inference
    if qml_data and qml_scaler:
        scaled_data = qml_scaler.transform(data)
        qml_features = scaled_data[0][:4] # Use first 4 features
        qml_val = qml_circuit_inference(qml_data['weights'], qml_features) + qml_data['bias']
        qml_risk = float((qml_val + 1) / 2) # Map to [0, 1]
        results["qml_prediction"] = {
            "risk_score": qml_risk,
            "label": "High Risk" if qml_risk > 0.5 else "Low Risk"
        }
    else:
        results["qml_prediction"] = "Model not loaded"

    # Comparison / Conclusion
    scores = []
    if isinstance(results["ml_prediction"], dict): scores.append(results["ml_prediction"]["risk_score"])
    if isinstance(results["dl_prediction"], dict): scores.append(results["dl_prediction"]["risk_score"])
    if isinstance(results["qml_prediction"], dict): scores.append(results["qml_prediction"]["risk_score"])
    
    avg_score = np.mean(scores) if scores else 0
    results["comparison"] = {
        "average_risk": float(avg_score),
        "consensus": "High Risk" if avg_score > 0.5 else "Low Risk",
        "confidence": "High" if len(set([results[m]["label"] for m in results if isinstance(results[m], dict)])) == 1 else "Medium"
    }

    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
