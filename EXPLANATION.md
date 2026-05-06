# Project Explanation & Technical Details

This document explains the architecture and implementation details of the Unified Health AI Platform.

## 📊 Dataset Loading
All models load the shared dataset from:
`datasets/health_data.csv`

**Line References:**
- `models/ml_model.py`: Line 21 (`df = pd.read_csv('datasets/health_data.csv')`)
- `models/dl_model.py`: Line 36 (`df = pd.read_csv('datasets/health_data.csv')`)
- `models/qml_model.py`: Line 33 (`df = pd.read_csv('datasets/health_data.csv')`)

## 🧠 AI Models

### 1. Machine Learning (Ensemble)
- **Algorithm**: Soft-voting ensemble of RandomForestClassifier and SVC.
- **Why**: Combines the bagging strength of RF with the margin maximization of SVM for robust performance on small datasets.

### 2. Deep Learning (Attention)
- **Architecture**: Dense -> Attention -> Dense.
- **Why**: The attention mechanism allows the model to weigh different health features dynamically, highlighting the most significant risk factors.

### 3. Quantum Machine Learning (QML)
- **Framework**: PennyLane.
- **Architecture**: Variational Quantum Circuit (VQC) with 4 qubits.
- **Process**:
    1. `AngleEmbedding`: Encodes classical health features into quantum states.
    2. `StronglyEntanglingLayers`: Applies parameterized rotations and entangling gates.
    3. `PauliZ` Measurement: Extracts the expectation value to produce a prediction.

## 🌐 API Flow
1. **Frontend**: Collects 10 health features from the user.
2. **Backend**: Receives features via `POST /analyze`.
3. **Inference**:
    - Preprocesses data using saved `StandardScaler` objects.
    - Runs prediction on all three models concurrently.
    - Calculates a consensus/average risk score.
4. **Response**: Returns a JSON object with individual model results and a comparison summary.

## 📈 MLflow Integration
Each training script initializes an experiment and logs:
- **Params**: Model type, layers, hyperparameters.
- **Metrics**: Accuracy, Precision, Recall, F1.
- **Artifacts**: Saved `.joblib` and `.h5` model files.
