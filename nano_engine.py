import google.generativeai as genai

def generate_nano_image(api_key, refined_prompt, aspect_ratio, reference_img=None):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-flash-image')
        
        # Build Content List
        content = [refined_prompt]
        if reference_img:
            content.append(reference_img)
            # Instruct AI to only take style/vibe, not the old text
            content.append("IMPORTANT: Use the style and colors from the reference image, but COMPLETELY IGNORE any text or words present in it.")

        response = model.generate_content(
            content,
            generation_config={
                "aspect_ratio": aspect_ratio,
                "output_mime_type": "image/png"
            }
        )
        return response.candidates[0].content.parts[0].inline_data.data
    
    except Exception as e:
        error_msg = str(e).lower()
        if "429" in error_msg or "quota" in error_msg:
            return "CREDIT_EXHAUSTED"
        return f"Engine Error: {e}"