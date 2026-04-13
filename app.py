import streamlit as st
import google.generativeai as genai
import os

# 1. PAGE SETUP
st.set_page_config(page_title="AI Tutor", layout="centered")

# 2. API KEY SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key in Streamlit Secrets!")

# --- ZMENA: Skúsime získať model iným spôsobom ---
@st.cache_resource
def load_model():
    # Toto povie Googlu: "Daj mi flash model a nerieš verziu API"
    return genai.GenerativeModel(model_name="gemini-1.5-flash")

model = load_model()

# 3. APP INTERFACE
st.title("📚 AI Tutor")
st.subheader("Upload your notes and let's study!")

uploaded_file = st.file_uploader("Upload notes (JPG, PNG, PDF)", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    st.success("File uploaded! Ready to analyze.")
    
    if st.button('✨ Explain these notes'):
        # Spracovanie súboru
        file_bits = uploaded_file.read()
        
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
                # Skúsime to poslať v najjednoduchšom možnom formáte
                response = model.generate_content([
                    prompt,
                    {'mime_type': uploaded_file.type, 'data': file_bits}
                ])
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                # Ak to zlyhá, vypíšeme zoznam modelov, ktoré máš dostupné
                st.error(f"Error: {e}")
                st.write("Checking available models for your API key...")
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                st.write("Available models:", models)

st.markdown("---")
st.caption("AI Tutor Project 🎓")
