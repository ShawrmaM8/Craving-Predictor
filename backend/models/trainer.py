# backend/models/trainer.py
"""
Trainer script for Urge Predictor.
- Loads past reports/events from DB
- Builds features & labels
- Trains + evaluates a Logistic Regression model
- Saves trained model to disk
"""

import os
import sqlite3
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, brier_score_loss
import joblib

from backend.utils import get_db_path, get_model_path, preprocess_features, log

DB_PATH = get_db_path()
MODEL_PATH = get_model_path()

def load_data():
    """Load labeled data from DB."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM reports", conn)
    conn.close()

    if df.empty:
        raise ValueError("No reports found in DB to train model.")

    # Create labels: simplistic rule — if stress high & sleep low → label 1 (urge risk)
    df["label"] = ((df["stress_level"] > 6) & (df["sleep_hours"] < 6)).astype(int)

    features = df[["sleep_hours", "stress_level", "productivity_score", "exercise_minutes"]]
    labels = df["label"]

    return preprocess_features(features), labels


def train_and_evaluate():
    """Train Logistic Regression, evaluate, and save model."""
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_train, y_train)

    # Evaluation
    y_probs = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_probs)
    brier = brier_score_loss(y_test, y_probs)

    log(f"Model trained. AUC={auc:.3f}, Brier={brier:.3f}")

    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return {"auc": auc, "brier": brier, "model_path": MODEL_PATH}


if __name__ == "__main__":
    results = train_and_evaluate()
    print("✅ Training complete:", results)
