import google.generativeai as genai

def generate_nano_image(api_key, refined_prompt, aspect_ratio, reference_img=None):
    try:
        genai.configure(api_key=api_key)
        
        # --- AUTO-DETECT WORKING MODEL ---
        models = genai.list_models()
        image_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods and ('image' in m.name.lower() or 'flash' in m.name.lower())]
        
        # Priority: Nano Banana 2 (Gemini 3 Flash Image) then Fallback
        priority_order = ['models/gemini-3-flash-image', 'models/gemini-1.5-flash']
        selected_model = next((m for m in priority_order if m in image_models), image_models[0] if image_models else None)
        
        if not selected_model:
            return "Engine Error: No suitable AI model found."

        model = genai.GenerativeModel(selected_model)
        
        # Building Instruction
        final_prompt = f"{refined_prompt}. Aspect Ratio: {aspect_ratio}."
        content = [final_prompt]
        
        if reference_img:
            content.append(reference_img)
            content.append("IMPORTANT: Use the style/colors of this reference, but COMPLETELY IGNORE all text inside it.")

        response = model.generate_content(content)
        
        # --- DATA VALIDATION (Prevents PIL Errors) ---
        try:
            part = response.candidates[0].content.parts[0]
            if hasattr(part, 'inline_data'):
                return part.inline_data.data
            else:
                return f"AI Refusal: {part.text}"
        except:
            return "AI Error: Model failed to provide valid image data."

    except Exception as e:
        msg = str(e).lower()
        if "429" in msg or "quota" in msg: return "CREDIT_EXHAUSTED"
        return f"Engine Error: {e}"