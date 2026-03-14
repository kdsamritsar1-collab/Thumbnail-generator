import google.generativeai as genai

def generate_nano_image(api_key, refined_prompt, aspect_ratio, reference_img=None):
    try:
        genai.configure(api_key=api_key)
        
        # --- MODEL CHECK ---
        # Gemini 3 Flash Image (Nano Banana 2) is the ONLY one that makes images
        # gemini-1.5-flash image nahi banata, sirf description deta hai.
        selected_model = 'models/gemini-3-flash-image' 
        
        # Check if this model is actually available for your key
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if selected_model not in available_models:
            return f"Model Not Found: Your API Key does not support '{selected_model}' yet. Please use a key with Image Generation access."

        model = genai.GenerativeModel(selected_model)
        
        # Building Instruction
        final_prompt = f"{refined_prompt}. Output should be a high-quality image. Aspect Ratio: {aspect_ratio}."
        content = [final_prompt]
        
        if reference_img:
            content.append(reference_img)
            content.append("Reference Style: Copy the colors and lighting, but DO NOT include any text from this reference.")

        response = model.generate_content(content)
        
        # --- DATA EXTRACTION ---
        if response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            if hasattr(part, 'inline_data'):
                return part.inline_data.data
            else:
                # Agar AI ne description bhej di hai
                return f"AI_TEXT_RESPONSE: {part.text}"
        return "AI Error: Empty response."

    except Exception as e:
        msg = str(e).lower()
        if "429" in msg or "quota" in msg: return "CREDIT_EXHAUSTED"
        return f"Engine Error: {e}"