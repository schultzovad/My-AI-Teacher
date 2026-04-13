import streamlit as st
import google.generativeai as genai

# 1. ZÁKLADNÉ NASTAVENIE STRÁNKY
st.set_page_config(page_title="AI Tutor Pro", layout="centered", page_icon="🎓")

# 2. PRIPOJENIE API KĽÚČA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")

# ZOZNAM MODELOV - zoradené od najvyššej kvóty po najnovšie preview
AVAILABLE_MODELS = [
    'gemini-1.5-flash-latest', 
    'gemini-1.5-flash',
    'gemini-2.0-flash',
    'gemini-2.5-flash'
]

# 3. DIZAJN APLIKÁCIE
st.title("📚 AI Tutor Pro")
st.markdown("Upload your notes and get instant explanations. Our AI supports images and PDFs!")

# Nahrávanie viacerých súborov naraz
uploaded_files = st.file_uploader(
    "Choose your notes (JPG, PNG, PDF)", 
    type=["jpg", "jpeg", "png", "pdf"],
    accept_multiple_files=True
)

# Priestor pre vlastné otázky
user_question = st.text_area(
    "What should I focus on?", 
    placeholder="e.g., Explain the chemical reactions or summarize the main dates in history..."
)

if uploaded_files:
    if st.button('✨ Start Analysis'):
        # Príprava podkladov pre AI
        content_to_send = []
        
        # Inštrukcia pre AI (Prompt)
        base_prompt = """
        You are a friendly and expert teacher. Analyze all the provided documents together.
        1. Summarize the main topics clearly.
        2. Explain the key concepts and formulas in a simple way.
        3. Provide a practical real-life example.
        4. End with 3 quick review questions to test my knowledge.
        
        IMPORTANT: Your response MUST be in the same language as the notes in the files.
        Use clean Markdown formatting, bullet points, and bold text.
        """
        
        if user_question:
            full_prompt = f"{base_prompt}\n\nUSER'S SPECIFIC REQUEST: {user_question}"
        else:
            full_prompt = base_prompt
            
        content_to_send.append(full_prompt)

        # Spracovanie nahraných súborov do formátu pre Gemini
        for f in uploaded_files:
            content_to_send.append({'mime_type': f.type, 'data': f.getvalue()})

        # --- LOGIKA PREPÍNANIA MODELOV ---
        success = False
        
        for model_name in AVAILABLE_MODELS:
            if success: 
                break
            
            try:
                # Tu nepoužívame spinner s názvom modelu, aby to používateľa neplietlo
                with st.spinner('Our AI faculty is reviewing your notes...'):
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(content_to_send)
                    
                    st.success("Analysis complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                    success = True
            except Exception as e:
                # Ak je to chyba limitu (429), skúšame ďalší model v zozname
                if "429" in str(e):
                    continue 
                else:
                    # Iné technické chyby vypíšeme
                    st.error(f"Technical issue: {e}")
                    break

        # FINÁLNA HLÁŠKA PRI PREŤAŽENÍ
        if not success:
            st.warning("⚠️ **Too many students are studying right now!**")
            st.info("""
                Our AI teachers are a bit overwhelmed. 
                Please wait about **30 to 60 seconds** for the limits to reset and then try clicking the button again. 
                Even AI needs a small coffee break! 😊
            """)

# Pätička
st.markdown("---")
st.caption("AI Tutor Pro | Powered by Gemini Multi-Model Engine 🎓")
