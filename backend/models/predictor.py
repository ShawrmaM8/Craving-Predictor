# lightweight predictor: either load a saved sklearn pipeline or return safe defaults
import joblib
from pathlib import Path
import numpy as np

MODEL_PATH = Path(__file__).resolve().parents[2] / 'models' / 'default_model.joblib'
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

class Predictor:
    def __init__(self, model_path=None):
        self.model_path = model_path or MODEL_PATH
        self.model = None
        self._load()

    def _load(self):
        try:
            self.model = joblib.load(self.model_path)
        except Exception:
            self.model = None

    def predict(self, feature_dict):
        # returns {'prob': float, 'explanation': {...}}
        # If model missing, return heuristic probability
        if not self.model:
            # simple heuristic: more urges in window = higher prob
            uc = feature_dict.get('urge_count_60m', 0)
            ts = feature_dict.get('time_since_last_urge_min', 9999)
            base = min(0.05 + 0.2*uc + (0.5 if ts<30 else 0.0), 0.98)
            return {'prob': float(base), 'explanation': {'heuristic': True, 'features': feature_dict}}
        # prepare vector: order by sorted keys
        keys = sorted(feature_dict.keys())
        x = np.array([feature_dict[k] for k in keys], dtype=float).reshape(1, -1)
        prob = float(self.model.predict_proba(x)[0,1])
        # small permutation importance explanation (cheap)
        return {'prob': prob, 'explanation': {'heuristic': False, 'keys': keys}}

    def save(self, model):
        joblib.dump(model, self.model_path)
        self.model = model