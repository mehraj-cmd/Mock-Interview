import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

app = Flask(__name__)
# A secret key is needed to securely store data in the Flask session between pages
app.secret_key = "super_secret_development_key"

# Initialize the Gemini API client
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key and api_key != "your_api_key_here" else None

@app.route('/')
def home():
    """Render the landing page with the resume text area."""
    return render_template('index.html')

@app.route('/process_resume', methods=['POST'])
def process_resume():
    """Handle resume submission via text paste OR PDF upload."""
    resume_text = request.form.get('resume_text', '').strip()
    pdf_file = request.files.get('resume_pdf')

    # --- PDF Upload path ---
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        try:
            import fitz  # PyMuPDF
            pdf_bytes = pdf_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            extracted_pages = []
            for page in doc:
                extracted_pages.append(page.get_text())
            resume_text = "\n".join(extracted_pages).strip()
            doc.close()
        except Exception as e:
            flash("Could not read the PDF file. Please try a different file or paste your resume as text.")
            print(f"PDF extraction error: {str(e)}")
            return redirect(url_for('home'))

    # --- Validate we have some text to work with ---
    if not resume_text:
        flash("Please either paste your resume text or upload a PDF file before continuing.")
        return redirect(url_for('home'))

    if not client:
        flash("Gemini API key not configured properly in .env.")
        return redirect(url_for('home'))

    # Prompt instructing Gemini to extract specific data into JSON format
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
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        extracted_data = json.loads(response.text)
        session['resume_data'] = extracted_data
        return redirect(url_for('setup_interview'))

    except Exception as e:
        flash("Oops! The AI is a bit busy and had trouble parsing your resume. Please try again.")
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
    """Save the selected interview type and role to the session."""
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
    """Step 4: Generate interview questions using Gemini."""
    resume_data = session.get('resume_data')
    interview_type = session.get('interview_type')
    role = session.get('role')
    
    if not resume_data or not interview_type or not role:
        return redirect(url_for('home'))
        
    if not client:
        flash("Gemini API key not configured.")
        return redirect(url_for('home'))

    prompt = f"""
    You are an expert technical recruiter and interviewer.
    Generate a list of exactly 5 to 8 interview questions for a candidate applying for a {role} role.
    The interview type is {interview_type}.

    Here is the candidate's extracted resume data:
    {json.dumps(resume_data)}

    Guidelines:
    - If the resume data has specific skills and projects, make at least half the questions highly specific to their actual experience.
    - If the resume data is sparse, rely more on standard, high-quality questions for this role and interview type.
    - Ensure questions sound natural, conversational, and challenging but fair.
    - Do not include answers, explanations, or conversational filler.

    Return the result STRICTLY as a JSON array of strings. 
    Example format: ["Tell me about a time you used Python?", "How does a database index work?"]
    """

    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        questions = json.loads(response.text)
        session['questions'] = questions
        session['current_q_index'] = 0
        session['answers'] = [] 
        return redirect(url_for('interview'))
        
    except Exception as e:
        flash("Oops! The AI took too long to generate questions. Please try again.")
        print(f"Error: {str(e)}")
        return redirect(url_for('setup_interview'))

@app.route('/interview')
def interview():
    """Step 5: Present one question at a time for the user to answer."""
    questions = session.get('questions', [])
    current_index = session.get('current_q_index', 0)
    
    if not questions:
        return redirect(url_for('home'))
        
    if current_index >= len(questions):
        return redirect(url_for('process_grades'))
        
    current_question = questions[current_index]
    return render_template('interview.html', 
                           question=current_question, 
                           current=current_index + 1, 
                           total=len(questions))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Save the user's typed answer and move to the next question."""
    answer_text = request.form.get('answer', '')
    answers = session.get('answers', [])
    answers.append(answer_text)
    session['answers'] = answers
    session['current_q_index'] = session.get('current_q_index', 0) + 1
    return redirect(url_for('interview'))

@app.route('/process_grades')
def process_grades():
    """Step 7 & 8: Grade all answers via Gemini and save the whole session to SQLite."""
    questions = session.get('questions', [])
    answers = session.get('answers', [])
    role = session.get('role')
    interview_type = session.get('interview_type')
    resume_data = session.get('resume_data')
    
    if not questions or not answers:
        return redirect(url_for('home'))
        
    import db
    db_session_id = db.create_session(interview_type, role, resume_data)
    
    from grader import grade_answer
    for i in range(len(questions)):
        q = questions[i]
        a = answers[i] if i < len(answers) else ""
        grade = grade_answer(q, a, role, interview_type)
        db.add_qa_record(
            session_id=db_session_id,
            question=q,
            answer=a,
            score=grade.get('score', 0),
            feedback=grade.get('feedback', ''),
            improvement_tip=grade.get('improvement_tip', '')
        )
        
    session['db_session_id'] = db_session_id
    session.pop('questions', None)
    session.pop('answers', None)
    session.pop('current_q_index', None)
    
    return redirect(url_for('report_card'))

@app.route('/report_card')
def report_card():
    """Step 9: Show the final report with scores and feedback for each Q&A."""
    db_session_id = session.get('db_session_id')
    if not db_session_id:
        return redirect(url_for('home'))
    
    import db
    interview_type, role, resume_data = db.get_session(db_session_id)
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
    import db
    db.init_db()
    app.run(debug=True)


