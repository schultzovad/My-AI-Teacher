import streamlit as st
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="AI Tutor", layout="centered", page_icon="🎓")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")

AVAILABLE_MODELS = ['gemini-1.5-flash-latest', 'gemini-2.0-flash']

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. UI - HLAVNÁ ČASŤ
st.title("🎓 AI Tutor")
st.markdown("Upload notes or just ask a question. I'm here to help!")

# Nahrávanie súborov PRIAMO v hlavnom okne
with st.container():
    uploaded_files = st.file_uploader(
        "Attach notes (JPG, PNG, PDF)", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed" # Schováme label, aby to bolo čistejšie
    )

# Zobrazenie histórie četu
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. LOGIKA ODOSIELANIA
if prompt := st.chat_input("Ask something or send files..."):
    
    # Pridáme správu do histórie (aj keď je to len info o súboroch)
    user_content = prompt if prompt else "Analysis of uploaded files"
    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user"):
        st.markdown(user_content)

    with st.chat_message("assistant"):
        container = st.empty()
        payload = []
        
        # Inštrukcia pre AI
        system_msg = "You are a friendly AI Tutor. If the user sends files, analyze them. If they ask a question, answer it. Always use the language of the notes/user."
        payload.append(system_msg)
        
        # Pridanie histórie
        for m in st.session_state.messages:
            payload.append(f"{m['role']}: {m['content']}")

        # Pridanie súborov k TEJTO konkrétnej správe
        if uploaded_files:
            for f in uploaded_files:
                payload.append({'mime_type': f.type, 'data': f.getvalue()})
        
        # Ak nie je text ani súbor, nič nerobíme
        if not prompt and not uploaded_files:
            st.stop()

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
                    full_response = f"Technical glitch: {e}"
                    break
        
        if not success:
            st.warning("⚠️ **Too many students are studying right now!**")
            full_response = "Our AI teachers are taking a 30-second coffee break. Please try again in a moment! ☕😊"

        container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Tlačidlo na vymazanie četu v bočnej lište (nech nezavadzia v hlavnom okne)
with st.sidebar:
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
