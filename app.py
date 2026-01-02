import streamlit as st
import requests
import io
import time
from PIL import Image

st.set_page_config(page_title="Final AI Lab", layout="wide")

# 1. THE TOKEN (Make sure it has "Read" permissions)
HF_TOKEN = "your_hf_token_here" 

# 2. THE NEW API URL (SD3 is much more reliable against 410 errors)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_model(prompt_text):
    # Added 'wait_for_model' to force the server to handle the loading
    payload = {
        "inputs": prompt_text,
        "options": {"wait_for_model": True, "use_cache": False}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.content
        else:
            return f"ERROR_{response.status_code}"
    except:
        return "TIMEOUT"

# --- UI ---
st.title("🏠 AI Interior Design Studio")

with st.sidebar:
    room = st.selectbox("Room", ["Living Room", "Bedroom"])
    style = st.selectbox("Style", ["Modern", "Minimalist"])
    color = st.color_picker("Color", "#3498db")
    run_btn = st.button("Generate Now")

if run_btn:
    prompt = f"Professional interior design, {style} {room}, {color} accents, high quality"
    with st.spinner("Model is inferencing..."):
        result = query_model(prompt)
        
        if isinstance(result, bytes):
            image = Image.open(io.BytesIO(result))
            st.image(image, use_container_width=True)
            st.success("Generation Complete!")
        else:
            st.error(f"Inference Error: {result}")
            st.info("If 410 persists, the Hugging Face free tier for this model is temporarily down. Use the 'Manual Blueprint' fallback below for your presentation.")
            
            # --- 3. THE EMERGENCY FALLBACK (SAVES YOUR PRESENTATION) ---
            from PIL import ImageDraw
            fallback = Image.new('RGB', (800, 400), color=color)
            draw = ImageDraw.Draw(fallback)
            draw.text((300, 180), f"{style} {room} Plan", fill="white")
            st.image(fallback, caption="AI Schematic (Fallback Mode)")
