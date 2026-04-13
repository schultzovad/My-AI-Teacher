import streamlit as st
import google.generativeai as genai
import json
import os
import re
import unicodedata
from datetime import datetime

# 1. ZÁKLADNÉ NASTAVENIA
st.set_page_config(page_title="EduHub Pro", layout="wide", page_icon="🎓", initial_sidebar_state="expanded")

# Priečinky pre dáta
HISTORY_DIR = "chat_history"
FORUM_DIR = "shared_forum"
for d in [HISTORY_DIR, FORUM_DIR]:
    if not os.path.exists(d): os.makedirs(d)

SUBJECTS = ["Angličtina", "Matematika", "Dejepis", "Biológia", "Slovenčina", "Iné"]

# API kľúč (ak ho máš v secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- POMOCNÉ FUNKCIE ---
def save_chat(name, msgs):
    data = {"updated": datetime.now().strftime("%d.%m. %H:%M"), "messages": msgs}
    with open(os.path.join(HISTORY_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_all_chats():
    chats = {}
    for f in [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]:
        try:
            with open(os.path.join(HISTORY_DIR, f), "r", encoding="utf-8") as file:
                content = json.load(file)
                name = f.replace(".json", "")
                chats[name] = content if isinstance(content, dict) else {"updated": "", "messages": content}
        except: continue
    return chats

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^\w\s-]', '', text).strip()[:20]

# Slovník jazykov
LANG_MAP = {
    "SK": {"new_chat": "➕ Nový čet", "input": "Opýtaj sa AI...", "search": "🔍 Hľadať v histórii..."},
    "EN": {"new_chat": "➕ New Chat", "input": "Ask AI...", "search": "🔍 Search history..."}
    # (Sem si neskôr môžeš doplniť všetky tie FR, DE, ES ako predtým)
}

# Inicializácia stavu
if "lang" not in st.session_state: st.session_state.lang = "SK"
L = LANG_MAP.get(st.session_state.lang, LANG_MAP["SK"])
if "chats" not in st.session_state: st.session_state.chats = load_all_chats()
if not st.session_state.chats: st.session_state.chats = {"New Chat": {"updated": "", "messages": []}}
if "current_chat" not in st.session_state: st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# --- NAVIGÁCIA (MENU) ---
tab_chat, tab_forum, tab_groups = st.tabs(["💬 AI Tutor", "🏫 Verejné Fórum", "👥 Moje Skupiny"])

# ==========================================
# SEKCIA 1: AI TUTOR (TVOJ PÔVODNÝ KÓD)
# ==========================================
with tab_chat:
    with st.sidebar:
        st.selectbox("🌐 Jazyk UI", options=list(LANG_MAP.keys()), key="lang")
        st.title("📂 História")
        if st.button(L['new_chat'], use_container_width=True, type="primary"):
            nid = f"Chat_{len(st.session_state.chats)+1}"
            st.session_state.chats[nid] = {"updated": "", "messages": []}
            st.session_state.current_chat = nid; save_chat(nid, []); st.rerun()
        
        search = st.text_input(L['search'], label_visibility="collapsed")
        st.write("---")
        for cname in list(st.session_state.chats.keys()):
            if search.lower() in cname.lower():
                dt = st.session_state.chats[cname].get("updated", "")
                if st.button(f"💬 {cname}\n{dt}", key=f"b_{cname}", use_container_width=True, type="primary" if cname == st.session_state.current_chat else "secondary"):
                    st.session_state.current_chat = cname; st.rerun()

    # Displej četu
    st.title(f"🎓 {st.session_state.current_chat}")
    curr_data = st.session_state.chats.get(st.session_state.current_chat, {"messages": []})
    msgs = curr_data.get("messages", [])

    for m in msgs:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input(L['input']):
        msgs.append({"role": "user", "content": prompt})
        save_chat(st.session_state.current_chat, msgs)
        st.rerun()
        # (AI LOGIKA ostáva rovnaká ako predtým, kvôli dĺžke ju tu vynechávam, ale patrí sem)

# ==========================================
# SEKCIA 2: VEREJNÉ FÓRUM
# ==========================================
with tab_forum:
    st.title("🏫 Verejná knižnica materiálov")
    st.write("Tu môžete zdieľať poznámky a učiť sa spoločne.")
    
    selected_subject = st.selectbox("Vyber si predmet", SUBJECTS, key="forum_subject")
    
    col1, col2 = st.columns([0.6, 0.4])
    
    with col1:
        st.subheader(f"Zdieľané súbory: {selected_subject}")
        # Tu budeme neskôr vypisovať zoznam nahraných súborov
        st.info("Zatiaľ tu nie sú žiadne súbory pre tento predmet.")
        
    with col2:
        st.subheader("📤 Pridať nový materiál")
        f_name = st.text_input("Názov materiálu (napr. Poznámky z buniek)")
        f_upload = st.file_uploader("Nahraj PDF alebo obrázok", type=["pdf", "jpg", "png"], key="f_up")
        
        if st.button("Uverejniť na fórum"):
            if f_upload and f_name:
                # Uložíme súbor do priečinka shared_forum
                save_path = os.path.join(FORUM_DIR, f"{selected_subject}_{slugify(f_name)}_{f_upload.name}")
                with open(save_path, "wb") as f:
                    f.write(f_upload.getbuffer())
                st.success(f"Súbor '{f_name}' bol pridaný do predmetu {selected_subject}!")
            else:
                st.warning("Zadaj názov a vyber súbor.")

# ==========================================
# SEKCIA 3: MOJE SKUPINY
# ==========================================
with tab_groups:
    st.title("👥 Uzavreté skupiny")
    st.info("Táto funkcia bude dostupná po nastavení prihlasovacieho systému.")
