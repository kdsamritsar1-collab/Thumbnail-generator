import google.generativeai as genai

def generate_nano_image(api_key, refined_prompt, aspect_ratio, reference_img=None):
    try:
        genai.configure(api_key=api_key)
        
        # --- AUTO-DETECT LOGIC START ---
        # Sabhi available models ki list nikalna
        models = genai.list_models()
        
        # Hume wo model chahiye jo 'generateContent' support kare aur jiske naam mein 'flash' ya 'image' ho
        # Nano Banana 2 (Gemini 3 Flash Image) ke liye priority check
        image_models = [
            m.name for m in models 
            if 'generateContent' in m.supported_generation_methods 
            and ('image' in m.name.lower() or 'flash' in m.name.lower())
        ]
        
        # Priority list: Jo model sabse naya aur best hai
        selected_model = None
        priority_order = [
            'models/gemini-3-flash-image',
            'models/gemini-1.5-flash',
            'models/gemini-pro-vision'
        ]
        
        for target in priority_order:
            if target in image_models:
                selected_model = target
                break
        
        # Agar priority wala nahi mila, toh pehla suitable model le lo
        if not selected_model and image_models:
            selected_model = image_models[0]
            
        if not selected_model:
            return "Engine Error: No suitable Image model found for this API Key."
        # --- AUTO-DETECT LOGIC END ---

        model = genai.GenerativeModel(selected_model)
        
        # Aspect Ratio ko instruction mein daalna
        final_instruction = f"{refined_prompt}. Aspect Ratio: {aspect_ratio}."
        
        content = [final_instruction]
        if reference_img:
            content.append(reference_img)
            content.append("Use the style of this reference, but ignore its text.")

        # Simple call without complex config to avoid 'Unknown field' errors
        response = model.generate_content(content)
        
        return response.candidates[0].content.parts[0].inline_data.data
    
    except Exception as e:
        error_msg = str(e).lower()
        if "429" in error_msg or "quota" in error_msg:
            return "CREDIT_EXHAUSTED"
        return f"Engine Error: {e}"