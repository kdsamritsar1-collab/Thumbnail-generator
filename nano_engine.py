import google.generativeai as genai

def generate_nano_image(api_key, refined_prompt, aspect_ratio, reference_img=None):
    try:
        genai.configure(api_key=api_key)
        
        # Model selection
        model = genai.GenerativeModel('gemini-3-flash-image')
        
        # Aspect ratio instruction ko prompt ke andar hi bhej rahe hain
        final_instruction = f"{refined_prompt}. Aspect Ratio: {aspect_ratio}. Ensure the composition fits this size."
        
        # Inputs list
        content = [final_instruction]
        if reference_img:
            content.append(reference_img)
            content.append("Use the style/colors of this reference, but ignore all its text.")

        # GenerationConfig ko bilkul simple rakha hai taaki error na aaye
        response = model.generate_content(content)
        
        # Image data extract karna
        return response.candidates[0].content.parts[0].inline_data.data
    
    except Exception as e:
        error_msg = str(e).lower()
        if "429" in error_msg or "quota" in error_msg:
            return "CREDIT_EXHAUSTED"
        return f"Engine Error: {e}"