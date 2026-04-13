import streamlit as st
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="AI Tutor Pro", layout="wide", page_icon="🎓")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")

# Stabilné názvy modelov
AVAILABLE_MODELS = ['gemini-flash-latest', 'gemini-2.0-flash', 'gemini-pro-latest']

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. BOČNÁ LIŠTA (Vždy po ruke)
with st.sidebar:
    st.title("📁 Attachments")
    st.markdown("Upload files here. They stay available even as you scroll the chat.")
    uploaded_files = st.file_uploader(
        "Upload notes/images", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True,
        key="sidebar_uploader"
    )
    
    if uploaded_files:
        st.success(f"Attached: {len(uploaded_files)} file(s)")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 3. HLAVNÁ ČASŤ (Chat)
st.title("💬 AI Tutor Chat")

# Zobrazenie správ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. LOGIKA (Spracovanie)
if prompt := st.chat_input("Write a message or ask to solve the attached files..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        container = st.empty()
        payload = []
        
        # PRÍSNEJŠIA INŠTRUKCIA: Rieš príklady hneď!
        system_instruction = """
        You are an expert AI Tutor. 
        CRITICAL: If the user uploads an image or document with mathematical problems, exercises, or questions, 
        your FIRST priority is to SOLVE them immediately and show the step-by-step calculation. 
        Do not just describe the topic unless asked. Solve first, explain after.
        Always respond in the language of the user/notes.
        """
        payload.append(system_instruction)
        
        # História
        for m in st.session_state.messages[-10:]:
            payload.append(f"{m['role']}: {m['content']}")

        # Súbory z bočnej lišty
        if uploaded_files:
            for f in uploaded_files:
                payload.append({'mime_type': f.type, 'data': f.getvalue()})

        success = False
        for model_name in AVAILABLE_MODELS:
            if success: break
            try:
                with st.spinner('Calculating...'):
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(payload)
                    full_response = response.text
                    success = True
            except Exception as e:
                if "429" in str(e): continue
                else:
                    st.error(f"Error: {e}")
                    break
        
        if not success:
            st.warning("⚠️ Teachers are on a break (Quota exceeded). Try again in 30s.")
            full_response = "Naši AI učitelia majú práve pauzu. Skús to prosím o chvíľku znova! ☕"

        container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
