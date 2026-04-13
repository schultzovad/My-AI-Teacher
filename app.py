import streamlit as st
import google.generativeai as genai

# 1. ZÁKLADNÉ NASTAVENIE
st.set_page_config(page_title="AI Tutor Pro", layout="centered", page_icon="🎓")

# 2. PRIPOJENIE API KĽÚČA
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")

# ZOZNAM MODELOV (Presne podľa tvojho zoznamu, ktorý funguje)
AVAILABLE_MODELS = [
    'gemini-flash-latest',       # Stabilná verzia 1.5
    'gemini-2.0-flash',          # Verzia 2.0
    'gemini-pro-latest'          # Stabilná Pro verzia
]

# PAMÄŤ ČETU (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. DIZAJN APLIKÁCIE
st.title("🎓 AI Tutor")
st.markdown("Upload your notes or ask a quick question.")

# Hlavná sekcia pre nahrávanie súborov s tlačidlom
with st.container():
    uploaded_files = st.file_uploader(
        "Attach notes (JPG, PNG, PDF)", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    # Tlačidlo pre analýzu samotných súborov bez nutnosti písať text
    analyze_files_clicked = st.button("✨ Analyze Uploaded Files")

st.markdown("---")

# Zobrazenie histórie správ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. LOGIKA SPRACOVANIA VSTUPU
user_input = st.chat_input("Type your question here...")

# Kontrola, či niečo prišlo (buď cez tlačidlo alebo cez čet)
if analyze_files_clicked or user_input:
    
    # Ak klikne na tlačidlo bez textu, nastavíme predvolenú otázku
    final_text = user_input if user_input else "Please analyze the uploaded files and summarize the main points."
    
    # Pridáme správu do histórie
    st.session_state.messages.append({"role": "user", "content": final_text})
    with st.chat_message("user"):
        st.markdown(final_text)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Príprava dát pre AI
        payload = []
        payload.append("You are a friendly AI Tutor. Use the chat history and any uploaded files for context.")
        
        # Pridanie histórie (posledných 6 správ pre stabilitu)
        for m in st.session_state.messages[-6:]:
            payload.append(f"{m['role']}: {m['content']}")

        # Pridanie súborov (ak sú prítomné)
        if uploaded_files:
            for f in uploaded_files:
                payload.append({'mime_type': f.type, 'data': f.getvalue()})

        success = False
        error_msg = ""
        
        # Skúšame dostupné modely
        for model_name in AVAILABLE_MODELS:
            if success: break
            try:
                with st.spinner('AI faculty is thinking...'):
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(payload)
                    full_text = response.text
                    success = True
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg:
                    continue # Skúsi ďalší model kvôli limitu
                else:
                    # Ak je to iná technická chyba (napr. 404), vypíšeme ju a skúsime ďalší
                    continue

        if success:
            response_placeholder.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})
        else:
            # Ak zlyhalo úplne všetko
            if "429" in error_msg:
                st.warning("⚠️ **Too many students are studying right now!**")
                response_placeholder.markdown("Our AI teachers are taking a 30-second coffee break. Please wait a moment and try again! ☕😊")
            else:
                st.error(f"Technical glitch: {error_msg}")

# Bočný panel pre čistenie četu
with st.sidebar:
    st.title("Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
