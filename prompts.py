def get_distrokid_prompt(description, style_preset):
    style_map = {
        "Spiritual": "Cinematic lighting, serene, ethereal, soft golden hour, spiritual depth, 8k, photorealistic.",
        "Modern": "Minimalist, bold colors, high contrast, clean lines, professional graphic design, 8k.",
        "Abstract": "Artistic, symbolic, creative textures, non-literal, 8k resolution."
    }
    refined_style = style_map.get(style_preset, "Professional album cover art, 8k resolution.")
    
    return f"""
    Create a 3000x3000px square cover art for music distribution.
    Scene: {description}.
    Style: {refined_style}.
    STRICT RULE: Absolutely NO TEXT, NO LOGOS, NO URLs. Clean artwork only.
    """

def get_thumbnail_prompt(description, text, style_preset):
    style_map = {
        "Spiritual": "Cinematic lighting, warm golden tones, traditional spiritual atmosphere, 4k.",
        "Modern": "Vibrant, bold colors, high-CTR professional YouTube design, 4k.",
        "Oil Painting": "Classical oil painting style, thick brushstrokes, artistic, 4k."
    }
    refined_style = style_map.get(style_preset, "High-quality YouTube thumbnail, 4k.")

    return f"""
    Create a high-CTR YouTube thumbnail.
    Scene: {description}.
    Text Overlay: '{text}'.
    Style: {refined_style}.
    Ensure text is bold, legible, and clear.
    """