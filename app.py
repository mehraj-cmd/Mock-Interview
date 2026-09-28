import os
import json
import db
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from ai_client import generate_ai_completion, has_valid_api_key

load_dotenv()
db.init_db()

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
        self.default_type = user_dict.get('default_type', '')
        self.default_role = user_dict.get('default_role', '')
        self.custom_api_key = user_dict.get('custom_api_key', '')

@login_manager.user_loader
def load_user(user_id):
    row = db.get_user_by_id(int(user_id))
    return User(row) if row else None


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
        default_type = request.form.get('default_type', '').strip()
        default_role = request.form.get('default_role', '').strip()
        custom_api_key = request.form.get('custom_api_key', '').strip()
        
        db.update_user_profile(
            current_user.id, 
            new_name, 
            saved_resume, 
            default_type, 
            default_role, 
            custom_api_key
        )
        flash("Profile and preferences updated successfully! ✅")
        return redirect(url_for('profile'))

    user_row = db.get_user_by_id(current_user.id)
    return render_template('profile.html', user=user_row)


@app.route('/clear_history', methods=['POST'])
@login_required
def clear_history():
    db.clear_user_history(current_user.id)
    flash("Your interview history has been permanently deleted.")
    return redirect(url_for('profile'))


# ══════════════════════════════════════════════════════════════════════════════
# INTERVIEW FLOW
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

    user_api_key = current_user.custom_api_key if current_user.is_authenticated else None
    if not has_valid_api_key() and not user_api_key:
        flash("API key not configured. Add one in your Profile Settings or check the server .env file.")
        return redirect(url_for('resume_page'))

    # Optionally save resume to user profile
    if save_it:
        user_row = db.get_user_by_id(current_user.id)
        db.update_user_profile(
            current_user.id, 
            user_row['name'], 
            resume_text, 
            user_row.get('default_type', ''), 
            user_row.get('default_role', ''), 
            user_row.get('custom_api_key', '')
        )

    # Make it incredibly fast by skipping the AI extraction here.
    # We will pass the raw resume_text directly to the question generator later.
    session['resume_data'] = resume_text
    return redirect(url_for('setup_interview'))


@app.route('/setup_interview')
@login_required
def setup_interview():
    if 'resume_data' not in session:
        return redirect(url_for('resume_page'))
        
    user_row = db.get_user_by_id(current_user.id)
    default_type = user_row.get('default_type', '') if user_row else ''
    default_role = user_row.get('default_role', '') if user_row else ''
    
    return render_template('setup.html', default_type=default_type, default_role=default_role)


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
    
    user_api_key = current_user.custom_api_key if current_user.is_authenticated else None
    if not has_valid_api_key() and not user_api_key:
        flash("API key not configured. Please add one in your Profile Settings or .env file.")
        return redirect(url_for('resume_page'))

    ref_path = os.path.join(os.path.dirname(__file__), 'Mock-Interview-Master-Reference.md')
    if not os.path.exists(ref_path):
        ref_path = os.path.join(os.path.dirname(__file__), 'rubric.md')
    try:
        with open(ref_path, 'r', encoding='utf-8') as f:
            master_ref_text = f.read()
            # Massively speed up generation and avoid rate limits by ONLY using Part 2
            if "## PART 2" in master_ref_text:
                part2_onward = "## PART 2" + master_ref_text.split("## PART 2", 1)[1]
                if "## PART 3" in part2_onward:
                    master_ref_text = part2_onward.split("## PART 3", 1)[0]
                else:
                    master_ref_text = part2_onward
    except FileNotFoundError:
        master_ref_text = ""

    prompt = f"""
    You are an expert technical recruiter and interviewer.
    Generate a list of exactly 5 to 8 interview questions for a candidate applying for a {role} role.
    The interview type is {interview_type}.

    Here is the candidate's full resume text:
    {resume_data}

    QUESTION GENERATION GUIDELINES:
    1. Replicate the style, tone, and difficulty of questions in PART 2 (INTERVIEW QUESTION REFERENCE) for {role}.
    2. Specific enough to test real understanding, not just memory.
    3. Tied to what the candidate actually claims in their resume (ask candidates to explain listed projects from scratch or rate their familiarity with tools/technologies listed).
    4. Generate NEW questions in a similar authentic style tailored specifically to the candidate's resume, rather than copying fixed questions directly.

    Return the result STRICTLY as a JSON object containing a single key "questions" which is an array of strings. 
    Example format: {{ "questions": ["Walk me through how you built project X?", "How would you handle scenario Y?"] }}

    <MASTER_REFERENCE_DOC>
    {master_ref_text}
    </MASTER_REFERENCE_DOC>
    """
    try:
        response_data = generate_ai_completion(prompt, json_mode=True, api_key=user_api_key)
        
        # Handle both the new object format and fallback array format
        if isinstance(response_data, dict) and 'questions' in response_data:
            questions = response_data['questions']
        elif isinstance(response_data, list):
            questions = response_data
        else:
            questions = [str(response_data)]
            
        if not isinstance(questions, list):
            questions = [str(questions)]
        
        # Persist session and questions in SQLite upfront
        db_session_id = db.create_session(interview_type, role, resume_data, questions, user_id=current_user.id)
        session['db_session_id'] = db_session_id
        session['current_q_index'] = 0
        return redirect(url_for('interview'))
    except Exception as e:
        flash(f"Error generating questions: {str(e)}")
        print(f"Error: {str(e)}")
        return redirect(url_for('setup_interview'))


