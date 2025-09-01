# Simple SQLite helper using sqlite3
import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / 'data.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA_PATH = Path(__file__).resolve().parents[0] / 'schema.sql'

def get_conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# simple helper functions
def ensure_user(anon_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE anon_id=?', (anon_id,))
    row = cur.fetchone()
    if row:
        uid = row['id']
    else:
        cur.execute('INSERT INTO users(anon_id) VALUES(?)', (anon_id,))
        uid = cur.lastrowid
        conn.commit()
    conn.close()
    return uid

def insert_event(user_id, ts, event_type, payload):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO events(user_id, ts, event_type, payload_json) VALUES(?,?,?,?)',
                (user_id, ts, event_type, json.dumps(payload)))
    conn.commit()
    conn.close()

def insert_daily_report(user_id, date, report):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO daily_reports(user_id, date, report_json) VALUES(?,?,?)',
                (user_id, date, json.dumps(report)))
    conn.commit()
    conn.close()

def query_events(user_id, start_ts=None, end_ts=None):
    conn = get_conn()
    cur = conn.cursor()
    if start_ts and end_ts:
        cur.execute('SELECT * FROM events WHERE user_id=? AND ts BETWEEN ? AND ? ORDER BY ts ASC',
                    (user_id, start_ts, end_ts))
    elif start_ts:
        cur.execute('SELECT * FROM events WHERE user_id=? AND ts>=? ORDER BY ts ASC', (user_id, start_ts))
    else:
        cur.execute('SELECT * FROM events WHERE user_id=? ORDER BY ts ASC', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]