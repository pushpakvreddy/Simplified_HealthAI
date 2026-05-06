# 📈 Full MLflow Tracking Implementation

This project uses **MLflow** for robust MLOps experiment tracking. Every time a model is trained, its performance, parameters, and versioned artifacts are stored automatically.

## 🚀 How it Works in this Project

1. **Centralized Tracking**: All models (`ML`, `DL`, `QML`) are configured to log to the same shared `mlruns/` directory.
2. **Experiment Separation**: 
   - `Health_AI_ML_Models`: Tracks the RandomForest + SVM Ensemble.
   - `Health_AI_DL_Models`: Tracks the Attention-based Neural Network.
   - `Health_AI_QML_Models`: Tracks the Variational Quantum Circuit.
3. **Artifact Persistence**: The trained models (`.joblib`, `.keras`) are saved as artifacts within MLflow, allowing you to "time-travel" back to any previous version of a model.

## 🛠️ Logging Details

For every training run, the platform captures:

| Category | Logged Items | Description |
|----------|--------------|-------------|
| **Parameters** | `model_type`, `n_layers`, `epochs`, `n_qubits` | The configuration used for the run. |
| **Metrics** | `accuracy`, `precision`, `recall`, `f1_score`, `loss` | Quantitative performance of the model. |
| **Artifacts** | `ensemble_model`, `attention_model`, `scaler.joblib` | The actual serialized model files. |

## 🌐 Launching the MLflow UI

The MLflow UI is integrated into the Docker ecosystem and starts automatically.

1. **Access the Dashboard**:
   Open your browser and go to:
   [**http://localhost:5001**](http://localhost:5001)

2. **Key Features**:
   - **Comparison**: Select multiple runs and click "Compare" to see side-by-side performance tables.
   - **Inspection**: Click on a run to see detailed charts of loss vs. epochs (for DL).
   - **Download**: Go to the "Artifacts" section of a run to download the model file for deployment.

## 🏃 Running New Experiments

To trigger a new tracked experiment, run the training scripts:

### Via Local Environment:
```bash
python models/ml_model.py
python models/dl_model.py
python models/qml_model.py
```

### Via Docker:
```bash
docker exec -it health_backend python models/ml_model.py
```

## 📂 Structure
- `mlruns/`: The local database where all experiment data is stored. **Do not delete this folder if you want to keep your history.**
- `mlflow_setup.md`: This documentation.
