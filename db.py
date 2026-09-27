import sqlite3
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = os.path.join(os.path.dirname(__file__), 'interview_data.db')


def init_db():
    """Initializes the SQLite database and creates all tables and migrations if they don't exist."""
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
            default_type TEXT,
            default_role TEXT,
            custom_api_key TEXT,
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
            questions TEXT,
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
            q_index INTEGER DEFAULT 0,
            question TEXT,
            answer TEXT,
            score REAL DEFAULT 0,
            feedback TEXT DEFAULT '',
            improvement_tip TEXT DEFAULT '',
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    ''')

    # ── Migrations: safely add new columns if they don't already exist ────────
    migrations = [
        "ALTER TABLE sessions ADD COLUMN questions TEXT",
        "ALTER TABLE sessions ADD COLUMN overall_score REAL DEFAULT 0",
        "ALTER TABLE sessions ADD COLUMN user_id INTEGER",
        "ALTER TABLE sessions ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE users ADD COLUMN saved_resume TEXT",
        "ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE users ADD COLUMN default_type TEXT",
        "ALTER TABLE users ADD COLUMN default_role TEXT",
        "ALTER TABLE users ADD COLUMN custom_api_key TEXT",
        "ALTER TABLE qa_records ADD COLUMN q_index INTEGER DEFAULT 0",
    ]
    for sql in migrations:
        try:
            c.execute(sql)
        except sqlite3.OperationalError:
            pass  # Column already exists — safe to ignore

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


def update_user_profile(user_id, name, saved_resume, default_type, default_role, custom_api_key):
    """Updates all user profile settings."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        UPDATE users 
        SET name = ?, saved_resume = ?, default_type = ?, default_role = ?, custom_api_key = ?
        WHERE id = ?
    ''', (name, saved_resume, default_type, default_role, custom_api_key, user_id))
    conn.commit()
    conn.close()


def clear_user_history(user_id):
    """Deletes all sessions and Q&A records for a user."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Delete QA records tied to this user's sessions
    c.execute('''
        DELETE FROM qa_records 
        WHERE session_id IN (SELECT id FROM sessions WHERE user_id = ?)
    ''', (user_id,))
    # Delete the sessions themselves
    c.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()


# ── Session helpers ───────────────────────────────────────────────────────────

def create_session(interview_type, role, resume_data, questions=None, user_id=None):
    """Creates a new interview session in the DB and returns its ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    questions_json = json.dumps(questions) if questions else "[]"
    c.execute('''
        INSERT INTO sessions (user_id, interview_type, role, resume_data, questions)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, interview_type, role, json.dumps(resume_data), questions_json))
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
    """Fetches session metadata and questions by ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT interview_type, role, resume_data, questions FROM sessions WHERE id = ?', (session_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        interview_type, role, resume_json, questions_json = row
        resume_data = json.loads(resume_json) if resume_json else {}
        questions = json.loads(questions_json) if questions_json else []
        return interview_type, role, resume_data, questions
    return None, None, {}, []


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


def save_answer(session_id, q_index, question, answer):
    """
    Saves or updates a candidate's answer for a specific question index synchronously in SQLite.
    Guarantees immediate persistence to prevent data loss.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id FROM qa_records WHERE session_id = ? AND q_index = ?', (session_id, q_index))
    row = c.fetchone()
    if row:
        c.execute('UPDATE qa_records SET question = ?, answer = ? WHERE id = ?', (question, answer, row[0]))
    else:
        c.execute('''
            INSERT INTO qa_records (session_id, q_index, question, answer, score, feedback, improvement_tip)
            VALUES (?, ?, ?, ?, 0, '', '')
        ''', (session_id, q_index, question, answer))
    conn.commit()
    conn.close()


def get_answer(session_id, q_index):
    """Fetches previously saved answer text for a specific question index."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT answer FROM qa_records WHERE session_id = ? AND q_index = ?', (session_id, q_index))
    row = c.fetchone()
    conn.close()
    return row[0] if row else ""


def update_qa_grade(session_id, q_index, score, feedback, improvement_tip):
    """Updates grading details for a specific saved Q&A record."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        UPDATE qa_records 
        SET score = ?, feedback = ?, improvement_tip = ?
        WHERE session_id = ? AND q_index = ?
    ''', (score, feedback, improvement_tip, session_id, q_index))
    conn.commit()
    conn.close()


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
    """Fetches all graded Q&A records for a given session ID ordered by question index."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT q_index, question, answer, score, feedback, improvement_tip 
        FROM qa_records 
        WHERE session_id = ? 
        ORDER BY q_index ASC, id ASC
    ''', (session_id,))
    rows = c.fetchall()
    conn.close()
    
    qa_list = []
    for row in rows:
        q_idx, q, a, s, f, tip = row
        qa_list.append({
            'q_index': q_idx,
            'question': q, 
            'answer': a, 
            'score': s, 
            'feedback': f, 
            'tip': tip
        })
    return qa_list
