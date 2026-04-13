import streamlit as st
import google.generativeai as genai
import json
import os
import re
import unicodedata
from datetime import datetime

# 1. ZÁKLADNÉ NASTAVENIE
st.set_page_config(page_title="EduHub Pro", layout="wide", page_icon="🎓", initial_sidebar_state="expanded")

HISTORY_DIR = "chat_history"
FORUM_DIR = "shared_forum"
for d in [HISTORY_DIR, FORUM_DIR]:
    if not os.path.exists(d): os.makedirs(d)

SUBJECTS = ["Angličtina", "Matematika", "Dejepis", "Biológia", "Slovenčina", "Iné"]

# API kľúč
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. KOMPLETNÝ PREKLADOVÝ SLOVNÍK (všetky opravy zahrnuté)
LANG_MAP = {
    "SK": {"chat": "💬 AI Tutor", "forum": "🏫 Fórum", "groups": "👥 Skupiny", "new_chat": "➕ Nový čet", "search": "Hľadaj v histórii...", "upload": "📤 Nahrať", "subject": "Predmet", "files": "Súbory", "input": "Opýtaj sa AI...", "status_think": "Premýšľam...", "status_ready": "Hotovo!", "error": "Chyba", "download": "📥 Stiahnuť", "no_files": "V tomto predmete zatiaľ nie sú žiadne súbory.", "learn_with_ai": "🤖 Uč sa s AI"},
    "EN": {"chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Groups", "new_chat": "➕ New Chat", "search": "Search in history...", "upload": "📤 Upload", "subject": "Subject", "files": "Files", "input": "Ask AI...", "status_think": "Thinking...", "status_ready": "Ready!", "error": "Error", "download": "📥 Download", "no_files": "There are no files in this subject yet.", "learn_with_ai": "🤖 Learn with AI"},
    "CZ": {"chat": "💬 AI Tutor", "forum": "🏫 Fórum", "groups": "👥 Skupiny", "new_chat": "➕ Nový chat", "search": "Hledat v historii...", "upload": "📤 Nahrát", "subject": "Předmět", "files": "Soubory", "input": "Zeptej se AI...", "status_think": "Přemýšlím...", "status_ready": "Hotovo!", "error": "Chyba", "download": "📥 Stáhnout", "no_files": "V tomto předmětu zatím nejsou žádné soubory.", "learn_with_ai": "🤖 Uč se s AI"},
    "FR": {"chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Groupes", "new_chat": "➕ Nouveau chat", "search": "Chercher dans l'histoire...", "upload": "📤 Charger", "subject": "Sujet", "files": "Fichiers", "input": "Demander à l'AI...", "status_think": "Réflexion...", "status_ready": "Prêt !", "error": "Erreur", "download": "📥 Télécharger", "no_files": "Il n'y a pas encore de fichiers dans ce sujet.", "learn_with_ai": "🤖 Apprendre s avec l'AI"},
    "DE": {"chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Gruppen", "new_chat": "➕ Neuer Chat", "search": "In der Historie suchen...", "upload": "📤 Hochladen", "subject": "Fach", "files": "Dateien", "input": "Frag die KI...", "status_think": "Überlegen...", "status_ready": "Fertig!", "error": "Fehler", "download": "📥 Herunterladen", "no_files": "In diesem Fach gibt es noch keine Dateien.", "learn_with_ai": "🤖 Mit KI lernen"},
    "ES": {"chat": "💬 AI Tutor", "forum": "🏫 Foro", "groups": "👥 Grupos", "new_chat": "➕ Nuevo chat", "search": "Buscar en el historial...", "upload": "📤 Subir", "subject": "Materia", "files": "Archivos", "input": "Pregunta a la IA...", "status_think": "Pensando...", "status_ready": "¡Listo!", "error": "Error", "download": "📥 Descargar", "no_files": "Aún no hay archivos en esta materia.", "learn_with_ai": "🤖 Aprende con IA"},
    "IT": {"chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Gruppi", "new_chat": "➕ Nuova chat", "search": "Cerca nella cronologia...", "upload": "📤 Carica", "subject": "Materia", "files": "File", "input": "Chiedi all'IA...", "status_think": "Pensando...", "status_ready": "Pronto!", "error": "Errore", "download": "📥 Scarica", "no_files": "Non ci sono ancora file in questa materia.", "learn_with_ai": "🤖 Impara con l'IA"},
    "PL": {"chat": "💬 AI Tutor", "forum": "🏫 Forum", "groups": "👥 Grupy", "new_chat": "➕ Nowy czat", "search": "Szukaj w historii...", "upload": "📤 Prześlij", "subject": "Przedmiot", "files": "Pliki", "input": "Zapytaj AI...", "status_think": "Myślenie...", "status_ready": "Gotowe!", "error": "Błąd", "download": "📥 Pobierz", "no_files": "W tym przedmiocie nie ma jeszcze żadnych plików.", "learn_with_ai": "🤖 Ucz się z AI"},
    "UA": {"chat": "💬 AI Tutor", "forum": "🏫 Форум", "groups": "👥 Групи", "new_chat": "➕ Новий чат", "search": "Пошук в історії...", "upload": "📤 Завантажити", "subject": "Предмет", "files": "Файли", "input": "Запитати AI...", "status_think": "Думаю...", "status_ready": "Готово!", "error": "Помилка", "download": "📥 Завантажити", "no_files": "У цій темі ще немає файлів.", "learn_with_ai": "🤖 Навчайся з AI"}
}

