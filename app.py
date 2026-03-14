import streamlit as st
import nano_engine as engine
import prompts as pm
from PIL import Image
import requests
from io import BytesIO

# --- Page Config ---
st.set_page_config(page_title="Ruhani Studio", page_icon="🎨", layout="centered")

# --- Session State (Memory) ---
if "last_image" not in st.session_state: st.session_state.last_image = None
if "last_prompt" not in st.session_state: st.session_state.last_prompt = ""
if "last_text" not in st.session_state: st.session_state.last_text = ""

st.title("🎨 Ruhani Creative Studio v3.5")
st.caption("Advanced AI Thumbnail & Cover Art Suite for Ikjot Ruhani Records")

# --- API Keys ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Missing GEMINI_API_KEY in Secrets!")
    st.stop()

# --- Helper: YT Thumbnail Fetch ---
def get_yt_thumb(url):
    try:
        v_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
        response = requests.get(f"https://img.youtube.com/vi/{v_id}/maxresdefault.jpg")
        return Image.open(BytesIO(response.content))
    except: return None

# --- Main Tabs ---
tab1, tab2 = st.tabs(["📺 YouTube Thumbnail", "🎵 DistroKid Cover Art"])

# --- YT THUMBNAIL TAB ---
with tab1:
    desc = st.text_area("Background Scene Description", value=st.session_state.last_prompt, height=100)
    text = st.text_input("Text to write on Image", value=st.session_state.last_text)
    
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("Art Style", ["Spiritual", "Modern", "Oil Painting", "Default"])
        yt_link = st.text_input("Ref YT Link (Optional)")
    with col2:
        ratio = st.selectbox("Ratio", ["16:9", "1:1", "9:16"])
        ref_file = st.file_uploader("Ref File (Optional)", type=['jpg', 'png'])

    if st.button("✨ Generate Thumbnail"):
        final_ref = None
        if yt_link: final_ref = get_yt_thumb(yt_link)
        elif ref_file: final_ref = Image.open(ref_file)

        if desc:
            with st.spinner("AI is painting..."):
                st.session_state.last_prompt = desc
                st.session_state.last_text = text
                
                prompt = pm.get_thumbnail_prompt(desc, text, style)
                result = engine.generate_nano_image(API_KEY, prompt, ratio, final_ref)
                
                if isinstance(result, bytes):
                    st.session_state.last_image = Image.open(BytesIO(result))
                    st.image(result, use_container_width=True)
                    st.download_button("📥 Download", result, "thumbnail.png", "image/png")
                    st.rerun()
                elif result == "CREDIT_EXHAUSTED": st.error("Quota Over! Try tomorrow.")
                else: st.error(result)

    # --- Correction Feature ---
    if st.session_state.last_image:
        st.markdown("---")
        st.subheader("🔧 Correct Text / Refine Scene")
        new_text = st.text_input("Correct the text", value=st.session_state.last_text)
        if st.button("🔄 Fix Text & Re-Generate"):
            with st.spinner("Fixing text while keeping the same style..."):
                st.session_state.last_text = new_text
                prompt = pm.get_thumbnail_prompt(st.session_state.last_prompt, new_text, "Default")
                result = engine.generate_nano_image(API_KEY, prompt, "16:9", st.session_state.last_image)
                
                if isinstance(result, bytes):
                    st.session_state.last_image = Image.open(BytesIO(result))
                    st.image(result, use_container_width=True)
                    st.download_button("📥 Download Fixed", result, "fixed_thumbnail.png")
                else: st.error(result)

# --- DISTROKID TAB ---
with tab2:
    d_desc = st.text_area("Cover Description (3000x3000px)", placeholder="e.g. Golden abstract waves...")
    d_style = st.selectbox("Art Preset", ["Spiritual", "Modern", "Abstract"])
    
    if st.button("✨ Generate Cover Art"):
        if d_desc:
            with st.spinner("Designing DistroKid Cover..."):
                prompt = pm.get_distrokid_prompt(d_desc, d_style)
                result = engine.generate_nano_image(API_KEY, prompt, "1:1")
                if isinstance(result, bytes):
                    st.image(result, use_container_width=True)
                    st.download_button("📥 Download 3000px Art", result, "cover_art.png")
                else: st.error(result)