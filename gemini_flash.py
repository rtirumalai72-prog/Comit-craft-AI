import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_outline(user_prompt: str) -> list:
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f'Generate a strictly formatted JSON array containing 5 panel descriptions based on the story idea below. Do not include markdown tags like ```json or ```. Return pure raw JSON text only. Each item in the array must be a JSON object with exactly these keys: "panel": number, "title": string, "scene_description": string, "image_prompt": string. STORY: "{user_prompt}"'
    
    try:
        response = model.generate_content(prompt)
        text_data = response.text.strip().strip("`").strip()
        if text_data.startswith("json"):
            text_data = text_data[4:].strip()
        return json.loads(text_data)
    except Exception as e:
        return [{"panel": 1, "title": "Error", "scene_description": str(e), "image_prompt": "error", "error": True}]