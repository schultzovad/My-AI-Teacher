import streamlit as st
import google.generativeai as genai
import json
import os
import re
import unicodedata
from datetime import datetime

# 1. SETUP
st.set_page_config(page_title="AI Tutor Pro", layout="wide", page_icon="🎓", initial_sidebar_state="expanded")

LANG_MAP = {
    "SK": {"title": "Konverzácie", "new_chat": "➕ Nový čet", "rename": "Premenovať:", "upload": "Nahrať poznámky", "explain": "✨ Vysvetli", "input": "Opýtaj sa...", "status_think": "Premýšľam...", "status_ready": "Hotovo!", "limit_label": "Limit!", "safety_label": "Filter", "error_label": "Chyba", "limit_msg": "Limit dosiahnutý.", "safety_msg": "⚠️ Zakázané.", "error_msg": "🔌 Chyba.", "rename_btn": "Uložiť", "search": "🔍 Hľadať v histórii...", "clear_all": "🗑️ Zmazať všetko", "download": "📥 Stiahnuť čet"},
    "EN": {"title": "Conversations", "new_chat": "➕ New Chat", "rename": "Rename:", "upload": "Attach notes", "explain": "✨ Explain", "input": "Ask...", "status_think": "Thinking...", "status_ready": "Ready!", "limit_label": "Limit!", "safety_label": "Filter", "error_label": "Error", "limit_msg": "Limit reached.", "safety_msg": "⚠️ Restricted.", "error_msg": "🔌 Error.", "rename_btn": "Save", "search": "🔍 Search history...", "clear_all": "🗑️ Clear all", "download": "📥 Download chat"}
}

if "lang" not in st.session_state: st.session_state.lang = "SK"
L = LANG_MAP[st.session_state.lang]

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

HISTORY_DIR = "chat_history"
if not os.path.exists(HISTORY_DIR): os.makedirs(HISTORY_DIR)

# FUNKCIA NA UKLADANIE S DÁTUMOM
def save_chat(name, msgs):
    data = {
        "updated": datetime.now().strftime("%d.%m. %H:%M"), # TOTO JE TEN DÁTUM
        "messages": msgs
    }
    with open(os.path.join(HISTORY_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_all():
    chats = {}
    if not os.path.exists(HISTORY_DIR): return chats
    for f in [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]:
        try:
            with open(os.path.join(HISTORY_DIR, f), "r", encoding="utf-8") as file:
                chats[f.replace(".json", "")] = json.load(file)
        except: continue
    return chats

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^\w\s-]', '', text).strip()[:20]

if "chats" not in st.session_state: st.session_state.chats = load_all()
if not st.session_state.chats: st.session_state.chats = {"New Chat": {"updated": "", "messages": []}}
if "current_chat" not in st.session_state or st.session_state.current_chat not in st.session_state.chats:
    st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# --- SIDEBAR ---
with st.sidebar:
    st.selectbox("🌐 Language", options=list(LANG_MAP.keys()), key="lang")
    L = LANG_MAP[st.session_state.lang]
    st.title(f"📂 {L['title']}")
    
    if st.button(L['new_chat'], use_container_width=True, type="primary"):
        nid = f"Chat_{len(st.session_state.chats)+1}"
        st.session_state.chats[nid] = {"updated": "", "messages": []}
        st.session_state.current_chat = nid
        save_chat(nid, [])
        st.rerun()

    # TOTO JE TÁ LUPA (VYHĽADÁVANIE)
    search_term = st.text_input(L['search'], placeholder=L['search'], label_visibility="collapsed")
    
    st.write("---")
    
    for cname in list(st.session_state.chats.keys()):
        if search_term.lower() in cname.lower(): # Filtrovanie podľa lupy
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                subtext = st.session_state.chats[cname].get("updated", "")
                # Zobrazenie mena a dátumu na tlačidle
                if st.button(f"💬 {cname}\n{subtext}", key=f"b_{cname}", use_container_width=True, type="primary" if cname == st.session_state.current_chat else "secondary"):
                    st.session_state.current_chat = cname
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"d_{cname}"):
                    try: os.remove(os.path.join(HISTORY_DIR, f"{cname}.json"))
                    except: pass
                    del st.session_state.chats[cname]
                    st.session_state.current_chat = list(st.session_state.chats.keys())[0] if st.session_state.chats else "New Chat"
                    st.rerun()

    st.write("---")
    # TLAČIDLO NA ZMAZANIE VŠETKÉHO
    if st.button(L['clear_all'], use_container_width=True):
        for f in os.listdir(HISTORY_DIR): 
            try: os.remove(os.path.join(HISTORY_DIR, f))
            except: pass
        st.session_state.chats = {"New Chat": {"updated": "", "messages": []}}
        st.session_state.current_chat = "New Chat"
        st.rerun()

# --- HLAVNÁ PLOCHA ---
curr_data = st.session_state.chats.get(st.session_state.current_chat, {"messages": []})
msgs = curr_data.get("messages", [])

col_t1, col_t2 = st.columns([0.7, 0.3])
with col_t1:
    st.title(f"🎓 {st.session_state.current_chat}")
with col_t2:
    # TLAČIDLO NA EXPORT
    chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in msgs])
    st.download_button(L['download'], data=chat_text, file_name=f"{st.session_state.current_chat}.txt", use_container_width=True)

for m in msgs:
    with st.chat_message(m["role"]): st.markdown(m["content"])

st.write("---")
files = st.file_uploader(L['upload'], type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True, label_visibility="collapsed")

if prompt := st.chat_input(L['input']):
    msgs.append({"role": "user", "content": prompt})
    save_chat(st.session_state.current_chat, msgs)
    st.rerun()

# AI LOGIKA
if msgs and msgs[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.status(L['status_think'], expanded=True) as status:
            is_generic = st.session_state.current_chat.startswith("Chat_") or st.session_state.current_chat == "New Chat"
            sys_msg = f"Teacher mode. Language: {st.session_state.lang}."
            if is_generic and len(msgs) <= 2: sys_msg += " START WITH [TITLE: 2_word_title] THEN explanation."
            
            payload = [sys_msg] + [f"{m['role']}: {m['content']}" for m in msgs[-5:]]
            if files:
                for f in files: payload.append({'mime_type': f.type, 'data': f.getvalue()})

            try:
                res = genai.GenerativeModel('gemini-flash-latest').generate_content(payload).text
                final = res
                if "[TITLE:" in res:
                    parts = res.split("]", 1)
                    final = parts[1].strip()
                    new_t = slugify(parts[0].replace("[TITLE:", "").strip())
                    if new_t and new_t != st.session_state.current_chat:
                        old_p = os.path.join(HISTORY_DIR, f"{st.session_state.current_chat}.json")
                        new_p = os.path.join(HISTORY_DIR, f"{new_t}.json")
                        if os.path.exists(old_p): os.rename(old_p, new_p)
                        st.session_state.chats[new_t] = st.session_state.chats.pop(st.session_state.current_chat)
                        st.session_state.current_chat = new_t

                status.update(label=L['status_ready'], state="complete", expanded=False)
                st.markdown(final)
                msgs.append({"role": "assistant", "content": final})
                save_chat(st.session_state.current_chat, msgs)
                st.rerun()
            except Exception as e:
                status.update(label=L['error_label'], state="error")
                st.error(L['error_msg'])
                st.stop()
