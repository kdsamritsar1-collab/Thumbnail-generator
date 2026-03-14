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
        
       # --- FIXED RESPONSE LOGIC ---
        try:
            # Check if the AI actually generated an image
            if hasattr(response.candidates[0].content.parts[0], 'inline_data'):
                return response.candidates[0].content.parts[0].inline_data.data
            else:
                # Agar AI ne sirf text (description) likh kar bhej diya hai
                return "AI Error: The model provided a text description instead of an actual image. This usually happens when the specific Image Model is not active on your API key."
        except Exception as e:
            return f"Parsing Error: AI failed to generate image data. {e}"

