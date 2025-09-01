from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from backend.db.db import init_db, ensure_user, insert_event, insert_daily_report, query_events
from backend.models.features import build_recent_window_features
from backend.models.predictor import Predictor
from backend.alerts.rules import combine, should_alert
from backend.alerts.notifier import send_local_notification

app = FastAPI()
init_db()
P = Predictor()

class ReportIn(BaseModel):
    anon_id: str
    date: str
    sleep_hours: float = None
    stress: int = None
    urges: list = []
    app_usage: dict = {}
    notes: str = ''

class EventIn(BaseModel):
    anon_id: str
    ts: str
    event_type: str
    payload: dict = {}

@app.get('/health')
async def health():
    return {'ok': True, 'version': '0.1'}

@app.post('/ingest/report')
async def ingest_report(r: ReportIn):
    user_id = ensure_user(r.anon_id)
    insert_daily_report(user_id, r.date, r.dict())
    # also convert urges into events
    for u in r.urges:
        ts = u.get('ts')
        intensity = u.get('intensity', None)
        insert_event(user_id, ts, 'urge', {'intensity': intensity})
    return {'status': 'ok'}

@app.post('/ingest/event')
async def ingest_event(e: EventIn):
    user_id = ensure_user(e.anon_id)
    insert_event(user_id, e.ts, e.event_type, e.payload)
    return {'status': 'ok'}

@app.get('/predict')
async def predict(anon_id: str, now_ts: str = None):
    now_ts = now_ts or datetime.utcnow().isoformat()
    user_id = ensure_user(anon_id)
    feats = build_recent_window_features(user_id, now_ts)
    out = P.predict(feats)
    rule = combine(out['prob'])
    if should_alert(rule):
        # send a notification (non-blocking)
        try:
            send_local_notification('Urge Risk', f"Risk {out['prob']:.2f}; Tier {rule['tier']}")
        except Exception:
            pass
    return {'features': feats, 'prediction': out, 'rule': rule}
