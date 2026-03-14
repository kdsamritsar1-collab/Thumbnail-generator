def get_distrokid_prompt(description, style_preset):
    style_map = {
        "Spiritual": "Cinematic lighting, serene, ethereal, soft golden hour, spiritual depth, 8k.",
        "Modern": "Minimalist, bold colors, high contrast, graphic design, 8k.",
        "Abstract": "Artistic, symbolic, creative textures, 8k."
    }
    refined_style = style_map.get(style_preset, "Professional album cover art, 8k.")
    return f"Create a 3000x3000px square cover art. Scene: {description}. Style: {refined_style}. NO TEXT, NO LOGOS."

def get_thumbnail_prompt(description, text, style_preset):
    style_map = {
        "Spiritual": "Cinematic lighting, warm golden tones, spiritual atmosphere, 4k.",
        "Modern": "Vibrant, bold colors, high-CTR YouTube design, 4k.",
        "Oil Painting": "Classical oil painting style, brushstrokes, 4k."
    }
    refined_style = style_map.get(style_preset, "High-quality YouTube thumbnail, 4k.")
    return f"Create a high-CTR YouTube thumbnail. Scene: {description}. Text Overlay: '{text}'. Style: {refined_style}. Text must be bold and clear."