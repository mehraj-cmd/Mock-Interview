import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pypdf import PdfReader

# Load environment variables from the .env file
load_dotenv()

# Initialize the Gemini API client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key or api_key == "your_api_key_here":
    print("WARNING: Please set a valid GEMINI_API_KEY in your .env file.")
    client = None
else:
    client = genai.Client(api_key=api_key)

def extract_resume_info(text=None, pdf_path=None):
    """
    Extracts skills, project names, and technologies from a resume.
    Accepts raw text, a path to a PDF, or both.
    """
    if not client:
        print("Gemini Client not initialized due to missing API key.")
        return None

    if not text and not pdf_path:
        raise ValueError("You must provide either 'text' or 'pdf_path'")

    resume_content = text if text else ""

    # If a PDF path is provided, extract its text and append/use it
    if pdf_path:
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    resume_content += extracted_text + "\n"
        except Exception as e:
            print(f"Error reading PDF '{pdf_path}': {e}")
            return None

    if not resume_content.strip():
        print("No content could be extracted from the provided inputs.")
        return None

    # Prompt forcing the model to return a structured JSON response
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

    max_retries = 6
    for attempt in range(max_retries):
        try:
            # Use a modern Gemini model via the new SDK
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
            )
            
            return json.loads(response.text)
        
        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "UNAVAILABLE" in error_str:
                if attempt < max_retries - 1:
                    wait_time = 2 ** (attempt + 1)  # 2s, 4s, 8s, 16s, 32s...
                    print(f"API is currently busy (503). Retrying in {wait_time} seconds (Attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    print(f"Error: API is persistently unavailable after {max_retries} attempts.")
                    return None
            else:
                print(f"Error during Gemini API call or JSON parsing: {e}")
                return None

if __name__ == "__main__":
    # Quick test to demonstrate functionality
    sample_text = (
        "Experienced Backend Developer. "
        "Led the development of the 'E-Commerce Analytics Platform' using Python, Django, and PostgreSQL. "
        "Proficient in Cloud Architecture, Agile Methodologies, and Team Leadership. "
        "Also built 'ChatterBox', a real-time chat app utilizing Node.js, Socket.io, and Redis. "
        "Familiar with Docker and AWS."
    )
    
    print("Testing extraction with sample text...")
    result = extract_resume_info(text=sample_text)
    
    if result:
        print("\nExtracted Data:")
        print(json.dumps(result, indent=2))
