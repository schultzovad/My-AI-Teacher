import streamlit as st
import google.generativeai as genai
import json
import os

# 1. SETUP
st.set_page_config(page_title="AI Tutor Pro", layout="wide", page_icon="🎓")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")

AVAILABLE_MODELS = ['gemini-flash-latest', 'gemini-2.0-flash', 'gemini-pro-latest']
HISTORY_DIR = "chat_history"
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

# --- POMOCNÉ FUNKCIE ---
def save_chat(chat_name, messages):
    file_path = os.path.join(HISTORY_DIR, f"{chat_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

def load_all_chats():
    chats = {}
    if not os.path.exists(HISTORY_DIR): return chats
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    for file in files:
        name = file.replace(".json", "")
        with open(os.path.join(HISTORY_DIR, file), "r", encoding="utf-8") as f:
            chats[name] = json.load(f)
    return chats

def rename_chat_file(old_name, new_name):
    old_path = os.path.join(HISTORY_DIR, f"{old_name}.json")
    new_path = os.path.join(HISTORY_DIR, f"{new_name}.json")
    if os.path.exists(old_path):
        os.rename(old_path, new_path)

# NAČÍTANIE PRI ŠTARTE
if "chats" not in st.session_state:
    st.session_state.chats = load_all_chats()
    if not st.session_state.chats:
        st.session_state.chats = {"New Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# 2. SIDEBAR - SPRÁVA ČETOV
with st.sidebar:
    st.title("📂 Conversations")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_chat_id = f"Chat_{len(st.session_state.chats) + 1}"
        st.session_state.chats[new_chat_id] = []
        st.session_state.current_chat = new_chat_id
        save_chat(new_chat_id, [])
        st.rerun()
    
    st.write("---")
    
    for chat_name in list(st.session_state.chats.keys()):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            # Zvýraznený aktívny čet
            style = "primary" if chat_name == st.session_state.current_chat else "secondary"
            if st.button(f"💬 {chat_name}", key=f"btn_{chat_name}", use_container_width=True, type=style):
                st.session_state.current_chat = chat_name
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"del_{chat_name}"):
                os.remove(os.path.join(HISTORY_DIR, f"{chat_name}.json"))
                del st.session_state.chats[chat_name]
                st.session_state.current_chat = list(st.session_state.chats.keys())[0] if st.session_state.chats else "New Chat"
                st.rerun()

    # Možnosť manuálneho premenovania aktuálneho četu
    st.write("---")
    new_name_input = st.text_input("Rename current chat:", placeholder=st.session_state.current_chat)
    if st.button("Rename"):
        if new_name_input and new_name_input != st.session_state.current_chat:
            rename_chat_file(st.session_state.current_chat, new_name_input)
            st.session_state.chats[new_name_input] = st.session_state.chats.pop(st.session_state.current_chat)
            st.session_state.current_chat = new_name_input
            st.rerun()

# 3. MAIN UI
st.title(f"🎓 {st.session_state.current_chat}")

messages = st.session_state.chats[st.session_state.current_chat]
for m in messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

st.write("---")

# 4. UPLOADER & INPUT
with st.container():
    uploaded_files = st.file_uploader("Upload notes", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True, label_visibility="collapsed", key=f"up_{st.session_state.current_chat}")
    explain_btn = False
    if uploaded_files:
        if st.button("✨ Explain my uploaded files"):
            explain_btn = True

if input_text := st.chat_input("Ask a question..."):
    prompt = input_text
    process = True
elif explain_btn:
    prompt = "Please explain these files like a teacher and solve any problems."
    process = True
else:
    process = False

if process:
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
    st.rerun()

# 5. AI RESPONSE & AUTO-NAMING
if messages and messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        container = st.empty()
        
        # Logika pre odpoveď učiteľa
        teacher_payload = ["You are a kind teacher. Respond in the same language as user."]
        for m in messages[-6:]:
            teacher_payload.append(f"{m['role']}: {m['content']}")
        if uploaded_files:
            for f in uploaded_files:
                teacher_payload.append({'mime_type': f.type, 'data': f.getvalue()})

        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(teacher
