import streamlit as st
import google.generativeai as genai
import json
import os
import re

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
        try:
            with open(os.path.join(HISTORY_DIR, file), "r", encoding="utf-8") as f:
                chats[name] = json.load(f)
        except: continue
    return chats

def slugify(text):
    # Vyčistí názov od znakov, ktoré nemôžu byť v názve súboru
    return re.sub(r'[^\w\s-]', '', text).strip()[:30]

# NAČÍTANIE PRI ŠTARTE
if "chats" not in st.session_state:
    st.session_state.chats = load_all_chats()
    if not st.session_state.chats:
        st.session_state.chats = {"New Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# 2. SIDEBAR
with st.sidebar:
    st.title("📂 Conversations")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_id = f"Chat_{len(st.session_state.chats) + 1}"
        st.session_state.chats[new_id] = []
        st.session_state.current_chat = new_id
        save_chat(new_id, [])
        st.rerun()
    
    st.write("---")
    
    for chat_name in list(st.session_state.chats.keys()):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            btn_type = "primary" if chat_name == st.session_state.current_chat else "secondary"
            if st.button(f"💬 {chat_name}", key=f"btn_{chat_name}", use_container_width=True, type=btn_type):
                st.session_state.current_chat = chat_name
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"del_{chat_name}"):
                try:
                    os.remove(os.path.join(HISTORY_DIR, f"{chat_name}.json"))
                except: pass
                del st.session_state.chats[chat_name]
                st.session_state.current_chat = list(st.session_state.chats.keys())[0] if st.session_state.chats else "New Chat"
                st.rerun()

    st.write("---")
    manual_name = st.text_input("Rename chat:", placeholder="Type new name...")
    if st.button("Rename"):
        if manual_name and manual_name != st.session_state.current_chat:
            new_name = slugify(manual_name)
            old_path = os.path.join(HISTORY_DIR, f"{st.session_state.current_chat}.json")
            new_path = os.path.join(HISTORY_DIR, f"{new_name}.json")
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
            st.session_state.chats[new_name] = st.session_state.chats.pop(st.session_state.current_chat)
            st.session_state.current_chat = new_name
            st.rerun()

# 3. MAIN UI
st.title(f"🎓 {st.session_state.current_chat}")

messages = st.session_state.chats.get(st.session_state.current_chat, [])
for m in messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 4. UPLOADER & INPUT
st.write("---")
with st.container():
    uploaded_files = st.file_uploader("Upload notes", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True, label_visibility="collapsed", key=f"up_{st.session_state.current_chat}")
    explain_btn = False
    if uploaded_files:
        if st.button("✨ Explain my uploaded files"):
            explain_btn = True

if input_text := st.chat_input("Ask your teacher..."):
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

# 5. AI RESPONSE WITH STATUS INDICATOR
if messages and messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        # TOTO JE TÁ NOVÁ KONTROLKA ČAKANIA
        with st.status("Teacher is preparing the answer...", expanded=True) as status:
            
            # Príprava payloadu
            teacher_payload = ["You are a kind teacher. Respond in the user's language."]
            for m in messages[-6:]:
                teacher_payload.append(f"{m['role']}: {m['content']}")
            if uploaded_files:
                for f in uploaded_files:
                    teacher_payload.append({'mime_type': f.type, 'data': f.getvalue()})

            # Generovanie odpovede
            try:
                model = genai.GenerativeModel('gemini-flash-latest')
                response = model.generate_content(teacher_payload)
                teacher_text = response.text
                status.update(label="Answer ready!", state="complete", expanded=False)
                st.markdown(teacher_text)
                
                st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": teacher_text})
                save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
            except Exception as e:
                status.update(label="Something went wrong...", state="error")
                st.error(f"Error: {e}")
                st.stop()

            # AUTOMATICKÉ POMENOVANIE
            if len(st.session_state.chats[st.session_state.current_chat]) <= 2 and st.session_state.current_chat.startswith("Chat_"):
                status.update(label="Naming your conversation...", state="running", expanded=True)
                naming_query = f"Create a 2-3 word title for a chat starting with: '{prompt}'. Return only the title."
                try:
                    new_title_raw = model.generate_content(naming_query).text.strip()
                    new_title = slugify(new_title_raw)
                    
                    old_name = st.session_state.current_chat
                    old_path = os.path.join(HISTORY_DIR, f"{old_name}.json")
                    new_path = os.path.join(HISTORY_DIR, f"{new_title}.json")
                    
                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)
                    
                    st.session_state.chats[new_title] = st.session_state.chats.pop(old_name)
                    st.session_state.current_chat = new_title
                except: pass # Ak zlyhá pomenovanie, necháme pôvodné
        
        st.rerun()
