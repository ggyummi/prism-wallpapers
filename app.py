import streamlit as st
import subprocess
import os
import glob
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Prism Wallpapers", page_icon="✨", layout="centered")

# 2. Custom CSS to make it look sleek like your inspiration site
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #2e66ff;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("✨ Prism Wallpapers GUI")
st.markdown("Generate luxury media backdrops and logo cards directly from your browser.")

# Function to grab the newest image created by the scripts
def get_latest_image():
    files = glob.glob("**/*.png", recursive=True) + glob.glob("**/*.jpg", recursive=True)
    if not files: 
        return None
    return max(files, key=os.path.getctime)

# 3. Create tabs for the two main tools
tab1, tab2 = st.tabs(["Backdrops", "Logo Cards"])

# -- BACKDROP UI --
with tab1:
    st.subheader("Backdrop Generator")
    tmdb_id = st.text_input("TMDB ID", placeholder="e.g. 87108")
    bg_type = st.selectbox("Type", ["network", "provider", "company", "genre"])
    
    if st.button("Generate Backdrop", key="btn_bg"):
        with st.spinner("Processing visual math and generating backdrop..."):
            # This triggers the backdrop_T2.py script just like a terminal would
            subprocess.run(["python", "backdrop_T2.py", "--id", tmdb_id, "--type", bg_type])
            
            latest_img = get_latest_image()
            if latest_img:
                st.image(Image.open(latest_img), caption="Your Generated Backdrop", use_container_width=True)
            else:
                st.error("No image was generated. Please check your TMDB ID.")

# -- LOGO CARD UI --
with tab2:
    st.subheader("Logo Card Generator")
    source = st.selectbox("Source", ["both", "tmdb", "custom"])
    bg_color = st.text_input("Background Code", value="0d0d11", help="Enter a Hex color or a Radial format string")
    
    if st.button("Generate Logo Card", key="btn_logo"):
        with st.spinner("Warping perspective and rendering..."):
            # This triggers the logo_cards.py script
            subprocess.run(["python", "logo_cards.py", "--source", source, "--bg", bg_color])
            
            latest_img = get_latest_image()
            if latest_img:
                st.image(Image.open(latest_img), caption="Your Generated Logo Card", use_container_width=True)
            else:
                st.error("Generation failed. Check your background format.")