@app.route('/interview')
@login_required
def interview():
    """Step 5: Present one question at a time for the user to answer."""
    db_session_id = session.get('db_session_id')
    if not db_session_id:
        return redirect(url_for('resume_page'))

    interview_type, role, resume_data, questions = db.get_session(db_session_id)
    current_index = session.get('current_q_index', 0)
    
    if not questions:
        return redirect(url_for('resume_page'))
    if current_index >= len(questions):
        return redirect(url_for('process_grades'))
        
    current_question = questions[current_index]
    existing_answer = db.get_answer(db_session_id, current_index)

    return render_template('interview.html', 
                           question=current_question, 
                           current=current_index + 1, 
                           total=len(questions),
                           existing_answer=existing_answer)


@app.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    """Save user's typed answer synchronously to SQLite database and move to next question."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    db_session_id = session.get('db_session_id')
    
    if not db_session_id:
        err_msg = "Session lost. Please restart your interview."
        if is_ajax:
            return jsonify({'success': False, 'error': err_msg}), 400
        flash(err_msg)
        return redirect(url_for('resume_page'))

    interview_type, role, resume_data, questions = db.get_session(db_session_id)
    current_index = session.get('current_q_index', 0)

    if current_index >= len(questions):
        next_url = url_for('process_grades')
        if is_ajax:
            return jsonify({'success': True, 'redirect': next_url})
        return redirect(next_url)

    answer_text = request.form.get('answer', '').strip()
    if not answer_text:
        err_msg = "Answer cannot be empty."
        if is_ajax:
            return jsonify({'success': False, 'error': err_msg}), 400
        flash(err_msg)
        return redirect(url_for('interview'))

    current_question = questions[current_index]

    try:
        # Synchronously persist answer in SQLite BEFORE responding to client
        db.save_answer(db_session_id, current_index, current_question, answer_text)
        
        # Advance index
        next_index = current_index + 1
        session['current_q_index'] = next_index

        next_url = url_for('interview') if next_index < len(questions) else url_for('process_grades')

        if is_ajax:
            return jsonify({'success': True, 'redirect': next_url})
        return redirect(next_url)

    except Exception as e:
        err_msg = f"Database save error: {str(e)}"
        print(f"[App Error] {err_msg}")
        if is_ajax:
            return jsonify({'success': False, 'error': err_msg}), 500
        flash(err_msg)
        return render_template('interview.html', 
                               question=current_question, 
                               current=current_index + 1, 
                               total=len(questions),
                               existing_answer=answer_text)


@app.route('/process_grades')
@login_required
def process_grades():
    """Step 7 & 8: Grade all recorded answers via AI and save grades in SQLite."""
    db_session_id = session.get('db_session_id')
    if not db_session_id:
        return redirect(url_for('resume_page'))
        
    interview_type, role, resume_data, questions = db.get_session(db_session_id)
    qa_list = db.get_qa_records(db_session_id)
    
    if not qa_list:
        flash("No answers were recorded to grade.")
        return redirect(url_for('resume_page'))
        
    from grader import grade_answer
    import concurrent.futures
    user_api_key = current_user.custom_api_key if current_user.is_authenticated else None

    # Filter out already graded answers to save API calls
    ungraded_qas = [qa for qa in qa_list if qa['score'] == 0 and not qa['feedback']]
    
    if ungraded_qas:
        def _grade_single(qa):
            grade = grade_answer(qa['question'], qa['answer'], role, interview_type, user_api_key)
            return qa['q_index'], grade

        # Grade all answers in parallel!
        results_to_save = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(_grade_single, qa) for qa in ungraded_qas]
            for future in concurrent.futures.as_completed(futures):
                try:
                    q_index, grade = future.result()
                    results_to_save.append((q_index, grade))
                except Exception as e:
                    print(f"Error grading in parallel: {e}")

        # Save to database sequentially to prevent SQLite 'database is locked' errors
        for q_index, grade in results_to_save:
            db.update_qa_grade(
                session_id=db_session_id,
                q_index=q_index,
                score=grade.get('score_out_of_10', grade.get('score', 0) * 2),
                feedback=grade.get('feedback', ''),
                improvement_tip=grade.get('improvement_tip', '')
            )

    # Calculate and store overall score on session (average of per-question 1-10 scores)
    graded_records = db.get_qa_records(db_session_id)
    if graded_records:
        overall = round(sum(r['score'] for r in graded_records) / len(graded_records), 1)
        db.update_session_score(db_session_id, overall)

    return redirect(url_for('report_card'))


@app.route('/report_card')
@login_required
def report_card():
    """Step 9: Show final report with scores and feedback for each Q&A."""
    db_session_id = session.get('db_session_id')
    if not db_session_id:
        return redirect(url_for('dashboard'))
    
    interview_type, role, resume_data, _ = db.get_session(db_session_id)
    qa_list = db.get_qa_records(db_session_id)
    
    total_score = sum([qa['score'] for qa in qa_list])
    overall = round(total_score / len(qa_list), 2) if qa_list else 0
    
    return render_template('report_placeholder.html',
                           interview_type=interview_type,
                           role=role,
                           resume_data=resume_data,
                           qa_list=qa_list,
                           overall_score=overall)


if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)
