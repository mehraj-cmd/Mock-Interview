import sqlite3
import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'interview_data.db')

def init_db():
    """Initializes the SQLite database and ensures required tables and columns exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Table to store overarching interview session details
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_type TEXT,
            role TEXT,
            resume_data TEXT,
            questions TEXT
        )
    ''')
    
    # Ensure 'questions' column exists in sessions table
    c.execute("PRAGMA table_info(sessions)")
    columns = [col[1] for col in c.fetchall()]
    if 'questions' not in columns:
        c.execute("ALTER TABLE sessions ADD COLUMN questions TEXT")
    
    # Table to store individual Q&A pairs and their grades
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
    
    # Ensure 'q_index' column exists in qa_records table
    c.execute("PRAGMA table_info(qa_records)")
    qa_cols = [col[1] for col in c.fetchall()]
    if 'q_index' not in qa_cols:
        c.execute("ALTER TABLE qa_records ADD COLUMN q_index INTEGER DEFAULT 0")

    conn.commit()
    conn.close()

def create_session(interview_type, role, resume_data, questions=None):
    """Creates a new interview session in the DB and returns its ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    questions_json = json.dumps(questions) if questions else "[]"
    c.execute('''
        INSERT INTO sessions (interview_type, role, resume_data, questions) 
        VALUES (?, ?, ?, ?)
    ''', (interview_type, role, json.dumps(resume_data), questions_json))
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id

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
