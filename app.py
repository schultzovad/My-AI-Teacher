import streamlit as st
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="AI Tutor", layout="centered")

# 2. API KEY SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")

# --- ZMENA TU: Skúšame najstabilnejšie volanie modelu ---
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. APP INTERFACE
st.title("📚 AI Tutor")
st.subheader("Turn your notes into clear explanations!")

uploaded_file = st.file_uploader("Upload your notes (JPG, PNG, PDF)", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    if st.button('✨ Explain these notes'):
        file_data = uploaded_file.getvalue()
        file_type = uploaded_file.type
        
        prompt = """
        You are a friendly and expert teacher. 
        Analyze the provided document and follow these steps:
        1. Give a brief summary of the topic.
        2. Explain the main concepts or formulas in a simple way.
        3. Provide a real-world example to help me understand better.
        4. End with 3 quick review questions.
        
        IMPORTANT: Your response MUST be in the same language as the notes in the file.
        Use clean Markdown formatting, bullet points, and bold text.
        """
        
        with st.spinner('Analyzing...'):
            try:
                # Skúsime vygenerovať obsah
                response = model.generate_content([
                    prompt,
                    {'mime_type': file_type, 'data': file_data}
                ])
                
                st.success("Analysis complete!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                # AK TO ZNOVA PADNE, skúsime automaticky záložný model
                st.warning("Primary model failed, trying backup model...")
                try:
                    backup_model = genai.GenerativeModel('gemini-pro-vision')
                    response = backup_model.generate_content([prompt, {'mime_type': file_type, 'data': file_data}])
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"Even backup failed. Error: {e2}")
                    st.info("Check if Gemini API is enabled in your Google AI Studio at https://aistudio.google.com/")

st.markdown("---")
st.caption("Powered by Gemini AI 🎓")
