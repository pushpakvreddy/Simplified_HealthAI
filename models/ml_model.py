import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
import joblib
import os

# Create models directory if not exists
os.makedirs('models/saved_models', exist_ok=True)

def train_ml_model():
    # 1. Load Data
    df = pd.read_csv('datasets/health_data.csv')
    X = df.drop('disease_risk', axis=1)
    y = df['disease_risk']
    
    # 2. Preprocessing
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # 4. Ensemble Model (RandomForest + SVM)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    svm = SVC(probability=True, random_state=42)
    
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('svm', svm)],
        voting='soft'
    )
    
    # 5. MLflow Tracking
    mlflow.set_experiment("Health_AI_ML_Models")
    
    with mlflow.start_run(run_name="ML_Ensemble_Run"):
        ensemble.fit(X_train, y_train)
        y_pred = ensemble.predict(X_test)
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"ML Model Accuracy: {acc:.4f}")
        print(f"ML Model Precision: {prec:.4f}")
        print(f"ML Model Recall: {rec:.4f}")
        print(f"ML Model F1-Score: {f1:.4f}")
        
        # Log to MLflow
        mlflow.log_param("model_type", "Ensemble (RF+SVM)")
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)
        mlflow.log_metric("f1_score", f1)
        
        # Save Model and Scaler
        joblib.dump(ensemble, 'models/saved_models/ml_ensemble_model.joblib')
        joblib.dump(scaler, 'models/saved_models/ml_scaler.joblib')
        
        mlflow.sklearn.log_model(ensemble, "ensemble_model", registered_model_name="Health_Ensemble_Model")
        print("ML Model saved to models/saved_models/ml_ensemble_model.joblib")

if __name__ == "__main__":
    train_ml_model()
