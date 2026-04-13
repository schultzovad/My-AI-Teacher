import streamlit as st
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="AI Tutor", layout="centered", page_icon="🎓")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")

# Skúsime na prvé miesto stabilnejší model
AVAILABLE_MODELS = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-2.0-flash']

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. UI
st.title("🎓 AI Tutor")

# Nahrávanie súborov + tlačidlo na analýzu
with st.expander("📁 Upload notes / photos", expanded=True):
    uploaded_files = st.file_uploader(
        "Attach images or PDFs", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    analyze_button = st.button("✨ Analyze Files")

# Zobrazenie histórie
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. LOGIKA (Spracovanie vstupu)
input_prompt = st.chat_input("Ask a question...")

# Ak užívateľ klikol na tlačidlo ANALYZE alebo napísal text
if analyze_button or input_prompt:
    
    # Určíme, čo je textový vstup
    current_user_text = input_prompt if input_prompt else "Analyze these files, please."
    
    # Pridáme do histórie
    st.session_state.messages.append({"role": "user", "content": current_user_text})
    with st.chat_message("user"):
        st.markdown(current_user_text)

    with st.chat_message("assistant"):
        container = st.empty()
        payload = []
        
        # Inštrukcie
        payload.append("You are a friendly AI Tutor. Analyze files if provided. Answer questions clearly in the language of the notes.")
        
        # História (posledných 5 správ, aby sme nepreťažili limit)
        for m in st.session_state.messages[-6:]:
            payload.append(f"{m['role']}: {m['content']}")

        # Súbory
        if uploaded_files:
            for f in uploaded_files:
                payload.append({'mime_type': f.type, 'data': f.getvalue()})

        success = False
        for model_name in AVAILABLE_MODELS:
            if success: break
            try:
                with st.spinner('Thinking...'):
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(payload)
                    full_response = response.text
                    success = True
            except Exception as e:
                if "429" in str(e):
                    continue
                else:
                    st.error(f"Technical glitch: {e}")
                    break
        
        if not success:
            st.warning("⚠️ **Too many students are studying right now!**")
            full_response = "Our AI teachers are taking a 30-second coffee break. Please try again in a moment! ☕😊"

        container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with st.sidebar:
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
