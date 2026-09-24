import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_image(prompt: str, panel_number: int) -> str:
    url = f"https://pollinations.ai{requests.utils.quote(prompt)}?width=512&height=512&nologo=true&seed=42"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            panels_dir = os.path.join(BASE_DIR, "static", "panels")
            os.makedirs(panels_dir, exist_ok=True)
            filename = f"panel_{panel_number}.jpg"
            filepath = os.path.join(panels_dir, filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            return f"static/panels/{filename}"
    except Exception:
        pass
    return ""