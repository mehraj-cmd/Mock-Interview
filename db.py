import sqlite3
import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'interview_data.db')

def init_db():
    """Initializes the SQLite database and creates tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Table to store overarching interview session details
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_type TEXT,
            role TEXT,
            resume_data TEXT
        )
    ''')
    
    # Table to store individual Q&A pairs and their grades
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

def create_session(interview_type, role, resume_data):
    """Creates a new interview session in the DB and returns its ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO sessions (interview_type, role, resume_data) VALUES (?, ?, ?)',
              (interview_type, role, json.dumps(resume_data)))
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id

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

def get_session(session_id):
    """Fetches session metadata by ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT interview_type, role, resume_data FROM sessions WHERE id = ?', (session_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        interview_type, role, resume_json = row
        resume_data = json.loads(resume_json) if resume_json else {}
        return interview_type, role, resume_data
    return None, None, {}

def get_qa_records(session_id):
    """Fetches all graded Q&A records for a given session ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT question, answer, score, feedback, improvement_tip FROM qa_records WHERE session_id = ?', (session_id,))
    rows = c.fetchall()
    conn.close()
    
    qa_list = []
    for row in rows:
        q, a, s, f, tip = row
        qa_list.append({'question': q, 'answer': a, 'score': s, 'feedback': f, 'tip': tip})
    return qa_list
