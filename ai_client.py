import os
import json
import re
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

INVALID_KEY_PLACEHOLDERS = {
    "", 
    "your_api_key_here", 
    "your_gemini_api_key_here", 
    "your_grok_api_key_here", 
    "your_xai_api_key_here"
}

def clean_json_string(text: str) -> str:
    """Extract and sanitize JSON content from markdown code blocks or raw strings."""
    if not text:
        return "{}"
    text = text.strip()
    # Strip markdown fenced code block delimiters if present
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        text = match.group(1).strip()
    return text

def get_api_keys(custom_key: str = None):
    """Returns valid (gemini_key, grok_key) tuples or None for unconfigured keys."""
    gemini_key = (custom_key or os.environ.get("GEMINI_API_KEY", "") or "").strip()
    if gemini_key.lower() in INVALID_KEY_PLACEHOLDERS:
        gemini_key = None

    grok_key = (os.environ.get("GROK_API_KEY") or os.environ.get("XAI_API_KEY") or "").strip()
    if grok_key.lower() in INVALID_KEY_PLACEHOLDERS:
        grok_key = None

    return gemini_key, grok_key

def has_valid_api_key(custom_key: str = None) -> bool:
    """Check if at least one AI API key (Gemini or Grok) is configured."""
    gemini_key, grok_key = get_api_keys(custom_key=custom_key)
    return bool(gemini_key or grok_key)

def call_gemini(prompt: str, json_mode: bool = True, api_key: str = None) -> str:
    """Calls Gemini API via official google-genai SDK with model fallback."""
    from google import genai
    from google.genai import types

    gemini_key, _ = get_api_keys(custom_key=api_key)
    if not gemini_key:
        raise ValueError("Gemini API key is not configured or invalid.")

    client = genai.Client(api_key=gemini_key)
    config = types.GenerateContentConfig(
        response_mime_type="application/json" if json_mode else "text/plain"
    )

    models_to_try = ['gemini-3.8-flash', 'gemini-flash-lite-latest', 'gemini-flash-latest']
    last_error = None

    for model in models_to_try:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config
            )
            if response and response.text:
                return response.text
        except Exception as e:
            last_error = e
            print(f"[AI Client] Gemini model '{model}' failed: {e}")
            continue

    raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")

def call_grok(prompt: str, json_mode: bool = True) -> str:
    """Calls Grok (xAI) API via OpenAI-compatible endpoint with model fallback."""
    _, grok_key = get_api_keys()
    if not grok_key:
        raise ValueError("Grok (xAI) API key is not configured or invalid.")

    headers = {
        "Authorization": f"Bearer {grok_key}",
        "Content-Type": "application/json"
    }

    system_prompt = "You are an expert AI assistant for job interviews."
    if json_mode:
        system_prompt += " You MUST respond ONLY with a valid JSON object or JSON array without markdown wrapping or commentary."

    models_to_try = ["grok-2-latest", "grok-beta", "grok-2-1212"]
    last_error = None

    for model in models_to_try:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                if content:
                    return content
            else:
                print(f"[AI Client] Grok model '{model}' HTTP {response.status_code}: {response.text}")
                last_error = f"HTTP {response.status_code}: {response.text}"
        except Exception as e:
            last_error = e
            print(f"[AI Client] Grok request failed for model '{model}': {e}")
            continue

    raise RuntimeError(f"All Grok models failed. Last error: {last_error}")

def generate_ai_completion(prompt: str, json_mode: bool = True, api_key: str = None):
    """
    Executes AI completion with automatic failover:
    1. Primary: Gemini (if configured or passed via api_key)
    2. Failover: Grok / xAI (if configured)
    If primary fails or key is missing, automatically falls back to secondary.
    Returns parsed JSON if json_mode=True, else returns raw string.
    """
    load_dotenv(override=True)
    gemini_key, grok_key = get_api_keys(custom_key=api_key)

    if not gemini_key and not grok_key:
        raise ValueError("No valid API key configured. Please set GEMINI_API_KEY or GROK_API_KEY in your .env file.")

    attempt_errors = []

    # Attempt 1: Gemini
    if gemini_key:
        try:
            print("[AI Client] Requesting completion from Gemini...")
            raw_text = call_gemini(prompt, json_mode=json_mode, api_key=gemini_key)
            if json_mode:
                return json.loads(clean_json_string(raw_text))
            return raw_text
        except Exception as e:
            msg = f"Gemini error: {e}"
            print(f"[AI Client] {msg}")
            attempt_errors.append(msg)
            if grok_key:
                print("[AI Client] Failing over to Grok (xAI)...")

    # Attempt 2: Grok / xAI (if key present)
    if grok_key:
        try:
            print("[AI Client] Requesting completion from Grok...")
            raw_text = call_grok(prompt, json_mode=json_mode)
            if json_mode:
                return json.loads(clean_json_string(raw_text))
            return raw_text
        except Exception as e:
            msg = f"Grok error: {e}"
            print(f"[AI Client] {msg}")
            attempt_errors.append(msg)

    # If both failed
    all_errs = " | ".join(attempt_errors)
    raise RuntimeError(f"All configured AI providers failed. ({all_errs})")
