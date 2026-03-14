import google.generativeai as genai

def generate_nano_image(api_key, refined_prompt, aspect_ratio, reference_img=None):
    try:
        genai.configure(api_key=api_key)
        
        # मॉडल का नाम चेक करें (v1beta या standard)
        model = genai.GenerativeModel('gemini-3-flash-image')
        
        # प्रॉम्प्ट में रेश्यो (Size) की जानकारी जोड़ना
        final_instruction = f"{refined_prompt}. Please ensure the output image composition fits an aspect ratio of {aspect_ratio}."
        
        # इनपुट लिस्ट तैयार करना
        content = [final_instruction]
        if reference_img:
            content.append(reference_img)
            content.append("IMPORTANT: Use the style and colors from the reference, but COMPLETELY IGNORE any existing text in it.")

        # GenerationConfig से aspect_ratio हटा दिया गया है ताकि एरर न आए
        response = model.generate_content(
            content,
            generation_config={
                "output_mime_type": "image/png"
            }
        )
        
        return response.candidates[0].content.parts[0].inline_data.data
    
    except Exception as e:
        error_msg = str(e).lower()
        if "429" in error_msg or "quota" in error_msg:
            return "CREDIT_EXHAUSTED"
        return f"Engine Error: {e}"