import google.generativeai as genai

def generate_nano_image(api_key, refined_prompt, aspect_ratio, reference_img=None):
    try:
        genai.configure(api_key=api_key)
        
        # Auto-detect models
        models = genai.list_models()
        image_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        priority = ['models/gemini-3-flash-image', 'models/gemini-1.5-flash']
        selected_model = next((m for m in priority if m in image_models), image_models[0] if image_models else None)
        
        if not selected_model:
            return "Engine Error: No AI model found."

        model = genai.GenerativeModel(selected_model)
        
        # Final prompt with size instructions
        final_instruction = f"{refined_prompt}. Aspect Ratio: {aspect_ratio}."
        content = [final_instruction]
        
        if reference_img:
            content.append(reference_img)
            content.append("Use the style of this image but ignore all text inside it.")

        # Simple call to avoid Syntax/Unknown Field errors
        response = model.generate_content(content)
        
        # Safety Check for image data
        if response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            if hasattr(part, 'inline_data'):
                return part.inline_data.data
            else:
                # Return text description if image fails
                return f"AI_TEXT_RESPONSE: {part.text if hasattr(part, 'text') else 'Safety Blocked'}"
        else:
            return "AI Error: Empty response."

    except Exception as e:
        msg = str(e).lower()
        if "429" in msg or "quota" in msg:
            return "CREDIT_EXHAUSTED"
        return f"Engine Error: {e}"