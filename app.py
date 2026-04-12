import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. PAGE SETUP
st.set_page_config(page_title="AI Tutor", layout="centered")

# 2. API KEY SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")

model = genai.GenerativeModel('gemini-1.5-flash')

# 3. APP DESIGN
st.title("📚 Your AI Tutor")
st.subheader("Upload a photo of your notes and I'll explain it!")

# File uploader
uploaded_file = st.file_uploader("Choose a photo (JPG, PNG) or PDF...", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Notes uploaded successfully!', use_column_width=True)
    
    if st.button('✨ Explain it to me'):
        
        # ZMENA JE TU: Inštrukcia, aby AI odpovedala v jazyku poznámok
        prompt = """
        You are a friendly and patient teacher. 
        Look at this image/document and do the following:
        1. Summarize what these notes are about.
        2. Explain the main concepts and topics simply.
        3. Use a real-life example for complex parts.
        4. Provide 3 short review questions at the end.
        
        IMPORTANT: Use the same language for your response as the language used in the notes.
        Use clear formatting, bullet points, and bold text.
        """
        
        with st.spinner('Reading your notes...'):
            try:
                response = model.generate_content([prompt, image])
                st.success("Done!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Ups, something went wrong: {e}")

st.markdown("---")
st.caption("Created for your academic success 🎓")
