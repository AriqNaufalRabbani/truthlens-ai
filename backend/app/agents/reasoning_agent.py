from groq import Groq
import os
import json
import re

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_json(text: str) -> dict | None:
    """
    Ambil JSON object pertama dari string (aman dari ```json```).
    """
    match = re.search(r'\{[\s\S]*\}', text)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


def verify_claim(image_text: str, search_result: str) -> dict:
    prompt = f"""
You are a fact-checking AI.

CLAIM:
{image_text}

SEARCH RESULTS:
{search_result}

Return ONLY valid JSON (no markdown, no explanation outside JSON):
{{
  "verdict": "BENAR | SALAH | TIDAK PASTI",
  "confidence": 1-100,
  "explanation": "Penjelasan singkat dan jelas dalam Bahasa Indonesia"
}}
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    raw = res.choices[0].message.content.strip()

    parsed = extract_json(raw)
    if parsed:
        return parsed

    # fallback terakhir (kalau LLM benar-benar ngawur)
    return {
        "verdict": "TIDAK PASTI",
        "confidence": 0,
        "explanation": raw
    }
