import streamlit as st
import nano_engine as engine
import prompts as pm
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="Ruhani Studio", page_icon="🎨", layout="centered")

# Session State
if "last_image" not in st.session_state: st.session_state.last_image = None
if "last_prompt" not in st.session_state: st.session_state.last_prompt = ""
if "last_text" not in st.session_state: st.session_state.last_text = ""

st.title("🎨 Ruhani Creative Studio v4.1")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Missing GEMINI_API_KEY in Secrets!")
    st.stop()

def get_yt_thumb(url):
    try:
        v_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
        res = requests.get(f"https://img.youtube.com/vi/{v_id}/maxresdefault.jpg")
        return Image.open(BytesIO(res.content))
    except: return None

tab1, tab2 = st.tabs(["📺 YouTube Thumbnail", "🎵 DistroKid Art"])

with tab1:
    desc = st.text_area("Scene Description", value=st.session_state.last_prompt)
    text = st.text_input("Text on Image", value=st.session_state.last_text)
    
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("Style", ["Spiritual", "Modern", "Oil Painting"])
        yt_link = st.text_input("Ref YT Link")
    with col2:
        ratio = st.selectbox("Ratio", ["16:9", "1:1", "9:16"])
        ref_file = st.file_uploader("Upload Ref Image", type=['jpg', 'png'])

    if st.button("✨ Generate"):
        if desc:
            with st.spinner("AI is painting..."):
                final_ref = None
                if yt_link: final_ref = get_yt_thumb(yt_link)
                elif ref_file: final_ref = Image.open(ref_file)

                st.session_state.last_prompt, st.session_state.last_text = desc, text
                result = engine.generate_nano_image(API_KEY, pm.get_thumbnail_prompt(desc, text, style), ratio, final_ref)
                
                if isinstance(result, bytes):
                    try:
                        # Validation before saving
                        img_obj = Image.open(BytesIO(result))
                        st.session_state.last_image = img_obj
                        st.image(result, use_container_width=True)
                        st.download_button("📥 Download", result, "thumb.png", "image/png")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Image Error: AI provided bytes but format is invalid. ({e})")
                elif "AI_TEXT_RESPONSE" in str(result):
                    st.warning("AI sent text instead of image:")
                    st.info(result.replace("AI_TEXT_RESPONSE:", ""))
                else:
                    st.error(result)

    # Correction Feature
    if st.session_state.last_image:
        st.markdown("---")
        st.subheader("🔧 Correct Text")
        fix_text = st.text_input("New Text", value=st.session_state.last_text)
        if st.button("🔄 Fix & Re-Generate"):
            with st.spinner("Correcting..."):
                st.session_state.last_text = fix_text
                res = engine.generate_nano_image(API_KEY, pm.get_thumbnail_prompt(st.session_state.last_prompt, fix_text, "Default"), ratio, st.session_state.last_image)
                if isinstance(res, bytes):
                    st.session_state.last_image = Image.open(BytesIO(res))
                    st.image(res, use_container_width=True)
                    st.rerun()
                else: st.error(res)

with tab2:
    d_desc = st.text_area("DistroKid Art Concept")
    if st.button("Generate 3000px Art"):
        res = engine.generate_nano_image(API_KEY, pm.get_distrokid_prompt(d_desc, "Spiritual"), "1:1")
        if isinstance(res, bytes):
            st.image(res, use_container_width=True)
            st.download_button("Download", res, "cover.png")