import streamlit as st
from openai import OpenAI

# 1. Setup OpenAI Client using your Streamlit Secrets
# This looks for the "OPENAI_API_KEY" you pasted in the Secrets dashboard
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Interior Designer", layout="wide")

st.title("🏡 Smart AI Interior Designer")
st.write("Fill in your requirements below to generate a professional room design.")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("📌 Room Specifications")
    
    room_name = st.text_input("Room Name (e.g., Master Bedroom, Gaming Studio)", "Modern Living Room")
    
    room_shape = st.selectbox("Room Shape", 
                              ["Rectangular", "Square", "L-Shaped", "Open Plan", "Circular"])
    
    budget = st.select_slider("Budget Level", 
                              options=["Low Budget", "Standard", "Premium", "Ultra-Luxury"])
    
    primary_color = st.color_picker("Choose Theme Color", "#3498db")
    
    st.divider()
    generate_btn = st.button("Generate My Design ✨")

# --- MAIN LOGIC ---
if generate_btn:
    # Constructing a detailed prompt using your inputs
    # The prompt engineering here ensures the AI understands "Budget" and "Shape"
    prompt = (
        f"A professional photorealistic interior design of a {room_shape} {room_name}. "
        f"The design should strictly follow a {budget} style with a color palette "
        f"centered around {primary_color}. High-end lighting, detailed textures, 8k resolution."
    )
    
    with st.spinner(f"Creating your {budget} {room_name}..."):
        try:
            # Calling DALL-E 3
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            # Display the result
            image_url = response.data[0].url
            st.subheader(f"✅ Generated Design: {room_name}")
            st.image(image_url, use_column_width=True)
            st.success("Design complete! You can right-click the image to save it.")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Tip: Ensure your OpenAI API key has enough credits.")
