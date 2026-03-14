import google.generativeai as genai

def generate_nano_image(api_key, refined_prompt, aspect_ratio, reference_img=None):
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        image_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        # Priority logic
        priority = ['models/gemini-3-flash-image', 'models/gemini-1.5-flash']
        selected_model = next((m for m in priority if m in image_models), image_models[0] if image_models else None)
        
        if not selected_model: return "No suitable model found."

        model = genai.GenerativeModel(selected_model)
        content = [f"{refined_prompt}. Aspect Ratio: {aspect_ratio}."]
        
        if reference_img:
            content.append(reference_img)
            content.append("Use the style of this image but ignore any text inside it.")

        # Specific call for image models
        response = model.generate_content(content)
        
        # Extracting Data Safely
        if not response.candidates: return "AI Error: No candidates found."
        
        part = response.candidates[0].content.parts[0]
        
        # Checking for true image bytes
        if hasattr(part, 'inline_data') and part.inline_data:
            return part.inline_data.data
        elif hasattr(part, 'text') and part.text:
            return f"AI_TEXT_RESPONSE: {part.text}"
        else:
            return "AI Error: Model blocked generation or returned empty data."

    except Exception as e:
        msg = str(e).lower()
        if "429" in msg or "quota" in msg: return "CREDIT_EXHAUSTED"
        return f"Engine Error: {e}"