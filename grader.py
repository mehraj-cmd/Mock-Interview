import os
import json
from google import genai
from google.genai import types

def grade_answer(question, answer, role, interview_type, api_key=None):
    """
    Grades a single interview answer using the Master Rubric via the Gemini API.
    Returns a dictionary with 'score', 'feedback', and 'improvement_tip'.
    """
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"score": 0, "feedback": "API Key missing.", "improvement_tip": ""}
        
    client = genai.Client(api_key=api_key)
    
    # Read the rubric
    rubric_path = os.path.join(os.path.dirname(__file__), 'rubric.md')
    try:
        with open(rubric_path, 'r', encoding='utf-8') as f:
            rubric_text = f.read()
    except FileNotFoundError:
        rubric_text = "Standard professional grading."

    prompt = f"""
    You are an expert technical interviewer and strict grader.
    Your task is to grade a candidate's answer based on the provided Master Rubric.
    
    Interview Context:
    - Target Role: {role}
    - Interview Type: {interview_type}
    
    The Interview Question: 
    "{question}"
    
    The Candidate's Answer: 
    "{answer}"
    
    INSTRUCTIONS:
    1. Read the Master Rubric below. Identify the ONE most appropriate category for this role and interview type (e.g., if Technical SDE, use Category 1. If HR, use Category 2).
    2. Analyze the candidate's answer against the 4 dimensions of that category.
    3. Calculate the weighted score according to the rubric rules.
    4. Apply any red flags (deductions) or green flags (bonuses) if present.
    5. Clamp the final score between 1 and 10.
    
    Return the result STRICTLY as a JSON object with this exact structure:
    {{
        "score": <float between 1.0 and 10.0>,
        "feedback": "<Specific, actionable feedback explaining the score based on the rubric dimensions (2-3 sentences)>",
        "improvement_tip": "<One concrete tip to improve>"
    }}
    
    <MASTER_RUBRIC>
    {rubric_text}
    </MASTER_RUBRIC>
    """
    
    try:
        # Using flash-lite for speed and quota limits, though standard flash could be used if quota allows
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error grading answer: {e}")
        return {
            "score": 0, 
            "feedback": f"Error during grading: {str(e)}", 
            "improvement_tip": "N/A"
        }
