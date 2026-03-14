import streamlit as st
import nano_engine as engine
import prompts as pm
from PIL import Image
import requests
from io import BytesIO

# --- Page Setup ---
st.set_page_config(page_title="Ruhani Studio", page_icon="🎨", layout="centered")

# Initialize Session State
if "last_image" not in st.session_state: st.session_state.last_image = None
if "last_prompt" not in st.session_state: st.session_state.last_prompt = ""
if "last_text" not in st.session_state: st.session_state.last_text = ""
if "last_ratio" not in st.session_state: st.session_state.last_ratio = "16:9"

st.title("🎨 Ruhani Creative Studio v4.0")
st.caption("Official Studio for Ikjot Ruhani Records")

# API Key check
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Missing GEMINI_API_KEY in Secrets!")
    st.stop()

# YT Link Helper
def get_yt_thumb(url):
    try:
        v_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
        res = requests.get(f"https://img.youtube.com/vi/{v_id}/maxresdefault.jpg")
        return Image.open(BytesIO(res.content))
    except: return None

# Tabs
tab1, tab2 = st.tabs(["📺 YouTube Thumbnail", "🎵 DistroKid Cover"])

with tab1:
    desc = st.text_area("Scene Description", value=st.session_state.last_prompt, height=100)
    text = st.text_input("Text on Image", value=st.session_state.last_text)
    
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("Style", ["Spiritual", "Modern", "Oil Painting", "Default"])
        yt_link = st.text_input("Ref YouTube Link")
    with col2:
        ratio = st.selectbox("Ratio", ["16:9", "1:1", "9:16"], index=["16:9", "1:1", "9:16"].index(st.session_state.last_ratio))
        ref_file = st.file_uploader("Upload Ref Image", type=['jpg', 'png'])

    if st.button("✨ Generate Thumbnail"):
        if desc:
            with st.spinner("AI is painting..."):
                final_ref = None
                if yt_link: final_ref = get_yt_thumb(yt_link)
                elif ref_file: final_ref = Image.open(ref_file)

                st.session_state.last_prompt = desc
                st.session_state.last_text = text
                st.session_state.last_ratio = ratio
                
                result = engine.generate_nano_image(API_KEY, pm.get_thumbnail_prompt(desc, text, style), ratio, final_ref)
                
                if isinstance(result, bytes):
                    try:
                        img_data = BytesIO(result)
                        st.session_state.last_image = Image.open(img_data)
                        st.image(result, use_container_width=True)
                        st.download_button("📥 Download PNG", result, "thumbnail.png", "image/png")
                        st.rerun()
                    except: st.error("AI Error: Invalid image bytes received.")
                elif result == "CREDIT_EXHAUSTED": st.error("Quota Exceeded! Try tomorrow.")
                else: st.error(result)

    # --- TEXT CORRECTION ---
    if st.session_state.last_image:
        st.markdown("---")
        st.subheader("🔧 Correct Text / Refine Last Image")
        fix_text = st.text_input("Corrected Text", value=st.session_state.last_text)
        
        if st.button("🔄 Fix Text & Re-Generate"):
            with st.spinner("Fixing text..."):
                st.session_state.last_text = fix_text
                res = engine.generate_nano_image(API_KEY, pm.get_thumbnail_prompt(st.session_state.last_prompt, fix_text, "Default"), st.session_state.last_ratio, st.session_state.last_image)
                if isinstance(res, bytes):
                    st.session_state.last_image = Image.open(BytesIO(res))
                    st.image(res, use_container_width=True)
                    st.rerun()
                else: st.error(res)

with tab2:
    st.subheader("DistroKid Art (3000px Square)")
    d_desc = st.text_area("Art Concept", placeholder="Abstract golden flow...")
    if st.button("Generate Cover"):
        if d_desc:
            with st.spinner("Designing Art..."):
                res = engine.generate_nano_image(API_KEY, pm.get_distrokid_prompt(d_desc, "Spiritual"), "1:1")
                if isinstance(res, bytes):
                    st.image(res, use_container_width=True)
                    st.download_button("Download 3000px PNG", res, "cover_art.png")
                else: st.error(res)