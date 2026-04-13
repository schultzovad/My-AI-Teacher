import streamlit as st
import google.generativeai as genai

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="AI Tutor Chat", layout="centered", page_icon="🎓")

# 2. PRIPOJENIE API (Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")

# Modely - poradie od najstabilnejšieho po najnovší
AVAILABLE_MODELS = ['gemini-1.5-flash-latest', 'gemini-2.0-flash', 'gemini-1.5-flash']

# PAMÄŤ ČETU
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. BOČNÝ PANEL (Súbory)
with st.sidebar:
    st.title("📁 Study Materials")
    uploaded_files = st.file_uploader(
        "Upload notes (JPG, PNG, PDF)", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.info(f"✅ {len(uploaded_files)} file(s) loaded and ready for chat.")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 4. HLAVNÝ ČET
st.title("💬 AI Tutor Chat")

# Zobrazenie histórie
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# VSTUP OD POUŽÍVATEĽA
if prompt := st.chat_input("Ask about your notes..."):
    
    # Pridáme správu do histórie
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ODPOVEĎ AI
    with st.chat_message("assistant"):
        container = st.empty()
        full_response = ""
        
        # Príprava "balíka" pre AI (Text + História + Súbory)
        payload = []
        
        # Systémová inštrukcia (aby AI vedela, kto je)
        payload.append("You are a friendly AI Tutor. Analyze the attached files and the chat history to help the student.")
        
        # Pridanie histórie správ
        for m in st.session_state.messages:
            payload.append(f"{m['role']}: {m['content']}")

        # PRIDANIE SÚBOROV (Toto zabezpečí, že AI ich uvidí spolu s textom)
        if uploaded_files:
            for f in uploaded_files:
                payload.append({'mime_type': f.type, 'data': f.getvalue()})

        success = False
        for model_name in AVAILABLE_MODELS:
            if success: break
            try:
                with st.spinner(f'Učiteľ premýšľa...'):
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(payload)
                    full_response = response.text
                    success = True
            except Exception as e:
                if "429" in str(e):
                    continue # Skúsi ďalší model v poradí
                else:
                    full_response = f"Vyskytla sa technická chyba: {e}"
                    break
        
        # Ak zlyhali všetky modely kvôli limitu
        if not success:
            st.warning("⚠️ **Príliš veľa študentov sa práve učí!**")
            full_response = "Naši AI učitelia sú momentálne trošku vyťažení. Prosím, dopraj im krátku, **30-sekundovú prestávku** na kávu a skús mi napísať znova. ☕😊"

        container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
