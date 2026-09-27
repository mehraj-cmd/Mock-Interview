import sqlite3
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = os.path.join(os.path.dirname(__file__), 'interview_data.db')


def init_db():
    """Initializes the SQLite database and creates all tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            saved_resume TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Interview sessions table (linked to user)
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            interview_type TEXT,
            role TEXT,
            resume_data TEXT,
            overall_score REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Q&A records table
    c.execute('''
        CREATE TABLE IF NOT EXISTS qa_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            question TEXT,
            answer TEXT,
            score REAL,
            feedback TEXT,
            improvement_tip TEXT,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    ''')

    conn.commit()
    conn.close()


# ── User helpers ──────────────────────────────────────────────────────────────

def create_user(name, email, password):
    """Creates a new user. Returns the user id, or None if email is taken."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        pw_hash = generate_password_hash(password)
        c.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                  (name, email, pw_hash))
        user_id = c.lastrowid
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_user_by_email(email):
    """Returns the user row dict or None."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    """Returns the user row dict or None."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def verify_password(email, password):
    """Returns user dict if credentials are correct, else None."""
    user = get_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None


def save_user_resume(user_id, resume_text):
    """Saves/updates the user's stored resume text."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE users SET saved_resume = ? WHERE id = ?', (resume_text, user_id))
    conn.commit()
    conn.close()


def update_user_name(user_id, name):
    """Updates the user's display name."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))
    conn.commit()
    conn.close()


# ── Session helpers ───────────────────────────────────────────────────────────

def create_session(interview_type, role, resume_data, user_id=None):
    """Creates a new interview session in the DB and returns its ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        'INSERT INTO sessions (user_id, interview_type, role, resume_data) VALUES (?, ?, ?, ?)',
        (user_id, interview_type, role, json.dumps(resume_data))
    )
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id


def update_session_score(session_id, overall_score):
    """Stores the final overall score on a session row."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE sessions SET overall_score = ? WHERE id = ?', (overall_score, session_id))
    conn.commit()
    conn.close()


def get_session(session_id):
    """Returns (interview_type, role, resume_data) for a session."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT interview_type, role, resume_data FROM sessions WHERE id = ?', (session_id,))
    row = c.fetchone()
    conn.close()
    if row:
        interview_type, role, resume_json = row
        return interview_type, role, json.loads(resume_json) if resume_json else {}
    return None, None, {}


def get_user_sessions(user_id):
    """Returns all interview sessions for a user, newest first."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT id, interview_type, role, overall_score, created_at
        FROM sessions
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_qa_record(session_id, question, answer, score, feedback, improvement_tip):
    """Saves a graded Q&A record tied to a specific session."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO qa_records (session_id, question, answer, score, feedback, improvement_tip)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session_id, question, answer, score, feedback, improvement_tip))
    conn.commit()
    conn.close()


def get_qa_records(session_id):
    """Returns all graded Q&A records for a session."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        'SELECT question, answer, score, feedback, improvement_tip FROM qa_records WHERE session_id = ?',
        (session_id,)
    )
    rows = c.fetchall()
    conn.close()
    return [{'question': q, 'answer': a, 'score': s, 'feedback': f, 'tip': t}
            for q, a, s, f, t in rows]
