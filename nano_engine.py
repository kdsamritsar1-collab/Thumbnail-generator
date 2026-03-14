import google.generativeai as genai

def generate_nano_image(api_key, refined_prompt, aspect_ratio, reference_img=None):
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        image_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        # Priority logic for models
        priority = ['models/gemini-3-flash-image', 'models/gemini-1.5-flash']
        selected_model = next((m for m in priority if m in image_models), image_models[0] if image_models else None)
        
        if not selected_model: return "No AI model found."

        model = genai.GenerativeModel(selected_model)
        content = [f"{refined_prompt}. Aspect Ratio: {aspect_ratio}."]
        
        if reference_img:
            content.append(reference_img)
            content.append("Use the style of this image but IGNORE any text inside it.")

        response = model.generate_content(content)
        
        # --- Critical Fix: Check for Image Data vs Text ---
        try:
            # Check if candidates exist and have parts
            if response.candidates and response.candidates[0].content.parts:
                part = response.candidates[0].content.parts[0]
                if hasattr(part, 'inline_data') and part.inline_data:
                    return part.inline_data.data
                else:
                    return f"AI Refusal: {part.text if hasattr(part, 'text') else 'Safety Blocked'}"
            else:
                return "AI Error: Empty response from model."
        except Exception as parse_err:
            return f"Parsing Error: {parse_err}"

    except Exception as e:
        msg = str(e).lower()
        if "429" in msg or "quota" in msg: return "CREDIT_EXHAUSTED"
        return f"Engine Error: {e}"