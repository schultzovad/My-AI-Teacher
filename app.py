import streamlit as st
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="AI Tutor", layout="centered")

# 2. API KEY SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key in Streamlit Secrets!")

# Tu používame najnovšie stabilné označenie
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. APP INTERFACE
st.title("📚 AI Tutor")
st.subheader("Upload your notes and let's study!")

uploaded_file = st.file_uploader("Upload notes (JPG, PNG, PDF)", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    st.success("File ready!")
    
    if st.button('✨ Explain these notes'):
        file_data = uploaded_file.getvalue()
        file_type = uploaded_file.type
        
        prompt = """
        You are a friendly teacher. Analyze this document and:
        1. Summarize the topic.
        2. Explain main concepts simply.
        3. Give a real-life example.
        4. Provide 3 review questions.
        
        IMPORTANT: Use the same language as the notes.
        Format with bullet points and bold text.
        """
        
        with st.spinner('Thinking...'):
            try:
                # V novej verzii knižnice toto musí prejsť
                response = model.generate_content([
                    prompt,
                    {'mime_type': file_type, 'data': file_data}
                ])
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error detail: {e}")
                st.info("If you see 404, please wait 1 minute for the requirements.txt update to take effect.")

st.markdown("---")
st.caption("AI Tutor Project 🎓")