if "lang" not in st.session_state: st.session_state.lang = "SK"
L = LANG_MAP[st.session_state.lang]

# 3. POMOCNÉ FUNKCIE
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

# --- LOGIKA PREPÍNANIA TABOV (BONUS) ---
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0 # Default je AI Tutor

# --- DYNAMICKÁ NAVIGÁCIA ---
tab_titles = [L["chat"], L["forum"], L["groups"]]
tabs = st.tabs(tab_titles)

# ==========================================
# SEKCIA 1: AI TUTOR
# ==========================================
with tabs[0]:
    with st.sidebar:
        st.selectbox("🌐 Language", options=list(LANG_MAP.keys()), key="lang")
        L = LANG_MAP[st.session_state.lang]
        st.title(f"📂 {L['chat']}")
        
        if st.button(L['new_chat'], use_container_width=True, type="primary"):
            nid = f"Chat_{len(load_all_chats())+1}"
            save_chat(nid, [])
            st.session_state.current_chat = nid
            st.rerun()
        
        search_term = st.text_input("Search", placeholder=L['search'], label_visibility="collapsed")
        st.write("---")
        
        all_chats = load_all_chats()
        for cname in list(all_chats.keys()):
            if search_term.lower() in cname.lower():
                col_btn, col_del = st.columns([0.8, 0.2])
                with col_btn:
                    dt = all_chats[cname].get("updated", "")
                    label = f"💬 {cname}\n{dt}" if dt else f"💬 {cname}"
                    if st.button(label, key=f"b_{cname}", use_container_width=True, type="primary" if cname == st.session_state.get("current_chat") else "secondary"):
                        st.session_state.current_chat = cname
                        st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"del_{cname}"):
                        try: os.remove(os.path.join(HISTORY_DIR, f"{cname}.json"))
                        except: pass
                        st.rerun()

    if "current_chat" not in st.session_state and all_chats:
        st.session_state.current_chat = list(all_chats.keys())[0]
    
    if "current_chat" in st.session_state:
        st.title(f"🎓 {st.session_state.current_chat}")
        curr_chat_data = all_chats.get(st.session_state.current_chat, {"messages": []})
        msgs = curr_chat_data.get("messages", [])

        # Súbory pre AI
        st.write("---")
        ai_files = st.file_uploader(L['upload'], type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True, key="ai_up")

        # BONUS LOGIKA: Automatická správa ak prichádzame z fóra
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
                    sys_msg = f"Act as a tutor. Reply in the same language as user. UI is in {st.session_state.lang}."
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
                        status.update(label=L['error'], state="error")
                        st.error(str(e)); st.stop()

# ==========================================
# SEKCIA 2: VEREJNÉ FÓRUM
# ==========================================
with tabs[1]:
    st.title(f"{L['forum']}")
    sel_sub = st.selectbox(L["subject"], SUBJECTS, key="forum_sub")
    
    f_col1, f_col2 = st.columns([0.6, 0.4])
    
    with f_col1:
        st.subheader(f"{L['files']}: {sel_sub}")
        all_f = os.listdir(FORUM_DIR)
        sub_f = [f for f in all_f if f.startswith(sel_sub)]
        
        if not sub_f: 
            st.info(L["no_files"]) # OPRAVA: Teraz je to v správnom jazyku
        else:
            for f in sub_f:
                c1, c2, c3 = st.columns([0.5, 0.2, 0.3])
                clean = f.replace(f"{sel_sub}_", "")
                with c1: st.write(f"📄 {clean}")
                with c2:
                    with open(os.path.join(FORUM_DIR, f), "rb") as fd:
                        st.download_button("💾", data=fd, file_name=clean, key=f"dl_{f}")
                with c3:
                    # --- BONUSOVÉ TLAČIDLO "UČ SA S AI" ---
                    if st.button(L["learn_with_ai"], key=f"ai_learn_{f}"):
                        # Pripravíme inštrukciu pre AI
                        st.session_state.auto_prompt = f"Ahoj! Našiel som na fóre tento materiál: '{clean}'. Mohol by si mi ho stručne vysvetliť a pomôcť mi sa ho naučiť?"
                        # Vytvoríme nový čet pre túto tému
                        nid = f"Study_{slugify(clean)}"
                        save_chat(nid, [])
                        st.session_state.current_chat = nid
                        # Prepnutie na tab 0 (AI Tutor) sa v Streamlite po rerune udeje vďaka logike zobrazenia
                        st.rerun()

    with f_col2:
        st.subheader(L["upload"])
        fn = st.text_input("Názov / Title", key="fn_in")
        fu = st.file_uploader("PDF/IMG", type=["pdf", "jpg", "png"], key="fu_in")
        if st.button(L["upload"], use_container_width=True):
            if fu and fn:
                with open(os.path.join(FORUM_DIR, f"{sel_sub}_{slugify(fn)}_{fu.name}"), "wb") as f:
                    f.write(fu.getbuffer())
                st.success("OK!"); st.rerun()

# ==========================================
# SEKCIA 3: MOJE SKUPINY
# ==========================================
with tabs[2]:
    st.title(L["groups"])
    st.info("Locked. Need Login System.")
