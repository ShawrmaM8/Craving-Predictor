# backend/predictor.py
"""
Urge Predictor - loads model and predicts relapse risk
"""

import os
import joblib
import numpy as np
from backend.utils import get_model_path, preprocess_features, log

MODEL_PATH = get_model_path()

class Predictor:
    def __init__(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            log(f"Loaded model from {MODEL_PATH}")
        else:
            self.model = None
            log("⚠️ No model found. Run trainer.py first.")

    def predict(self, report: dict) -> float:
        """
        Given a daily report, predict risk score (0–1).
        """
        if self.model is None:
            return 0.5  # Neutral fallback

        features = {
            "sleep_hours": report.get("sleep_hours", 7),
            "stress_level": report.get("stress_level", 5),
            "productivity_score": report.get("productivity_score", 5),
            "exercise_minutes": report.get("exercise_minutes", 0),
        }

        X = preprocess_features(np.array([list(features.values())]))
        prob = self.model.predict_proba(X)[0, 1]
        return float(prob)
