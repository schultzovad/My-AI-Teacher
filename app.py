import streamlit as st
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="AI Tutor Pro", layout="centered")

# 2. API KEY SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")

# Použijeme model 2.0, ktorý býva stabilnejší na limity, 
# ale ak chceš, pokojne prepíš späť na 2.5
model = genai.GenerativeModel('gemini-2.0-flash')

# 3. APP INTERFACE
st.title("📚 Advanced AI Tutor")
st.subheader("Upload multiple notes and ask specific questions")

# VIACNÁSOBNÉ NAHRÁVANIE (pridaný parameter accept_multiple_files)
uploaded_files = st.file_uploader(
    "Upload your notes (JPG, PNG, PDF)", 
    type=["jpg", "jpeg", "png", "pdf"],
    accept_multiple_files=True
)

# KOLÓNKA NA OTÁZKY
user_question = st.text_area(
    "Specific questions or focus (optional):", 
    placeholder="e.g., Explain the redox reactions in these notes..."
)

if uploaded_files:
    st.success(f"Uploaded {len(uploaded_files)} file(s).")
    
    if st.button('✨ Analyze & Answer'):
        # Pripravíme si zoznam súborov pre AI
        content_to_send = []
        
        # Ak užívateľ napísal otázku, pridáme ju do promptu, inak dáme základný
        base_prompt = """
        You are an expert teacher. Analyze all the provided documents together.
        1. Summarize the main topics across all files.
        2. Explain the key concepts simply.
        3. If there are specific questions from the user, answer them in detail.
        
        IMPORTANT: Always respond in the language used in the notes.
        """
        
        if user_question:
            full_prompt = f"{base_prompt}\n\nUSER'S SPECIFIC QUESTION: {user_question}"
        else:
            full_prompt = base_prompt
            
        content_to_send.append(full_prompt)

        # Pridáme všetky nahrané súbory
        for uploaded_file in uploaded_files:
            file_data = uploaded_file.getvalue()
            content_to_send.append({'mime_type': uploaded_file.type, 'data': file_data})
        
        with st.spinner('Analyzing everything...'):
            try:
                response = model.generate_content(content_to_send)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                if "429" in str(e):
                    st.error("Slow down! You've reached the limit. Wait 30 seconds and try again.")
                else:
                    st.error(f"Error: {e}")

st.markdown("---")
st.caption("AI Tutor Pro 2026 | Multi-file Edition 🎓")
