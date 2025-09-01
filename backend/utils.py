# backend/utils.py
"""
Utility functions for Urge Predictor backend:
- Paths
- Preprocessing
- Logging
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime

# ----------------------
# Paths
# ----------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_FILENAME = "urge_data.db"
MODEL_FILENAME = "default_model.joblib"

def get_db_path():
    return os.path.join(BASE_DIR, DB_FILENAME)

def get_model_path():
    return os.path.join(BASE_DIR, "models", MODEL_FILENAME)

# ----------------------
# Preprocessing
# ----------------------
def preprocess_features(df: pd.DataFrame) -> np.ndarray:
    """
    Normalize numeric features (z-score).
    """
    return (df - df.mean()) / (df.std() + 1e-8)

# ----------------------
# Logging
# ----------------------
def log(msg: str):
    """
    Print log with timestamp (can be extended to file logging).
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")
