# minimal feature builder
from datetime import datetime, timedelta
import numpy as np
from backend.db.db import query_events


def time_cyc_features(ts):
    dt = datetime.fromisoformat(ts)
    hour = dt.hour + dt.minute/60.0
    return {'hour_sin': np.sin(2*np.pi*hour/24), 'hour_cos': np.cos(2*np.pi*hour/24), 'weekday': dt.weekday()}


def build_recent_window_features(user_id, now_ts, window_minutes=60):
    # simple features: count of 'urge' events in window, time since last urge (min), hour cyc
    end = datetime.fromisoformat(now_ts)
    start = end - timedelta(minutes=window_minutes)
    events = query_events(user_id, start.isoformat(), end.isoformat())
    urge_count = sum(1 for e in events if e['event_type']=='urge')
    last_urge_ts = None
    for e in reversed(events):
        if e['event_type']=='urge':
            last_urge_ts = e['ts']
            break
    time_since_last_urge_min = None
    if last_urge_ts:
        dt_last = datetime.fromisoformat(last_urge_ts)
        time_since_last_urge_min = (end - dt_last).total_seconds()/60.0
    else:
        time_since_last_urge_min = 9999.0
    cyc = time_cyc_features(now_ts)
    features = {
        'urge_count_{}m'.format(window_minutes): urge_count,
        'time_since_last_urge_min': time_since_last_urge_min,
        **cyc
    }
    return features