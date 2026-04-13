import streamlit as st
import google.generativeai as genai
import json
import os
import re
import unicodedata

# 1. SETUP
st.set_page_config(page_title="AI Tutor Pro", layout="wide", page_icon="🎓")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key in Secrets!")

AVAILABLE_MODELS = ['gemini-flash-latest', 'gemini-1.5-flash']
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
    # Odstránenie diakritiky a špeciálnych znakov pre bezpečnosť súborov
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    clean = re.sub(r'[^\w\s-]', '', text).strip()
    return clean[:25] if clean else "Untitled_Chat"

# NAČÍTANIE DÁT
if "chats" not in st.session_state:
    st.session_state.chats = load_all_chats()
    if not st.session_state.chats:
        st.session_state.chats = {"New Chat": []}

if "current_chat" not in st.session_state or st.session_state.current_chat not in st.session_state.chats:
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
            btn_style = "primary" if chat_name == st.session_state.current_chat else "secondary"
            if st.button(f"💬 {chat_name}", key=f"btn_{chat_name}", use_container_width=True, type=btn_style):
                st.session_state.current_chat = chat_name
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"del_{chat_name}"):
                try: os.remove(os.path.join(HISTORY_DIR, f"{chat_name}.json"))
                except: pass
                del st.session_state.chats[chat_name]
                st.session_state.current_chat = list(st.session_state.chats.keys())[0] if st.session_state.chats else "New Chat"
                if "New Chat" not in st.session_state.chats: st.session_state.chats["New Chat"] = []
                st.rerun()

# 3. MAIN UI
st.title(f"🎓 {st.session_state.current_chat}")
messages = st.session_state.chats.get(st.session_state.current_chat, [])

for m in messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 4. INPUT & ATTACHMENTS
st.write("---")
with st.container():
    uploaded_files = st.file_uploader("Upload notes", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True, label_visibility="collapsed", key=f"up_{st.session_state.current_chat}")
    
    analyze_clicked = False
    if uploaded_files:
        if st.button("✨ Explain my uploaded files"):
            analyze_clicked = True

if input_text := st.chat_input("Ask your teacher..."):
    prompt = input_text
    process = True
elif analyze_clicked:
    prompt = "Please explain these files like a teacher and solve any problems."
    process = True
else:
    process = False

if process:
    # Poistka pre existenciu četu
    if st.session_state.current_chat not in st.session_state.chats:
        st.session_state.chats[st.session_state.current_chat] = []
        
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
    st.rerun()

# 5. GENERATING RESPONSE (With Graceful Error Handling)
if messages and messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.status("Teacher is preparing the answer...", expanded=True) as status:
            
            # Nastavenie pre automatické meno
            is_new = st.session_state.current_chat.startswith("Chat_") or st.session_state.current_chat == "New Chat"
            needs_title = is_new and len(messages) <= 2
            
            system_msg = "You are a kind teacher. Respond in the user's language."
            if needs_title:
                system_msg += " IMPORTANT: Start your response with [TITLE: 2_word_english_title] then a newline, then your explanation."

            payload = [system_msg]
            for m in messages[-5:]:
                payload.append(f"{m['role']}: {m['content']}")
            if uploaded_files:
                for f in uploaded_files:
                    payload.append({'mime_type': f.type, 'data': f.getvalue()})

            try:
                model = genai.GenerativeModel('gemini-flash-latest')
                response_text = model.generate_content(payload).text
                
                final_text = response_text
                # Spracovanie názvu
                if "[TITLE:" in response_text:
                    parts = response_text.split("]", 1)
                    title_suggestion = parts[0].replace("[TITLE:", "").strip()
                    final_text = parts[1].strip()
                    
                    new_title = slugify(title_suggestion)
                    old_name = st.session_state.current_chat
                    if new_title and new_title != old_name:
                        old_path = os.path.join(HISTORY_DIR, f"{old_name}.json")
                        new_path = os.path.join(HISTORY_DIR, f"{new_title}.json")
                        if os.path.exists(new_path):
                            new_title = f"{new_title}_{os.urandom(2).hex()}"
                            new_path = os.path.join(HISTORY_DIR, f"{new_title}.json")
                        
                        if os.path.exists(old_path):
                            os.rename(old_path, new_path)
                        
                        st.session_state.chats[new_title] = st.session_state.chats.pop(old_name)
                        st.session_state.current_chat = new_title

                status.update(label="Answer ready!", state="complete", expanded=False)
                st.markdown(final_text)
                
                # Uloženie do pamäte a na disk
                if st.session_state.current_chat not in st.session_state.chats:
                    st.session_state.chats[st.session_state.current_chat] = []
                    
                st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": final_text})
                save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
                st.rerun()

            except Exception as e:
                err_str = str(e)
                if "429" in err_str:
                    status.update(label="Daily limit reached", state="error")
                    st.warning("😊 **Môj AI mozog si potrebuje oddýchnuť.** Dnes sme už prebrali veľa učiva a dosiahli sme denný limit (20 správ). Stretneme sa zajtra?")
                elif "safety" in err_str.lower():
                    status.update(label="Safety Filter", state="error")
                    st.info("⚠️ **O tomto téme nemôžem hovoriť.** Moje bezpečnostné pravidlá mi to nedovoľujú. Skúsme inú otázku!")
                else:
                    status.update(label="Technical hiccup", state="error")
                    st.error("🔌 **Mám malý technický problém.** Skús poslať správu znova, možno sa mi len zamotal kábel.")
                st.stop()
