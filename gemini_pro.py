import os
import google.generativeai as genai
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_story(outline: list) -> str:
    formatted_outline = "\n".join([f"Panel {item.get('panel')}: {item.get('title')} - {item.get('scene_description')}" for item in outline])
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f'You are a comic book writer. Given the following panel breakdown, write a cohesive comic-style story with engaging narration and character dialogues for each panel. Mark each panel sections clearly with **Panel 1, **Panel 2 etc. PANEL OUTLINE:\n{formatted_outline}'
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating story: {str(e)}"