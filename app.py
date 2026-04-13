import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Tutor", layout="centered")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")

# POUŽÍVAME MODEL Z TVOJHO ZOZNAMU
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("📚 AI Tutor")
st.subheader("Powered by Gemini 2.5 Flash")

uploaded_file = st.file_uploader("Upload notes (JPG, PNG, PDF)", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    if st.button('✨ Explain these notes'):
        file_data = uploaded_file.getvalue()
        
        prompt = """
        You are a friendly teacher. Analyze this document and:
        1. Summarize the topic.
        2. Explain main concepts simply.
        3. Give a real-life example.
        4. Provide 3 review questions.
        IMPORTANT: Use the same language as the notes.
        """
        
        with st.spinner('Thinking with Gemini 2.5...'):
            try:
                response = model.generate_content([
                    prompt,
                    {'mime_type': uploaded_file.type, 'data': file_data}
                ])
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("AI Tutor 2026 Edition 🎓")
