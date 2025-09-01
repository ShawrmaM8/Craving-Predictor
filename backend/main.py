# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import datetime
import json

from predictor import Predictor
from notifier import Notifier
from database import init_db, get_connection

app = FastAPI(title="Urge Predictor + Alert System")

# initialize DB + helper classes
init_db()
predictor = Predictor()
notifier = Notifier()


# ----------------------------
# Models for request/response
# ----------------------------
class DailyReport(BaseModel):
    sleep_hours: float
    stress_level: int
    productivity_score: int
    exercise_minutes: int
    notes: Optional[str] = None


class PredictionResponse(BaseModel):
    risk_score: float
    message: str
    timestamp: str


class AlertResponse(BaseModel):
    alerts: List[str]


# ----------------------------
# API Routes
# ----------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Urge Predictor API is running 🚀"}


@app.post("/report", response_model=dict)
def submit_report(report: DailyReport):
    """
    Accept daily report, store it in DB, and trigger predictor.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO reports (timestamp, sleep_hours, stress_level, productivity_score, exercise_minutes, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.datetime.now().isoformat(),
            report.sleep_hours,
            report.stress_level,
            report.productivity_score,
            report.exercise_minutes,
            report.notes,
        ),
    )
    conn.commit()
    conn.close()

    return {"status": "success", "message": "Report saved."}


@app.get("/predict", response_model=PredictionResponse)
def get_prediction():
    """
    Generate a risk score prediction using last report(s).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reports ORDER BY id DESC LIMIT 7")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=400, detail="No reports available for prediction.")

    # Simplified feature aggregation (last report only for demo)
    last = rows[0]
    features = {
        "sleep_hours": last[2],
        "stress_level": last[3],
        "productivity_score": last[4],
        "exercise_minutes": last[5],
    }

    score = predictor.predict(features)

    message = "⚠️ High risk of urge. Take action!" if score > 0.6 else "✅ Risk low. Stay steady."
    timestamp = datetime.datetime.now().isoformat()

    return PredictionResponse(risk_score=score, message=message, timestamp=timestamp)


@app.get("/alerts", response_model=AlertResponse)
def get_alerts():
    """
    Return the latest alerts from DB.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT message FROM alerts ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()

    return AlertResponse(alerts=[r[0] for r in rows])


@app.post("/alerts/trigger", response_model=dict)
def trigger_alert(message: str):
    """
    Manually trigger an alert (for testing).
    """
    notifier.send_alert(message)
    return {"status": "success", "message": "Alert triggered."}
