import streamlit as st
import google.generativeai as genai

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="AI Tutor Chat", layout="centered", page_icon="🎓")

# 2. API KEY SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")

# Zoznam modelov (nechávame tie najstabilnejšie)
AVAILABLE_MODELS = ['gemini-1.5-flash-latest', 'gemini-2.0-flash']

# --- PAMÄŤ ČETU (Session State) ---
# Toto zabezpečí, že správy nezmiznú pri každom kliknutí
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. UI - BOČNÝ PANEL PRE SÚBORY
with st.sidebar:
    st.title("📁 Documents")
    uploaded_files = st.file_uploader(
        "Upload notes for the AI context", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True
    )
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 4. HLAVNÁ ČETOVACIA ČASŤ
st.title("💬 AI Tutor Chat")
st.caption("Ask anything about your notes or just start a conversation.")

# Zobrazenie histórie správ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# VSTUP OD POUŽÍVATEĽA
if prompt := st.chat_input("What would you like to know?"):
    
    # 1. Pridáme správu používateľa do histórie a zobrazíme ju
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generovanie odpovede od AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Príprava kontextu (text + súbory)
        content_to_send = []
        
        # Pridáme inštrukciu pre správanie AI
        system_instruction = "You are a helpful AI Tutor. Use the uploaded files as context if available. Always respond in the language of the user or the notes."
        content_to_send.append(system_instruction)
        
        # Pridáme históriu (aby AI vedela, o čom sme hovorili predtým)
        for m in st.session_state.messages:
            content_to_send.append(f"{m['role']}: {m['content']}")

        # Pridáme súbory (ak sú nahrané)
        if uploaded_files:
            for f in uploaded_files:
                content_to_send.append({'mime_type': f.type, 'data': f.getvalue()})

        # Skúšame modely jeden po druhom
        success = False
        for model_name in AVAILABLE_MODELS:
            if success: break
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(content_to_send)
                full_response = response.text
                success = True
            except Exception as e:
                if "429" in str(e):
                    continue
                else:
                    full_response = f"Error with {model_name}: {e}"
                    break
        
        if not success:
            full_response = "⚠️ All models are busy. Please wait 30s and try again."

        # Zobrazenie odpovede a uloženie do histórie
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
