# AI Mock Interview Application

An AI-powered web application that conducts interactive technical and behavioral mock interviews tailored to your resume, role, and interview category using Google Gemini API (with Grok failover).

---

## 🚀 Features

- **Resume Parsing**: Automatically extracts candidate skills, projects, and tech stack from resume text.
- **Customized Question Generation**: Generates 5–8 targeted questions tailored to the candidate's profile and selected role/category, guided by Part 2 (Role Reference) and Part 3 (Few-Shot Examples) of the Master Reference Doc.
- **Interactive Interview Session**: Step-by-step interview prompt flow.
- **Automated AI Grading & Rubric Scoring**: Evaluates candidate answers against a master rubric (Part 1, 1–5 scale for Technical & STAR Behavioral dimensions), providing detailed feedback and concrete improvement tips.
- **SQLite Data Persistence**: Session history and detailed report cards stored locally.

---

## 📋 Requirements

- Python 3.10 or higher
- A Google Gemini API Key ([Get one from Google AI Studio](https://aistudio.google.com/)) or Grok/xAI API Key

---

## 🛠️ Local Setup Instructions

### 1. Clone & Navigate to Repository
```bash
git clone https://github.com/mehraj-cmd/Mock-Interview.git
cd Mock-Interview
git checkout main
```

### 2. Create and Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory (or copy `.env.example`):
```bash
cp .env.example .env
```
Open `.env` and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🏃 Running the Application Locally

Start the Flask development server:
```bash
python app.py
```

Once running, open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 🧪 Project Structure

- `app.py`: Flask web routes & application controller.
- `db.py`: SQLite database helper for session and Q&A persistence.
- `grader.py`: AI client integration for evaluating candidate answers against `Mock-Interview-Master-Reference.md`.
- `extract_resume.py`: Resume keyword and structure extractor.
- `Mock-Interview-Master-Reference.md`: Single source of truth containing Part 1 (Grading Rubric), Part 2 (Interview Question Reference by Role), and Part 3 (Resume + Question + Answer Examples).
- `rubric.md`: Mirror of master reference doc for backward compatibility.
- `templates/`: HTML Jinja templates for landing, setup, interview, and report cards.
- `static/`: CSS styles and front-end visual assets.