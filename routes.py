from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "app"))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

from gemini_flash import generate_outline
from gemini_pro import generate_story
from image_generator import generate_image
from layout_builder import build_comic_layout
from exporters import save_pdf

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...)
):
    try:
        full_prompt = f"{prompt}\nThe main character is {character_name}. The setting is a {setting}. The tone is {tone}. The art style is {style}."
        outline = generate_outline(full_prompt)
        
        if not isinstance(outline, list) or "error" in outline:
            raise ValueError("Failed to create outline layout from AI.")
            
        full_story = generate_story(outline)
        images = [generate_image(panel["image_prompt"], panel["panel"]) for panel in outline]
        layout = build_comic_layout(images, full_story, outline)
        pdf_path = save_pdf(layout)
        
        return templates.TemplateResponse("comic_preview.html", {
            "request": request,
            "layout": layout,
            "pdf_path": f"/{pdf_path}"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str):
    return templates.TemplateResponse("export_success.html", {
        "request": request,
        "pdf_path": pdf_path
    })