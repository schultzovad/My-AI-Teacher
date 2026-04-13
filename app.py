import streamlit as st
import google.generativeai as genai
import json
import os
import re
import unicodedata
from datetime import datetime

# 1. SETUP
st.set_page_config(page_title="EduHub Pro", layout="wide", page_icon="🎓", initial_sidebar_state="expanded")

# Adresáre
HISTORY_DIR = "chat_history"
FORUM_DIR = "shared_forum"
for d in [HISTORY_DIR, FORUM_DIR]:
    if not os.path.exists(d): os.makedirs(d)

SUBJECTS = ["Angličtina", "Matematika", "Dejepis", "Biológia", "Slovenčina", "Iné"]

# 2. KOMPLETNÝ PREKLADOVÝ SLOVNÍK (Všetkých 9 jazykov)
LANG_MAP = {
    "SK": {"chat": "💬 AI Tutor", "forum": "🏫 Fórum", "groups": "👥 Skupiny", "new_chat": "➕ Nový čet", "search": "🔍 Hľadať...", "upload": "📤 Nahrať", "subject": "Predmet", "files": "Súbory", "input": "Opýtaj sa AI...", "status_think": "Premýšľam...", "download": "📥 Stiahnuť"},
    "EN": {"chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Groups", "new_chat": "➕ New Chat", "search": "🔍 Search...", "upload": "📤 Upload", "subject": "Subject", "files": "Files", "input": "Ask AI...", "status_think": "Thinking...", "download": "📥 Download"},
    "CZ": {"chat": "💬 AI Tutor", "forum": "🏫 Fórum", "groups": "👥 Skupiny", "new_chat": "➕ Nový chat", "search": "🔍 Hledat...", "upload": "📤 Nahrát", "subject": "Předmět", "files": "Soubory", "input": "Zeptej se AI...", "status_think": "Přemýšlím...", "download": "📥 Stáhnout"},
    "FR": {"chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Groupes", "new_chat": "➕ Nouveau chat", "search": "🔍 Chercher...", "upload": "📤 Charger", "subject": "Sujet", "files": "Fichiers", "input": "Demander à l'AI...", "status_think": "Réflexion...", "download": "📥 Télécharger"},
    "DE": {"chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Gruppen", "new_chat": "➕ Neuer Chat", "search": "🔍 Suchen...", "upload": "📤 Hochladen", "subject": "Fach", "files": "Dateien", "input": "Frag die KI...", "status_think": "Überlegen...", "download": "📥 Herunterladen"},
    "ES": {"chat": "💬 AI Tutor", "forum": "🏫 Foro", "groups": "👥 Grupos", "new_chat": "➕ Nuevo chat", "search": "🔍 Buscar...", "upload": "📤 Subir", "subject": "Materia", "files": "Archivos", "input": "Pregunta a la IA...", "status_think": "Pensando...", "download": "📥 Descargar"},
    "IT": {"chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Gruppi", "new_chat": "➕ Nuova chat", "search": "🔍 Cerca...", "upload": "📤 Carica", "subject": "Materia", "files": "File", "input": "Chiedi all'IA...", "status_think": "Pensando...", "download": "📥 Scarica"},
    "PL": {"chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Grupy", "new_chat": "➕ Nowy czat", "search": "🔍 Szukaj...", "upload": "📤 Prześlij", "subject": "Przedmiot", "files": "Pliki", "input": "Zapytaj AI...", "status_think": "Myślenie...", "download": "📥 Pobierz"},
    "UA": {"chat": "💬 AI Tutor", "forum": "🏫 Форум", "groups": "👥 Групи", "new_chat": "➕ Новий чат", "search": "🔍 Пошук...", "upload": "📤 Завантажити", "subject": "Предмет", "files": "Файли", "input": "Запитати AI...", "status_think": "Думаю...", "download": "📥 Завантажити"}
}

# Inicializácia jazyka
if "lang" not in st.session_state: st.session_state.lang = "SK"
L = LANG_MAP[st.session_state.lang]

# --- POMOCNÉ FUNKCIE ---
def save_chat(name, msgs):
    data = {"updated": datetime.now().strftime("%d.%m. %H:%M"), "messages": msgs}
    with open(os.path.join(HISTORY_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_all_chats():
    chats = {}
    if not os.path.exists(HISTORY_DIR): return chats
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

# Dáta
if "chats" not in st.session_state: st.session_state.chats = load_all_chats()
if not st.session_state.chats: st.session_state.chats = {"New Chat": {"updated": "", "messages": []}}
if "current_chat" not in st.session_state: st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# --- DYNAMICKÉ TABS ---
tab_chat, tab_forum, tab_groups = st.tabs([L["chat"], L["forum"], L["groups"]])

# ==========================================
# SEKCIA 1: AI TUTOR
# ==========================================
with tab_chat:
    with st.sidebar:
        st.selectbox("🌐 Language", options=list(LANG_MAP.keys()), key="lang")
        L = LANG_MAP[st.session_state.lang] # Okamžitá aktualizácia prekladov
        st.title(f"📂 {L['chat']}")
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

    st.title(f"🎓 {st.session_state.current_chat}")
    curr_data = st.session_state.chats.get(st.session_state.current_chat, {"messages": []})
    msgs = curr_data.get("messages", [])

    for m in msgs:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input(L['input']):
        msgs.append({"role": "user", "content": prompt})
        save_chat(st.session_state.current_chat, msgs)
        # Tu by išla tvoja AI logika (preskočené pre dĺžku)
        st.rerun()

# ==========================================
# SEKCIA 2: FÓRUM (S PREKLADOM)
# ==========================================
with tab_forum:
    st.title(f"{L['forum']}")
    
    selected_subject = st.selectbox(L["subject"], SUBJECTS, key="forum_sub")
    
    col1, col2 = st.columns([0.6, 0.4])
    
    with col1:
        st.subheader(f"{L['files']}: {selected_subject}")
        # Načítanie súborov z priečinka shared_forum
        all_files = os.listdir(FORUM_DIR)
        subject_files = [f for f in all_files if f.startswith(selected_subject)]
        
        if not subject_files:
            st.info("No files yet.")
        else:
            for f in subject_files:
                col_name, col_btn = st.columns([0.7, 0.3])
                # Vyčistíme názov súboru pre zobrazenie
                clean_name = f.replace(f"{selected_subject}_", "")
                with col_name:
                    st.write(f"📄 {clean_name}")
                with col_btn:
                    with open(os.path.join(FORUM_DIR, f), "rb") as file_data:
                        st.download_button(L["download"], data=file_data, file_name=clean_name, key=f"dl_{f}")

    with col2:
        st.subheader(L["upload"])
        f_name = st.text_input("Názov / Title")
        f_upload = st.file_uploader("PDF/IMG", type=["pdf", "jpg", "png"], key="f_up")
        
        if st.button(L["upload"], use_container_width=True):
            if f_upload and f_name:
                save_path = os.path.join(FORUM_DIR, f"{selected_subject}_{slugify(f_name)}_{f_upload.name}")
                with open(save_path, "wb") as f:
                    f.write(f_upload.getbuffer())
                st.success("OK!")
                st.rerun()

# ==========================================
# SEKCIA 3: SKUPINY
# ==========================================
with tab_groups:
    st.title(L["groups"])
    st.info("Coming soon...")
