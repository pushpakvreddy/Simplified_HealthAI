import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import mlflow
import mlflow.tensorflow
import os
import joblib

# Create models directory if not exists
os.makedirs('models/saved_models', exist_ok=True)

def build_attention_model(input_shape):
    inputs = layers.Input(shape=(input_shape,))
    
    # Simple Attention Mechanism
    # We expand dimensions to treat features as a sequence for the attention layer
    x = layers.Reshape((input_shape, 1))(inputs)
    
    # Query, Key, Value for Attention
    query_value_attention_seq = layers.Attention(score_mode='dot')([x, x])
    
    # Flatten and Dense layers
    x = layers.Flatten()(query_value_attention_seq)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(32, activation='relu')(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)
    
    model = models.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_dl_model():
    # 1. Load Data
    df = pd.read_csv('datasets/health_data.csv')
    X = df.drop('disease_risk', axis=1)
    y = df['disease_risk']
    
    # 2. Preprocessing
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # 4. Model Building
    model = build_attention_model(X_train.shape[1])
    
    # 5. MLflow Tracking
    mlflow.set_experiment("Health_AI_DL_Models")
    
    with mlflow.start_run(run_name="DL_Attention_Run"):
        # Log Hyperparams
        mlflow.log_param("epochs", 50)
        mlflow.log_param("batch_size", 16)
        
        history = model.fit(
            X_train, y_train,
            epochs=50,
            batch_size=16,
            validation_split=0.1,
            verbose=0
        )
        
        # Evaluation
        loss, acc = model.evaluate(X_test, y_test, verbose=0)
        print(f"DL Model Accuracy: {acc:.4f}")
        
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("loss", loss)
        
        # Save Model and Scaler
        model.save('models/saved_models/dl_attention_model.keras')
        joblib.dump(scaler, 'models/saved_models/dl_scaler.joblib')
        
        mlflow.tensorflow.log_model(model, "attention_model", registered_model_name="Health_Attention_Model")
        print("DL Model saved to models/saved_models/dl_attention_model.keras")

if __name__ == "__main__":
    train_dl_model()
