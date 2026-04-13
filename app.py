import streamlit as st
import google.generativeai as genai
import json
import os
import re
import unicodedata

# 1. ZÁKLADNÉ NASTAVENIE
st.set_page_config(page_title="EduHub Pro", layout="wide", page_icon="🎓", initial_sidebar_state="expanded")

HISTORY_DIR = "chat_history"
FORUM_DIR = "shared_forum"
for d in [HISTORY_DIR, FORUM_DIR]:
    if not os.path.exists(d): os.makedirs(d)

# API kľúč
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. KOMPLETNÝ PREKLADOVÝ SLOVNÍK
LANG_MAP = {
    "SK": {
        "chat": "💬 AI Tutor", "forum": "🏫 Fórum", "groups": "👥 Skupiny", 
        "new_chat": "➕ Nový čet", "search": "Hľadaj v histórii...", "upload_label": "Nahraj súbor (PDF, JPG, PNG)", 
        "subject": "Predmet", "files": "Súbory", "input": "Opýtaj sa AI...", 
        "status_think": "Premýšľam...", "status_ready": "Hotovo!", "error": "Chyba", 
        "download": "📥 Stiahnuť", "no_files": "V tomto predmete zatiaľ nie sú žiadne súbory.", 
        "learn_with_ai": "🤖 Uč sa s AI", "mat_title": "Názov materiálu", "upload_btn": "Uverejniť na fórum",
        "groups_msg": "Sekcia je uzamknutá. Vyžaduje sa prihlasovací systém.", "lang_label": "🌐 Jazyk",
        "subjects": ["Angličtina", "Matematika", "Dejepis", "Biológia", "Slovenčina", "Iné"]
    },
    "EN": {
        "chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Groups", 
        "new_chat": "➕ New Chat", "search": "Search in history...", "upload_label": "Upload file (PDF, JPG, PNG)", 
        "subject": "Subject", "files": "Files", "input": "Ask AI...", 
        "status_think": "Thinking...", "status_ready": "Ready!", "error": "Error", 
        "download": "📥 Download", "no_files": "There are no files in this subject yet.", 
        "learn_with_ai": "🤖 Learn with AI", "mat_title": "Material Title", "upload_btn": "Publish to Forum",
        "groups_msg": "Section locked. Login system required.", "lang_label": "🌐 Language",
        "subjects": ["English", "Mathematics", "History", "Biology", "Other"]
    },
    "CZ": {
        "chat": "💬 AI Tutor", "forum": "🏫 Fórum", "groups": "👥 Skupiny", 
        "new_chat": "➕ Nový chat", "search": "Hledat v historii...", "upload_label": "Nahraj soubor (PDF, JPG, PNG)", 
        "subject": "Předmět", "files": "Soubory", "input": "Zeptej se AI...", 
        "status_think": "Přemýšlím...", "status_ready": "Hotovo!", "error": "Chyba", 
        "download": "📥 Stáhnout", "no_files": "V tomto předmětu zatím nejsou žádné soubory.", 
        "learn_with_ai": "🤖 Uč se s AI", "mat_title": "Název materiálu", "upload_btn": "Uveřejnit na fórum",
        "groups_msg": "Sekce je uzamčena. Je vyžadován přihlašovací systém.", "lang_label": "🌐 Jazyk",
        "subjects": ["Angličtina", "Matematika", "Dějepis", "Biologie", "Čeština", "Jiné"]
    },
    "FR": {
        "chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Groupes", 
        "new_chat": "➕ Nouveau chat", "search": "Chercher dans l'histoire...", "upload_label": "Charger un fichier (PDF, JPG, PNG)", 
        "subject": "Sujet", "files": "Fichiers", "input": "Demander à l'AI...", 
        "status_think": "Réflexion...", "status_ready": "Prêt !", "error": "Erreur", 
        "download": "📥 Télécharger", "no_files": "Aucun fichier dans ce sujet.", 
        "learn_with_ai": "🤖 Apprendre avec l'AI", "mat_title": "Titre du matériel", "upload_btn": "Publier sur le forum",
        "groups_msg": "Section verrouillée. Système de connexion requis.", "lang_label": "🌐 Langue",
        "subjects": ["Anglais", "Mathématiques", "Histoire", "Biologie", "Français", "Autre"]
    },
    "DE": {
        "chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Gruppen", 
        "new_chat": "➕ Neuer Chat", "search": "In der Historie suchen...", "upload_label": "Datei hochladen (PDF, JPG, PNG)", 
        "subject": "Fach", "files": "Dateien", "input": "Frag die KI...", 
        "status_think": "Überlegen...", "status_ready": "Fertig!", "error": "Fehler", 
        "download": "📥 Herunterladen", "no_files": "Keine Dateien vorhanden.", 
        "learn_with_ai": "🤖 Mit KI lernen", "mat_title": "Materialtitel", "upload_btn": "Im Forum veröffentlichen",
        "groups_msg": "Bereich gesperrt. Login-System erforderlich.", "lang_label": "🌐 Sprache",
        "subjects": ["Englisch", "Mathematik", "Geschichte", "Biologie", "Deutsch", "Anderes"]
    },
    "ES": {
        "chat": "💬 AI Tutor", "forum": "🏫 Foro", "groups": "👥 Grupos", 
        "new_chat": "➕ Nuevo chat", "search": "Buscar en el historial...", "upload_label": "Subir archivo (PDF, JPG, PNG)", 
        "subject": "Materia", "files": "Archivos", "input": "Pregunta a la IA...", 
        "status_think": "Pensando...", "status_ready": "¡Listo!", "error": "Error", 
        "download": "📥 Descargar", "no_files": "No hay archivos aquí.", 
        "learn_with_ai": "🤖 Aprende con IA", "mat_title": "Título del material", "upload_btn": "Publicar en el foro",
        "groups_msg": "Sección bloqueada. Sistema de inicio de sesión requerido.", "lang_label": "🌐 Idioma",
        "subjects": ["Inglés", "Matemáticas", "Historia", "Biología", "Español", "Otro"]
    },
    "IT": {
        "chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Gruppi", 
        "new_chat": "➕ Nuova chat", "search": "Cerca nella cronologia...", "upload_label": "Carica file (PDF, JPG, PNG)", 
        "subject": "Materia", "files": "File", "input": "Chiedi all'IA...", 
        "status_think": "Pensando...", "status_ready": "Pronto!", "error": "Errore", 
        "download": "📥 Scarica", "no_files": "Nessun file presente.", 
        "learn_with_ai": "🤖 Impara con l'IA", "mat_title": "Titolo del materiale", "upload_btn": "Pubblica sul forum",
        "groups_msg": "Sezione bloccata. Sistema di login richiesto.", "lang_label": "🌐 Lingua",
        "subjects": ["Inglese", "Matematica", "Storia", "Biologia", "Italiano", "Altro"]
    },
    "PL": {
        "chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Grupy", 
        "new_chat": "➕ Nowy czat", "search": "Szukaj w historii...", "upload_label": "Prześlij plik (PDF, JPG, PNG)", 
        "subject": "Przedmiot", "files": "Pliki", "input": "Zapytaj AI...", 
        "status_think": "Myślenie...", "status_ready": "Gotowe!", "error": "Błąd", 
        "download": "📥 Pobierz", "no_files": "Brak plików.", 
        "learn_with_ai": "🤖 Ucz się z AI", "mat_title": "Tytuł materiału", "upload_btn": "Opublikuj na forum",
        "groups_msg": "Sekcja zablokowana. Wymagany system logowania.", "lang_label": "🌐 Język",
        "subjects": ["Angielski", "Matematyka", "Historia", "Biologia", "Polski", "Inne"]
    },
    "UA": {
        "chat": "💬 AI Tutor", "forum": "🏫 Форум", "groups": "👥 Групи", 
        "new_chat": "➕ Новий чат", "search": "Пошук в історії...", "upload_label": "Завантажити файл (PDF, JPG, PNG)", 
        "subject": "Предмет", "files": "Файли", "input": "Запитати AI...", 
        "status_think": "Думаю...", "status_ready": "Готово!", "error": "Помилка", 
        "download": "📥 Завантажити", "no_files": "Файлів немає.", 
        "learn_with_ai": "🤖 Навчайся з AI", "mat_title": "Назва матеріалу", "upload_btn": "Опублікувати на форумі",
        "groups_msg": "Розділ заблоковано. Потрібна система входу.", "lang_label": "🌐 Мова",
        "subjects": ["Англійська", "Математика", "Історія", "Біологія", "Українська", "Інше"]
    }
}

