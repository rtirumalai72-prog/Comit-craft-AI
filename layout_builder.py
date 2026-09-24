def build_comic_layout(image_paths: list, full_story: str, outline: list) -> list:
    story_panels = full_story.split("**Panel")
    story_panels = [f"**Panel{panel}" for panel in story_panels if panel.strip()]
    
    layout = []
    for idx, (image, panel_info) in enumerate(zip(image_paths, outline), start=1):
        text_content = "Narration: Action takes place."
        for segment in story_panels:
            if f"Panel {idx}" in segment or f"Panel{idx}" in segment:
                text_content = "\n".join(segment.strip().splitlines()[1:]).strip()
                break
                
        layout.append({
            "panel": idx,
            "title": panel_info.get("title", f"Panel {idx}"),
            "image_path": image,
            "text": text_content,
            "scene_description": panel_info.get("scene_description", "")
        })
    return layout