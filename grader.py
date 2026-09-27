import os
from ai_client import generate_ai_completion, has_valid_api_key

def grade_answer(question, answer, role, interview_type):
    """
    Grades a single interview answer using Part 1 (Rubric) and Part 3 (Few-shot examples)
    from Mock-Interview-Master-Reference.md via AI (Gemini with Grok failover).
    Returns a dictionary with 'score', 'feedback', and 'improvement_tip'.
    """
    if not has_valid_api_key():
        return {
            "score": 0.0,
            "feedback": "API Key not configured. Please set GEMINI_API_KEY or GROK_API_KEY in your .env file.",
            "improvement_tip": "Configure your .env file."
        }
    
    # Read the Master Reference Doc (Part 1 Rubric & Part 3 Calibration Examples)
    ref_path = os.path.join(os.path.dirname(__file__), 'Mock-Interview-Master-Reference.md')
    if not os.path.exists(ref_path):
        ref_path = os.path.join(os.path.dirname(__file__), 'rubric.md')
        
    try:
        with open(ref_path, 'r', encoding='utf-8') as f:
            master_ref_text = f.read()
    except FileNotFoundError:
        master_ref_text = "Standard professional grading."

    prompt = f"""
    You are an expert technical interviewer and strict grader.
    Your task is to grade a candidate's answer based on the official Mock Interview Master Reference Doc below.

    Interview Context:
    - Target Role: {role}
    - Interview Type: {interview_type}

    The Interview Question:
    "{question}"

    The Candidate's Answer:
    "{answer}"

    GRADING SYSTEM INSTRUCTIONS:
    1. Determine whether this question/interview type requires the Technical Rubric (Part 1, Part A) or the Behavioral/HR Rubric (Part 1, Part B).
       - Technical Rubric (1-5 scale): Relevance, Depth & Correctness, Structure & Clarity, Trade-off Awareness. Overall score = average of the 4 dimension scores (rounded to nearest 0.5).
       - Behavioral STAR Rubric (1-5 scale): Situation, Task, Action, Result. Overall score = average of the 4 STAR dimension scores (rounded to nearest 0.5).

    2. Enforce Strict Feedback Rules (Part 1, Part C):
       - Never write vague feedback like "could be clearer" or "good effort." Always name the specific thing that was missing or strong.
       - Always quote or paraphrase something the candidate actually said in their answer.
       - For technical questions with low trade-off awareness, suggest what trade-off they missed.
       - For behavioral questions with low Action score due to "we" language, explicitly call that out ("You described what the team did, but not your specific role...").
       - Keep feedback to 2-4 sentences per answer.

    3. Calibration Reference: Use the model answers in Part 3 of the reference doc below as benchmarks for high-scoring (Score 4.5 - 5.0) responses.

    Return the result STRICTLY as a JSON object with this exact structure:
    {{
        "score": <float between 1.0 and 5.0, rounded to nearest 0.5>,
        "feedback": "<2-4 sentences of specific, actionable feedback referencing the candidate's actual words and rubric dimensions>",
        "improvement_tip": "<One concrete, specific tip to improve the answer>"
    }}

    <MASTER_REFERENCE_DOC>
    {master_ref_text}
    </MASTER_REFERENCE_DOC>
    """
    
    try:
        result = generate_ai_completion(prompt, json_mode=True)
        if isinstance(result, dict):
            # Ensure score is numeric and within 1.0 - 5.0 range
            score = float(result.get('score', 3.0))
            result['score'] = min(max(round(score * 2) / 2, 1.0), 5.0)
            return result
        return {
            "score": 3.0,
            "feedback": str(result),
            "improvement_tip": "N/A"
        }
    except Exception as e:
        print(f"Error grading answer: {e}")
        return {
            "score": 1.0, 
            "feedback": f"Error during grading: {str(e)}", 
            "improvement_tip": "N/A"
        }
