import streamlit as st
import google.generativeai as genai

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="AI Tutor Pro", layout="centered")

# 2. NASTAVENIE API KĽÚČA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")

# ZOZNAM MODELOV NA PREPÍNANIE (od najnovšieho po najstabilnejší)
# Ak jeden model zahlási chybu 429, kód automaticky skúsi ďalší
AVAILABLE_MODELS = [
    'gemini-2.5-flash', 
    'gemini-2.0-flash', 
    'gemini-1.5-flash-latest'
]

# 3. DIZAJN APLIKÁCIE
st.title("📚 AI Tutor Pro")
st.subheader("Multi-file Support & Smart Learning")

# Nahrávanie súborov
uploaded_files = st.file_uploader(
    "Upload your notes (JPG, PNG, PDF)", 
    type=["jpg", "jpeg", "png", "pdf"],
    accept_multiple_files=True
)

# Textové pole pre otázky
user_question = st.text_area(
    "What should I focus on?", 
    placeholder="e.g., Explain the formulas or create a short summary..."
)

if uploaded_files:
    if st.button('✨ Start Analysis'):
        # Príprava obsahu pre AI
        content_to_send = []
        
        # Základný prompt
        prompt = """
        You are a friendly and expert teacher. Analyze all the provided documents together.
        1. Summarize the main topics across all files.
        2. Explain the key concepts and formulas simply.
        3. Provide real-life examples.
        4. End with 3 quick review questions.
        
        IMPORTANT: Your response MUST be in the same language as the notes in the files.
        """
        
        if user_question:
            prompt += f"\n\nUSER'S SPECIFIC REQUEST: {user_question}"
        
        content_to_send.append(prompt)

        # Pridanie všetkých nahraných súborov
        for f in uploaded_files:
            content_to_send.append({'mime_type': f.type, 'data': f.getvalue()})

        # --- LOGIKA PREPÍNANIA MODELOV S PEKNOU HLÁŠKOU ---
        success = False
        
        for model_name in AVAILABLE_MODELS:
            if success: 
                break # Ak už máme odpoveď, nepokračujeme
            
            try:
                with st.spinner(f'Consulting our AI faculty...'):
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(content_to_send)
                    
                    # Ak sme sa dostali sem, všetko prebehlo v poriadku
                    st.success(f"Analysis complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                    success = True
            except Exception as e:
                # Ak je to chyba preťaženia (429), skúsime ďalší model v zozname
                if "429" in str(e):
                    continue 
                else:
                    # Ak je to iná chyba, vypíšeme ju pre tvoju informáciu
                    st.error(f"Technical glitch with {model_name}: {e}")
                    break

        # AK ZLYHALI ÚPLNE VŠETKY MODELY (Všetky sú preťažené)
        if not success:
            st.warning("⚠️ **Too many students are studying right now!**")
            st.info("""
                Our AI teachers are a bit overwhelmed by the interest. 
                Please give them a short **30-second break** to catch their breath and then try clicking the button again. 
                Thank you for your patience! 😊
            """)

# Pätička
st.markdown("---")
st.caption("Powered by Gemini Multi-Model Engine | Designed for your success 🎓")
