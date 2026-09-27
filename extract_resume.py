import os
import json
from dotenv import load_dotenv
from ai_client import generate_ai_completion, has_valid_api_key

load_dotenv()

def extract_resume_info(text=None, pdf_path=None, api_key=None):
    """
    Extracts skills, project names, and technologies from a resume.
    Accepts raw text, a path to a PDF, or both. Uses Gemini with Grok failover.
    """
    if not has_valid_api_key(api_key):
        print("AI Client not initialized due to missing API keys.")
        return None

    if not text and not pdf_path:
        raise ValueError("You must provide either 'text' or 'pdf_path'")

    resume_content = text if text else ""

    if pdf_path:
        try:
            import fitz
            doc = fitz.open(pdf_path)
            extracted_text = "\n".join(page.get_text() for page in doc)
            doc.close()
            if extracted_text:
                resume_content += extracted_text + "\n"
        except Exception as e:
            print(f"Error reading PDF '{pdf_path}': {e}")
            return None

    if not resume_content.strip():
        print("No content could be extracted from the provided inputs.")
        return None

    prompt = f"""
    You are an expert technical recruiter and resume parser. 
    Analyze the following resume text and extract the applicant's skills, project names, and technologies mentioned.
    
    Return the result strictly as a JSON object with this exact structure:
    {{
        "skills": ["list", "of", "general", "skills"],
        "projects": ["Project A", "Project B"],
        "technologies": ["list", "of", "frameworks", "tools", "languages"]
    }}
    
    Resume Text:
    {resume_content}
    """

    try:
        return generate_ai_completion(prompt, json_mode=True, api_key=api_key)
    except Exception as e:
        print(f"Error during AI resume extraction: {e}")
        return None

if __name__ == "__main__":
    sample_text = (
        "Mohd Mehraj. CSE student, solo AI-product builder. Business development intern (built outbound sales "
        "from scratch, LinkedIn prospecting, 15-20% conversion to discovery calls). Built two Shopify stores "
        "end-to-end (Mazami, Sonali Jain) using AI-assisted tools, both lifting conversions/engagement ~40%. "
        "Built 'The Signal', a solo RSS-to-LLM content curation app using Gemini Flash API. "
        "Skills: Claude Code, Antigravity, Shopify, WordPress, LinkedIn Sales Navigator."
    )
    
    print("Testing extraction with sample text...")
    result = extract_resume_info(text=sample_text)
    
    if result:
        print("\nExtracted Data:")
        print(json.dumps(result, indent=2))
