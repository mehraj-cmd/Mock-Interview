import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
from ai_client import generate_ai_completion, has_valid_api_key
import db

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Secret key for Flask session storage
app.secret_key = "super_secret_development_key"

@app.route('/')
def home():
    """Render the landing page with the resume text area."""
    return render_template('index.html')

@app.route('/process_resume', methods=['POST'])
def process_resume():
    """Handle resume submission, extract data using Gemini/Grok failover, and save to session."""
    resume_text = request.form.get('resume_text', '')
    
    if not resume_text.strip():
        flash("Please paste your resume text before continuing.")
        return redirect(url_for('home'))
        
    if not has_valid_api_key():
        flash("No valid API key configured. Please set GEMINI_API_KEY or GROK_API_KEY in your .env file.")
        return redirect(url_for('home'))
    
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
        extracted_data = generate_ai_completion(prompt, json_mode=True)
        if not isinstance(extracted_data, dict):
            extracted_data = {"skills": [], "projects": [], "technologies": []}
        session['resume_data'] = extracted_data
        return redirect(url_for('setup_interview'))
    
    except Exception as e:
        flash(f"Error processing resume with AI: {str(e)}")
        print(f"Error: {str(e)}")
        return redirect(url_for('home'))

@app.route('/setup_interview')
def setup_interview():
    """Step 3: Screen to select interview type and role."""
    if 'resume_data' not in session:
        return redirect(url_for('home'))
    return render_template('setup.html')

@app.route('/save_setup', methods=['POST'])
def save_setup():
    """Save selected interview type and role to session."""
    interview_type = request.form.get('interview_type')
    role = request.form.get('role')
    
    if not interview_type or not role:
        flash("Please select both an interview type and a role.")
        return redirect(url_for('setup_interview'))
        
    session['interview_type'] = interview_type
    session['role'] = role
    return redirect(url_for('generate_questions'))

@app.route('/generate_questions')
def generate_questions():
    """Step 4: Generate interview questions and initialize SQLite session."""
    resume_data = session.get('resume_data')
    interview_type = session.get('interview_type')
    role = session.get('role')
    
    if not resume_data or not interview_type or not role:
        return redirect(url_for('home'))
        
    if not has_valid_api_key():
        flash("No valid API key configured. Please set GEMINI_API_KEY or GROK_API_KEY in your .env file.")
        return redirect(url_for('home'))

    ref_path = os.path.join(os.path.dirname(__file__), 'Mock-Interview-Master-Reference.md')
    if not os.path.exists(ref_path):
        ref_path = os.path.join(os.path.dirname(__file__), 'rubric.md')
    try:
        with open(ref_path, 'r', encoding='utf-8') as f:
            master_ref_text = f.read()
    except FileNotFoundError:
        master_ref_text = ""

    prompt = f"""
    You are an expert technical recruiter and interviewer.
    Generate a list of exactly 5 to 8 interview questions for a candidate applying for a {role} role.
    The interview type is {interview_type}.

    Here is the candidate's extracted resume data:
    {json.dumps(resume_data, indent=2)}

    QUESTION GENERATION GUIDELINES (Refer to Part 2 & Part 3 of the Master Reference Doc below):
    1. Replicate the style, tone, and difficulty of questions in PART 2 (INTERVIEW QUESTION REFERENCE) for {role}.
    2. Follow the principles in Part 2, Part A:
       - Specific enough to test real understanding, not just memory.
       - Tied to what the candidate actually claims in their resume (ask candidates to explain listed projects from scratch or rate their familiarity with tools/technologies listed).
       - Layered with natural follow-ups where appropriate.
       - Balanced mix across: Technical/knowledge questions, Problem-solving questions, and Behavioral questions.
    3. Use PART 3 (RESUME -> QUESTION EXAMPLES) as few-shot examples of how to craft resume-tied questions that probe deeply into specific projects, metrics, and technical decisions.
    4. Generate NEW questions in a similar authentic style tailored specifically to the candidate's resume, rather than copying fixed questions directly.

    Return the result STRICTLY as a JSON array of strings. 
    Example format: ["Walk me through how you built project X?", "How would you handle scenario Y?"]

    <MASTER_REFERENCE_DOC>
    {master_ref_text}
    </MASTER_REFERENCE_DOC>
    """

    try:
        questions = generate_ai_completion(prompt, json_mode=True)
        if not isinstance(questions, list):
            questions = [str(questions)]
        
        # Persist session and questions in SQLite upfront to keep cookie payload light (<100 bytes)
        db_session_id = db.create_session(interview_type, role, resume_data, questions)
        session['db_session_id'] = db_session_id
        session['current_q_index'] = 0
        return redirect(url_for('interview'))
        
    except Exception as e:
        flash(f"Error generating questions: {str(e)}")
        print(f"Error: {str(e)}")
        return redirect(url_for('setup_interview'))

@app.route('/interview')
def interview():
    """Step 5: Present one question at a time for the user to answer."""
    db_session_id = session.get('db_session_id')
    if not db_session_id:
        return redirect(url_for('home'))

    interview_type, role, resume_data, questions = db.get_session(db_session_id)
    current_index = session.get('current_q_index', 0)
    
    if not questions:
        return redirect(url_for('home'))
        
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
def submit_answer():
    """Save user's typed answer synchronously to SQLite database and move to next question."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    db_session_id = session.get('db_session_id')
    
    if not db_session_id:
        err_msg = "Session lost. Please restart your interview."
        if is_ajax:
            return jsonify({'success': False, 'error': err_msg}), 400
        flash(err_msg)
        return redirect(url_for('home'))

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
def process_grades():
    """Step 7 & 8: Grade all recorded answers via AI and save grades in SQLite."""
    db_session_id = session.get('db_session_id')
    if not db_session_id:
        return redirect(url_for('home'))
        
    interview_type, role, resume_data, questions = db.get_session(db_session_id)
    qa_list = db.get_qa_records(db_session_id)
    
    if not qa_list:
        flash("No answers were recorded to grade.")
        return redirect(url_for('home'))
        
    from grader import grade_answer
    for qa in qa_list:
        # Grade only if not already graded
        if qa['score'] == 0 and not qa['feedback']:
            grade = grade_answer(qa['question'], qa['answer'], role, interview_type)
            db.update_qa_grade(
                session_id=db_session_id,
                q_index=qa['q_index'],
                score=grade.get('score', 0),
                feedback=grade.get('feedback', ''),
                improvement_tip=grade.get('improvement_tip', '')
            )
            
    return redirect(url_for('report_card'))

@app.route('/report_card')
def report_card():
    """Step 9: Show final report with scores and feedback for each Q&A."""
    db_session_id = session.get('db_session_id')
    if not db_session_id:
        return redirect(url_for('home'))
    
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
