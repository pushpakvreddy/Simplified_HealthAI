import pennylane as qml
from pennylane import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import mlflow
import os
import joblib

# Create models directory if not exists
os.makedirs('models/saved_models', exist_ok=True)

# Define Quantum Device
n_qubits = 4
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def circuit(weights, features):
    # Data Embedding (use first 4 features for simplicity)
    qml.AngleEmbedding(features, wires=range(n_qubits))
    
    # Variational Layers
    qml.StronglyEntanglingLayers(weights, wires=range(n_qubits))
    
    return qml.expval(qml.PauliZ(0))

def variational_classifier(weights, bias, x):
    return circuit(weights, x) + bias

def loss_func(weights, bias, X, Y):
    predictions = np.array([variational_classifier(weights, bias, x) for x in X])
    # Convert PAuliZ expval [-1, 1] to [0, 1] for binary loss
    predictions = (predictions + 1) / 2
    return np.mean((predictions - Y) ** 2)

def train_qml_model():
    # 1. Load Data
    df = pd.read_csv('datasets/health_data.csv')
    # QML is slow, use a smaller subset for demonstration if needed, 
    # but for 500 rows it might be okay. Let's use 100 rows for speed in demo.
    df_small = df.sample(100, random_state=42)
    X = df_small.drop('disease_risk', axis=1).values
    y = df_small['disease_risk'].values
    
    # 2. Preprocessing
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # Reduce to 4 features for the 4-qubit circuit
    X_qml = X_scaled[:, :4] 
    
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_qml, y, test_size=0.2, random_state=42)
    
    # 4. Initialize weights
    n_layers = 2
    weights_shape = qml.StronglyEntanglingLayers.shape(n_layers=n_layers, n_wires=n_qubits)
    weights = np.random.random(weights_shape, requires_grad=True)
    bias = np.array(0.0, requires_grad=True)
    
    # 5. Optimization
    opt = qml.AdamOptimizer(stepsize=0.1)
    batch_size = 5
    
    mlflow.set_experiment("Health_AI_QML_Models")
    
    with mlflow.start_run(run_name="QML_Variational_Run"):
        print("Starting QML training...")
        for it in range(20): # 20 iterations for demo
            # Batching
            batch_index = np.random.randint(0, len(X_train), (batch_size,))
            X_batch = X_train[batch_index]
            y_batch = y_train[batch_index]
            
            weights, bias, _, _ = opt.step(loss_func, weights, bias, X_batch, y_batch)
            
            if (it + 1) % 5 == 0:
                loss = loss_func(weights, bias, X_train, y_train)
                print(f"Iter {it+1}: Loss = {loss:.4f}")
        
        # Evaluation
        predictions = np.array([variational_classifier(weights, bias, x) for x in X_test])
        predictions = ((predictions + 1) / 2 > 0.5).astype(int)
        acc = np.mean(predictions == y_test)
        print(f"QML Model Accuracy: {acc:.4f}")
        
        mlflow.log_param("n_qubits", n_qubits)
        mlflow.log_param("n_layers", n_layers)
        mlflow.log_metric("accuracy", acc)
        
        # Save Model Artifacts
        qml_data = {
            'weights': weights.numpy(),
            'bias': bias.numpy(),
            'n_qubits': n_qubits,
            'n_layers': n_layers
        }
        joblib.dump(qml_data, 'models/saved_models/qml_model_data.joblib')
        joblib.dump(scaler, 'models/saved_models/qml_scaler.joblib')
        
        # Log to mlflow as artifact
        mlflow.log_artifact('models/saved_models/qml_model_data.joblib')
        print("QML Model saved to models/saved_models/qml_model_data.joblib")

if __name__ == "__main__":
    train_qml_model()
