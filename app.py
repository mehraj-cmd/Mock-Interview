import os
import json
import db
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key_change_in_production")

# ── Flask-Login setup ─────────────────────────────────────────────────────────
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access that page."

class User(UserMixin):
    def __init__(self, user_dict):
        self.id = user_dict['id']
        self.name = user_dict['name']
        self.email = user_dict['email']
        self.saved_resume = user_dict.get('saved_resume', '')

@login_manager.user_loader
def load_user(user_id):
    row = db.get_user_by_id(int(user_id))
    return User(row) if row else None

# ── Gemini client ─────────────────────────────────────────────────────────────
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key and api_key != "your_api_key_here" else None


# ══════════════════════════════════════════════════════════════════════════════
# AUTH ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        if not name or not email or not password:
            flash("All fields are required.")
            return render_template('register.html')
        if password != confirm:
            flash("Passwords do not match.")
            return render_template('register.html')
        if len(password) < 6:
            flash("Password must be at least 6 characters.")
            return render_template('register.html')

        user_id = db.create_user(name, email, password)
        if user_id is None:
            flash("An account with that email already exists. Please log in.")
            return render_template('register.html')

        user_row = db.get_user_by_id(user_id)
        login_user(User(user_row))
        flash(f"Welcome, {name}! Your account has been created.")
        return redirect(url_for('dashboard'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user_row = db.verify_password(email, password)
        if user_row:
            login_user(User(user_row))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password. Please try again.")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out.")
    return redirect(url_for('login'))


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD & PROFILE
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    past_sessions = db.get_user_sessions(current_user.id)

    # Build chart data: last 10 scores for the progress graph
    scores = [s['overall_score'] for s in past_sessions[:10]][::-1]
    labels = [f"#{s['id']}" for s in past_sessions[:10]][::-1]

    # Compute stats
    total_interviews = len(past_sessions)
    avg_score = round(sum(s['overall_score'] for s in past_sessions) / total_interviews, 1) if total_interviews else 0
    best_score = max((s['overall_score'] for s in past_sessions), default=0)

    return render_template('dashboard.html',
                           past_sessions=past_sessions,
                           scores=scores,
                           labels=labels,
                           total_interviews=total_interviews,
                           avg_score=avg_score,
                           best_score=best_score)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_name = request.form.get('name', '').strip()
        saved_resume = request.form.get('saved_resume', '').strip()
        if new_name:
            db.update_user_name(current_user.id, new_name)
        if saved_resume:
            db.save_user_resume(current_user.id, saved_resume)
        flash("Profile updated successfully! ✅")
        return redirect(url_for('profile'))

    user_row = db.get_user_by_id(current_user.id)
    return render_template('profile.html', user=user_row)


# ══════════════════════════════════════════════════════════════════════════════
# INTERVIEW FLOW (all routes now require login)
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/resume')
@login_required
def resume_page():
    """Step 1: Resume input page."""
    user_row = db.get_user_by_id(current_user.id)
    saved_resume = user_row.get('saved_resume', '') or ''
    return render_template('index.html', saved_resume=saved_resume)


@app.route('/process_resume', methods=['POST'])
@login_required
def process_resume():
    """Handle resume submission via text paste OR PDF upload."""
    resume_text = request.form.get('resume_text', '').strip()
    pdf_file    = request.files.get('resume_pdf')
    save_it     = request.form.get('save_resume') == 'on'

    # PDF Upload path
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        try:
            import fitz
            pdf_bytes = pdf_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            resume_text = "\n".join(page.get_text() for page in doc).strip()
            doc.close()
        except Exception as e:
            flash("Could not read the PDF file. Please try a different file or paste your resume as text.")
            print(f"PDF error: {e}")
            return redirect(url_for('resume_page'))

    if not resume_text:
        flash("Please either paste your resume text or upload a PDF file.")
        return redirect(url_for('resume_page'))

    if not client:
        flash("Gemini API key not configured properly.")
        return redirect(url_for('resume_page'))

    # Optionally save resume to user profile
    if save_it:
        db.save_user_resume(current_user.id, resume_text)

    prompt = f"""
    Analyze the following resume text and extract the applicant's skills, project names, and technologies.
    Return the result strictly as a JSON object with this exact structure:
    {{
        "skills": ["skill 1", "skill 2"],
        "projects": ["project A", "project B"],
        "technologies": ["tech 1", "tech 2"]
    }}
    Resume Text:
    {resume_text}
    """
    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        session['resume_data'] = json.loads(response.text)
        return redirect(url_for('setup_interview'))
    except Exception as e:
        flash("Oops! The AI had trouble parsing your resume. Please try again.")
        print(f"Gemini error: {e}")
        return redirect(url_for('resume_page'))


@app.route('/setup_interview')
@login_required
def setup_interview():
    if 'resume_data' not in session:
        return redirect(url_for('resume_page'))
    return render_template('setup.html')


@app.route('/save_setup', methods=['POST'])
@login_required
def save_setup():
    interview_type = request.form.get('interview_type')
    role           = request.form.get('role')
    if not interview_type or not role:
        flash("Please select both an interview type and a role.")
        return redirect(url_for('setup_interview'))
    session['interview_type'] = interview_type
    session['role'] = role
    return redirect(url_for('generate_questions'))


@app.route('/generate_questions')
@login_required
def generate_questions():
    resume_data    = session.get('resume_data')
    interview_type = session.get('interview_type')
    role           = session.get('role')
    if not resume_data or not interview_type or not role:
        return redirect(url_for('resume_page'))
    if not client:
        flash("Gemini API key not configured.")
        return redirect(url_for('resume_page'))

    prompt = f"""
    You are an expert technical recruiter and interviewer.
    Generate a list of exactly 5 to 8 interview questions for a candidate applying for a {role} role.
    The interview type is {interview_type}.
    Candidate resume data: {json.dumps(resume_data)}
    Guidelines:
    - Make at least half the questions specific to the candidate's actual experience.
    - Questions must sound natural, challenging but fair.
    - Do not include answers or filler text.
    Return STRICTLY as a JSON array of strings.
    """
    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        session['questions']      = json.loads(response.text)
        session['current_q_index'] = 0
        session['answers']         = []
        return redirect(url_for('interview'))
    except Exception as e:
        flash("Oops! The AI took too long to generate questions. Please try again.")
        print(f"Gemini error: {e}")
        return redirect(url_for('setup_interview'))


@app.route('/interview')
@login_required
def interview():
    questions     = session.get('questions', [])
    current_index = session.get('current_q_index', 0)
    if not questions:
        return redirect(url_for('resume_page'))
    if current_index >= len(questions):
        return redirect(url_for('process_grades'))
    return render_template('interview.html',
                           question=questions[current_index],
                           current=current_index + 1,
                           total=len(questions))


@app.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    answers = session.get('answers', [])
    answers.append(request.form.get('answer', ''))
    session['answers'] = answers
    session['current_q_index'] = session.get('current_q_index', 0) + 1
    return redirect(url_for('interview'))


@app.route('/process_grades')
@login_required
def process_grades():
    questions      = session.get('questions', [])
    answers        = session.get('answers', [])
    role           = session.get('role')
    interview_type = session.get('interview_type')
    resume_data    = session.get('resume_data')
    if not questions or not answers:
        return redirect(url_for('resume_page'))

    db_session_id = db.create_session(interview_type, role, resume_data, user_id=current_user.id)

    from grader import grade_answer
    total_score = 0
    for i, q in enumerate(questions):
        a     = answers[i] if i < len(answers) else ""
        grade = grade_answer(q, a, role, interview_type)
        score = grade.get('score', 0)
        total_score += score
        db.add_qa_record(db_session_id, q, a, score,
                         grade.get('feedback', ''),
                         grade.get('improvement_tip', ''))

    overall = round(total_score / len(questions), 2)
    db.update_session_score(db_session_id, overall)

    session['db_session_id'] = db_session_id
    session.pop('questions', None)
    session.pop('answers', None)
    session.pop('current_q_index', None)
    return redirect(url_for('report_card'))


@app.route('/report_card')
@login_required
def report_card():
    db_session_id = session.get('db_session_id')
    if not db_session_id:
        return redirect(url_for('dashboard'))
    interview_type, role, resume_data = db.get_session(db_session_id)
    qa_list = db.get_qa_records(db_session_id)
    total   = sum(qa['score'] for qa in qa_list)
    overall = round(total / len(qa_list), 2) if qa_list else 0
    return render_template('report_placeholder.html',
                           interview_type=interview_type,
                           role=role,
                           resume_data=resume_data,
                           qa_list=qa_list,
                           overall_score=overall)


if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)
