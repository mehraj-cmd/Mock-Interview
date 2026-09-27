import os
from dotenv import load_dotenv
from grader import grade_answer

# Load environment variables
load_dotenv()

def test_grading_consistency():
    """
    Tests the grading function by running it on sample answers from Part 3 of the
    Mock-Interview-Master-Reference doc to verify consistent scores on the 1-5 scale.
    """
    # Sample question & answer from Part 3 (Resume 1, Q4 - HR/Behavioral STAR)
    question = "You joined as the first sales hire at Diverse Lab. How did you build the outbound BD function from scratch with no existing playbook?"
    answer = (
        "Situation: I joined as the company's first sales hire for an AI creative studio with no existing outreach process. "
        "Task: I needed to build a working pipeline that could consistently generate qualified leads. "
        "Action: I moved away from generic cold outreach and built peer-to-peer, industry-tailored sequences with portfolio-led proposals, "
        "sourcing 40+ leads weekly across the US, UK, UAE, and India through LinkedIn Sales Navigator. "
        "Result: This converted 15-20% of qualified conversations into discovery calls, which became the foundation of the company's ongoing pipeline."
    )
    
    role = "Software Development Engineer (SDE)"
    interview_type = "HR/Behavioral"
    
    print("Testing Grading Consistency against Master Reference Doc (1-5 Scale)...\n")
    print(f"Question: {question}")
    print(f"Answer: {answer}\n")
    
    for i in range(1, 4):
        print(f"--- Attempt {i} ---")
        result = grade_answer(question, answer, role, interview_type)
        print(f"Score: {result.get('score')} / 5.0")
        print(f"Feedback: {result.get('feedback')}")
        print(f"Tip: {result.get('improvement_tip')}\n")

if __name__ == "__main__":
    test_grading_consistency()
