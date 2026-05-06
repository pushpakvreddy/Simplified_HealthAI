import pytest
import os
import pandas as pd

def test_dataset_exists():
    assert os.path.exists('datasets/health_data.csv')
    df = pd.read_csv('datasets/health_data.csv')
    assert len(df) >= 500
    assert 'disease_risk' in df.columns
    assert len(df.columns) == 11 # 10 features + 1 target

def test_model_scripts_exist():
    assert os.path.exists('models/ml_model.py')
    assert os.path.exists('models/dl_model.py')
    assert os.path.exists('models/qml_model.py')

# Note: Integration tests for actual training would be too slow for pytest CI, 
# but we can verify the structure.
