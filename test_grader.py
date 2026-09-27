import os
from dotenv import load_dotenv
from grader import grade_answer

# Load environment variables
load_dotenv()

def test_grading_consistency():
    """
    Tests the grading function by running it multiple times on the same answer 
    to verify that Gemini returns reasonably consistent scores based on the rubric.
    """
    question = "Can you describe a time you had a disagreement with a team member and how you resolved it?"
    
    # A deliberately mediocre answer that should score around a 5-6 on the HR/Behavioral STAR rubric
    answer = "Yes, one time my coworker wanted to use React but I wanted to use Vue. We argued for a bit, but eventually we just decided to use React because our manager told us to. It worked out fine in the end."
    
    role = "Software Development Engineer (SDE)"
    interview_type = "HR/Behavioral"
    
    print("Testing Grading Consistency...\n")
    print(f"Question: {question}")
    print(f"Answer: {answer}\n")
    
    for i in range(1, 4):
        print(f"--- Attempt {i} ---")
        result = grade_answer(question, answer, role, interview_type)
        print(f"Score: {result.get('score')}")
        print(f"Feedback: {result.get('feedback')}")
        print(f"Tip: {result.get('improvement_tip')}\n")

if __name__ == "__main__":
    test_grading_consistency()