if "lang" not in st.session_state: st.session_state.lang = "SK"
L = LANG_MAP[st.session_state.lang]

# 3. POMOCNÉ FUNKCIE (Bez času)
def save_chat(name, msgs):
    data = {"messages": msgs} # Ukladáme len správy
    with open(os.path.join(HISTORY_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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

# --- UI NAVIGÁCIA ---
tabs = st.tabs([L["chat"], L["forum"], L["groups"]])

# ==========================================
# SEKCIA 1: AI TUTOR
# ==========================================
with tabs[0]:
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
                    # ZOBRAZENIE: Už len čistý názov bez dátumu
                    label = f"💬 {cname}"
                    if st.button(label, key=f"b_{cname}", use_container_width=True, type="primary" if cname == st.session_state.get("current_chat") else "secondary"):
                        st.session_state.current_chat = cname; st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"del_{cname}"):
                        try: os.remove(os.path.join(HISTORY_DIR, f"{cname}.json"))
                        except: pass
                        st.rerun()

    if "current_chat" in st.session_state:
        st.title(f"🎓 {st.session_state.current_chat}")
        curr_chat_data = all_chats.get(st.session_state.current_chat, {"messages": []})
        msgs = curr_chat_data.get("messages", [])

        st.write("---")
        ai_files = st.file_uploader(L['upload_label'], type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True, key="ai_up")

        if "auto_prompt" in st.session_state:
            prompt_text = st.session_state.pop("auto_prompt")
            msgs.append({"role": "user", "content": prompt_text})
            save_chat(st.session_state.current_chat, msgs)

        for m in msgs:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input(L['input']):
            msgs.append({"role": "user", "content": prompt})
            save_chat(st.session_state.current_chat, msgs)
            
            with st.chat_message("assistant"):
                with st.status(L['status_think'], expanded=True) as status:
                    is_new = st.session_state.current_chat.startswith("Chat_") or st.session_state.current_chat == "New Chat"
                    sys_msg = f"Tutor mode. Language: {st.session_state.lang}."
                    if is_new and len(msgs) <= 2: sys_msg += " START WITH [TITLE: 2_word_title] THEN reply."
                    
                    payload = [sys_msg] + [f"{m['role']}: {m['content']}" for m in msgs[-10:]]
                    if ai_files:
                        for f in ai_files: payload.append({'mime_type': f.type, 'data': f.getvalue()})

                    try:
                        res = genai.GenerativeModel('gemini-flash-latest').generate_content(payload).text
                        final = res
                        if "[TITLE:" in res:
                            parts = res.split("]", 1)
                            final = parts[1].strip()
                            new_t = slugify(parts[0].replace("[TITLE:", "").strip())
                            if new_t and new_t != st.session_state.current_chat:
                                old_p = os.path.join(HISTORY_DIR, f"{st.session_state.current_chat}.json")
                                new_p = os.path.join(HISTORY_DIR, f"{new_t}.json"); os.rename(old_p, new_p)
                                st.session_state.current_chat = new_t

                        status.update(label=L['status_ready'], state="complete", expanded=False)
                        st.markdown(final)
                        msgs.append({"role": "assistant", "content": final})
                        save_chat(st.session_state.current_chat, msgs)
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

# ==========================================
# SEKCIA 2: FÓRUM
# ==========================================
with tabs[1]:
    st.title(f"{L['forum']}")
    sel_sub = st.selectbox(L["subject"], L["subjects"], key="forum_sub")
    
    f_col1, f_col2 = st.columns([0.6, 0.4])
    
    with f_col1:
        st.subheader(f"{L['files']}: {sel_sub}")
        all_f = os.listdir(FORUM_DIR)
        sub_f = [f for f in all_f if f.startswith(sel_sub)]
        
        if not sub_f: st.info(L["no_files"])
        else:
            for f in sub_f:
                c1, c2, c3 = st.columns([0.5, 0.2, 0.3])
                clean = f.split("_", 2)[-1]
                with c1: st.write(f"📄 {clean}")
                with c2:
                    with open(os.path.join(FORUM_DIR, f), "rb") as fd:
                        st.download_button("💾", data=fd, file_name=clean, key=f"dl_{f}")
                with c3:
                    if st.button(L["learn_with_ai"], key=f"ai_learn_{f}"):
                        st.session_state.auto_prompt = f"Help me learn this: '{clean}'"
                        nid = f"Study_{slugify(clean)}"
                        save_chat(nid, []); st.session_state.current_chat = nid; st.rerun()

    with f_col2:
        st.subheader(L["upload_btn"]) 
        fn = st.text_input(L["mat_title"], key="fn_in")
        fu = st.file_uploader(L["upload_label"], type=["pdf", "jpg", "png"], key="fu_in")
        if st.button(L["upload_btn"], use_container_width=True):
            if fu and fn:
                with open(os.path.join(FORUM_DIR, f"{sel_sub}_{slugify(fn)}_{fu.name}"), "wb") as f:
                    f.write(fu.getbuffer())
                st.success("OK!"); st.rerun()

# ==========================================
# SEKCIA 3: SKUPINY
# ==========================================
with tabs[2]:
    st.title(L["groups"])
    st.info(L["groups_msg"])
