import os
import time
from ai_client import generate_ai_completion, has_valid_api_key

# Grading uses a low temperature for consistent scoring of the same answer.
GRADING_TEMPERATURE = 0.2

def grade_answer(question, answer, role, interview_type, api_key=None, max_retries=2):
    """
    Grades a single interview answer using Part 1 (Rubric) and Part 3 (Few-shot examples)
    from Mock-Interview-Master-Reference.md via AI (Gemini with Grok failover).

    Scale: 1–10 natively (Gemini is instructed to score 1–10, no conversion needed).
    Retries up to max_retries times on failure to avoid ungraded answers.

    Returns a dict with:
        'score'          – float 1.0–10.0, stored & displayed directly
        'feedback'       – str
        'improvement_tip'– str
    """
    if not has_valid_api_key() and not api_key:
        return {
            "score": 0.0,
            "feedback": "API Key not configured. Please set GEMINI_API_KEY or GROK_API_KEY in your environment or settings.",
            "improvement_tip": "Configure your API key."
        }

    # Read the Master Reference Doc — only Part 1 (Rubric) and Part 3 (Examples) for grading
    ref_path = os.path.join(os.path.dirname(__file__), 'Mock-Interview-Master-Reference.md')
    if not os.path.exists(ref_path):
        ref_path = os.path.join(os.path.dirname(__file__), 'rubric.md')

    try:
        with open(ref_path, 'r', encoding='utf-8') as f:
            master_ref_text = f.read()
            # Strip out Part 2 (question generation) — not needed for grading
            if "## PART 2" in master_ref_text and "## PART 3" in master_ref_text:
                part1 = master_ref_text.split("## PART 2")[0]
                part3 = "## PART 3" + master_ref_text.split("## PART 3")[1]
                master_ref_text = part1 + "\n\n" + part3
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
       - Technical Rubric (1-10 scale): Relevance, Depth & Correctness, Structure & Clarity, Trade-off Awareness. Overall score = average of the 4 dimension scores on a 1-10 scale (rounded to nearest 0.5).
       - Behavioral STAR Rubric (1-10 scale): Situation, Task, Action, Result. Overall score = average of the 4 STAR dimension scores on a 1-10 scale (rounded to nearest 0.5).

    2. Enforce Strict Feedback Rules (Part 1, Part C):
       - Never write vague feedback like "could be clearer" or "good effort." Always name the specific thing that was missing or strong.
       - Always quote or paraphrase something the candidate actually said in their answer.
       - For technical questions with low trade-off awareness, suggest what trade-off they missed.
       - For behavioral questions with low Action score due to "we" language, explicitly call that out ("You described what the team did, but not your specific role...").
       - Keep feedback to 2-4 sentences per answer.

    3. Calibration Reference: Use the model answers in Part 3 of the reference doc below as benchmarks for high-scoring (Score 9.0 - 10.0) responses.

    Return the result STRICTLY as a JSON object with this exact structure:
    {{
        "score": <float between 1.0 and 10.0, rounded to nearest 0.5>,
        "feedback": "<2-4 sentences of specific, actionable feedback referencing the candidate's actual words and rubric dimensions>",
        "improvement_tip": "<One concrete, specific tip to improve the answer>"
    }}

    <MASTER_REFERENCE_DOC>
    {master_ref_text}
    </MASTER_REFERENCE_DOC>
    """

    last_exception = None
    for attempt in range(1, max_retries + 2):  # 1 initial + max_retries retries
        try:
            result = generate_ai_completion(
                prompt,
                json_mode=True,
                api_key=api_key,
                temperature=GRADING_TEMPERATURE
            )
            if isinstance(result, dict):
                # Clamp and round score to 1.0–10.0, nearest 0.5
                raw_score = float(result.get('score', 5.0))
                score = min(max(round(raw_score * 2) / 2, 1.0), 10.0)
                result['score'] = score
                return result
            # Unexpected non-dict response — treat as fallback
            return {
                "score": 5.0,
                "feedback": str(result),
                "improvement_tip": "N/A"
            }
        except Exception as e:
            last_exception = e
            print(f"[Grader] Attempt {attempt} failed for q='{question[:40]}': {e}")
            if attempt < max_retries + 1:
                wait = 2 ** (attempt - 1)  # 1s, 2s, ...
                print(f"[Grader] Retrying in {wait}s...")
                time.sleep(wait)

    # All retries exhausted — return a marked error entry so the answer is not silently dropped
    print(f"[Grader] All {max_retries + 1} attempts failed. Returning error grade.")
    return {
        "score": 0.0,
        "feedback": f"Grading failed after {max_retries + 1} attempts. Please retry. Error: {str(last_exception)}",
        "improvement_tip": "Refresh the results page to retry grading."
    }
