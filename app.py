import streamlit as st
import google.generativeai as genai
import json
import os
import re
import unicodedata

# 1. ZÁKLADNÉ NASTAVENIE
st.set_page_config(page_title="EduHub Pro", layout="wide", page_icon="🎓", initial_sidebar_state="collapsed") # Schovali sme sidebar pre čistejší vzhľad

HISTORY_DIR = "chat_history"
FORUM_DIR = "shared_forum"
for d in [HISTORY_DIR, FORUM_DIR]:
    if not os.path.exists(d): os.makedirs(d)

# 2. INTELIGENTNÁ NAVIGÁCIA CEZ URL
# Prečítame si, čo chce Framer (napr. ?p=forum)
query_params = st.query_params
requested_page = query_params.get("p", "chat") # Ak v URL nič nie je, predvolíme chat

# Mapovanie URL parametrov na indexy našich tabov
page_map = {"chat": 0, "forum": 1, "groups": 2}
current_tab_index = page_map.get(requested_page, 0)

# 3. SLOVNÍK (nechávam len SK/EN pre stručnosť kódu tu, ty si tam nechaj všetky)
LANG_MAP = {
    "SK": {
        "chat": "💬 AI Tutor", "forum": "🏫 Fórum", "groups": "👥 Skupiny", 
        "new_chat": "➕ Nový čet", "search": "Hľadaj...", "upload_label": "Nahraj súbor", 
        "subject": "Predmet", "files": "Súbory", "input": "Opýtaj sa AI...", 
        "status_think": "Premýšľam...", "status_ready": "Hotovo!", 
        "learn_with_ai": "🤖 Uč sa s AI", "mat_title": "Názov", "upload_btn": "Uverejniť",
        "groups_msg": "Sekcia je uzamknutá.", "lang_label": "🌐 Jazyk",
        "subjects": ["Angličtina", "Matematika", "Dejepis", "Biológia", "Slovenčina", "Iné"]
    },
    "EN": {
        "chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Groups", 
        "new_chat": "➕ New Chat", "search": "Search...", "upload_label": "Upload file", 
        "subject": "Subject", "files": "Files", "input": "Ask AI...", 
        "status_think": "Thinking...", "status_ready": "Ready!", 
        "learn_with_ai": "🤖 Learn with AI", "mat_title": "Title", "upload_btn": "Publish",
        "groups_msg": "Section locked.", "lang_label": "🌐 Language",
        "subjects": ["English", "Mathematics", "History", "Biology", "Other"]
    }
}

if "lang" not in st.session_state: st.session_state.lang = "SK"
L = LANG_MAP[st.session_state.lang]

# 4. POMOCNÉ FUNKCIE (Už bez času, ako sme sa dohodli)
def save_chat(name, msgs):
    with open(os.path.join(HISTORY_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump({"messages": msgs}, f, ensure_ascii=False, indent=4)

def load_all_chats():
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

# --- VLASTNÝ ŠTÝL (CSS), ABY TO SPLYNULO S WEBOM ---
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { display: none; } /* Schováme horné prepínače Streamlitu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HLAVNÉ MENU (Taby sú teraz riadené URL parametrom z Frameru) ---
tabs = st.tabs(["AI", "Forum", "Groups"])

# ==========================================
# SEKCIA 1: AI TUTOR (Index 0)
# ==========================================
with tabs[0]:
    if current_tab_index == 0:
        with st.sidebar:
            st.selectbox(L["lang_label"], options=list(LANG_MAP.keys()), key="lang")
            L = LANG_MAP[st.session_state.lang]
            st.title(f"📂 {L['chat']}")
            
            if st.button(L['new_chat'], use_container_width=True, type="primary"):
                nid = f"Chat_{len(load_all_chats())+1}"
                save_chat(nid, [])
                st.session_state.current_chat = nid; st.rerun()
            
            search_term = st.text_input("Search", placeholder=L['search'], label_visibility="collapsed")
            st.write("---")
            all_chats = load_all_chats()
            for cname in list(all_chats.keys()):
                if search_term.lower() in cname.lower():
                    col_btn, col_del = st.columns([0.8, 0.2])
                    with col_btn:
                        if st.button(f"💬 {cname}", key=f"b_{cname}", use_container_width=True):
                            st.session_state.current_chat = cname; st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_{cname}"):
                            os.remove(os.path.join(HISTORY_DIR, f"{cname}.json")); st.rerun()

        if "current_chat" in st.session_state:
            st.title(f"🎓 {st.session_state.current_chat}")
            msgs = all_chats.get(st.session_state.current_chat, {}).get("messages", [])
            for m in msgs:
                with st.chat_message(m["role"]): st.markdown(m["content"])
            if prompt := st.chat_input(L['input']):
                # ... tu by bola tvoja Gemini logika ...
                st.write("AI odpovedá...")

# ==========================================
# SEKCIA 2: FÓRUM (Index 1)
# ==========================================
with tabs[1]:
    if current_tab_index == 1:
        st.title(f"{L['forum']}")
        # ... tvoja logika fóra ...
        st.info("Tu sú tvoje študijné materiály.")

# ==========================================
# SEKCIA 3: SKUPINY (Index 2)
# ==========================================
with tabs[2]:
    if current_tab_index == 2:
        st.title(L["groups"])
        st.warning(L["groups_msg"])
