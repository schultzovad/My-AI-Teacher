import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# 1. SETUP
st.set_page_config(page_title="AI Tutor Pro", layout="wide", page_icon="🎓")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key in Secrets!")

AVAILABLE_MODELS = ['gemini-flash-latest', 'gemini-2.0-flash', 'gemini-pro-latest']

# CESTA K HISTÓRII
HISTORY_DIR = "chat_history"
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

# --- FUNKCIE PRE TRVALÉ UKLADANIE ---
def save_chat(chat_name, messages):
    file_path = os.path.join(HISTORY_DIR, f"{chat_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

def load_all_chats():
    chats = {}
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    for file in files:
        name = file.replace(".json", "")
        with open(os.path.join(HISTORY_DIR, file), "r", encoding="utf-8") as f:
            chats[name] = json.load(f)
    return chats

# NAČÍTANIE DÁT PRI ŠTARTE
if "chats" not in st.session_state:
    st.session_state.chats = load_all_chats()
    if not st.session_state.chats:
        st.session_state.chats = {"Default Chat": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# 2. SIDEBAR - PERMANENT HISTORY
with st.sidebar:
    st.title("📂 Saved Chats")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_name = f"Chat_{datetime.now().strftime('%H%M%S')}"
        st.session_state.chats[new_name] = []
        st.session_state.current_chat = new_name
        save_chat(new_name, []) # Vytvorí súbor
        st.rerun()
    
    st.write("---")
    
    for chat_name in list(st.session_state.chats.keys()):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button(f"💬 {chat_name}", key=f"btn_{chat_name}", use_container_width=True):
                st.session_state.current_chat = chat_name
                st.rerun()
        with col2:
            # Tlačidlo na vymazanie konkrétneho četu
            if st.button("🗑️", key=f"del_{chat_name}"):
                if chat_name in st.session_state.chats:
                    del st.session_state.chats[chat_name]
                    os.remove(os.path.join(HISTORY_DIR, f"{chat_name}.json"))
                    st.session_state.current_chat = list(st.session_state.chats.keys())[0] if st.session_state.chats else "Default Chat"
                    st.rerun()

# 3. MAIN INTERFACE
st.title(f"🎓 {st.session_state.current_chat}")

current_messages = st.session_state.chats[st.session_state.current_chat]
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.write("---")

# 4. ATTACHMENTS & INPUT
with st.container():
    uploaded_files = st.file_uploader(
        "Attach notes", type=["jpg", "jpeg", "png", "pdf"], 
        accept_multiple_files=True, label_visibility="collapsed", key=f"up_{st.session_state.current_chat}"
    )
    
    analyze_clicked = False
    if uploaded_files:
        if st.button("✨ Explain my uploaded files"):
            analyze_clicked = True

if input_text := st.chat_input("Ask a question..."):
    prompt = input_text
    process = True
elif analyze_clicked:
    prompt = "Please explain these files like a teacher and solve any problems."
    process = True
else:
    process = False

if process:
    # Uloženie správy užívateľa
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
    st.rerun()

# AI RESPONSE LOGIC
if current_messages and current_messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        container = st.empty()
        payload = ["You are a kind teacher. Explain humanly. Solve problems. Use the same language as user."]
        
        for m in current_messages[-6:]:
            payload.append(f"{m['role']}: {m['content']}")

        if uploaded_files:
            for f in uploaded_files:
                payload.append({'mime_type': f.type, 'data': f.getvalue()})

        success = False
        full_response = ""
        for model_name in AVAILABLE_MODELS:
            if success: break
            try:
                with st.spinner('Thinking...'):
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(payload)
                    full_response = response.text
                    success = True
            except: continue
        
        if not success:
            full_response = "Coffee break! ☕ Try again in 30s."

        container.markdown(full_response)
        # Uloženie odpovede asistenta
        st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": full_response})
        save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
        st.rerun()
