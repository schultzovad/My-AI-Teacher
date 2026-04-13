import streamlit as st
import google.generativeai as genai
import json
import os
import re
import unicodedata

# 1. SETUP & MULTILINGUAL DICTIONARY
st.set_page_config(page_title="AI Tutor Pro", layout="wide", page_icon="🎓")

# Kompletný zoznam jazykov pre celú aplikáciu
LANG_MAP = {
    "SK": {"title": "Konverzácie", "new_chat": "➕ Nový čet", "rename": "Premenovať:", "upload": "Nahrať poznámky", "explain": "✨ Vysvetli súbory", "input": "Opýtaj sa...", "status_think": "Učiteľ premýšľa...", "status_ready": "Hotovo!", "limit_msg": "😊 **Môj AI mozog si potrebuje oddýchnuť.** Limit 20 správ bol dosiahnutý. Vidíme sa zajtra?", "safety_msg": "⚠️ **O tomto nemôžem hovoriť.** Pravidlá mi to nedovoľujú.", "error_msg": "🔌 **Technická chyba.** Skús to znova.", "rename_btn": "Uložiť"},
    "EN": {"title": "Conversations", "new_chat": "➕ New Chat", "rename": "Rename:", "upload": "Attach notes", "explain": "✨ Explain files", "input": "Ask anything...", "status_think": "Thinking...", "status_ready": "Ready!", "limit_msg": "😊 **My AI brain needs a rest.** Daily limit reached. See you tomorrow?", "safety_msg": "⚠️ **I cannot talk about this.** My rules don't allow it.", "error_msg": "🔌 **Technical hiccup.** Please try again.", "rename_btn": "Save"},
    "FR": {"title": "Conversations", "new_chat": "➕ Nouveau chat", "rename": "Renommer:", "upload": "Notes", "explain": "✨ Expliquer", "input": "Posez une question...", "status_think": "Réflexion...", "status_ready": "Prêt !", "limit_msg": "😊 **Mon cerveau a besoin de repos.** Limite atteinte. À demain ?", "safety_msg": "⚠️ **Sujet interdit.** Mes règles ne le permettent pas.", "error_msg": "🔌 **Erreur technique.** Réessayez.", "rename_btn": "Enregistrer"},
    "DE": {"title": "Konversationen", "new_chat": "➕ Neuer Chat", "rename": "Umbenennen:", "upload": "Notizen", "explain": "✨ Erklären", "input": "Frag etwas...", "status_think": "Überlegen...", "status_ready": "Fertig!", "limit_msg": "😊 **Pause nötig.** Limit erreicht. Bis morgen?", "safety_msg": "⚠️ **Nicht erlaubt.** Meine Regeln verbieten das.", "error_msg": "🔌 **Fehler.** Erneut versuchen.", "rename_btn": "Speichern"},
    "ES": {"title": "Conversaciones", "new_chat": "➕ Nuevo chat", "rename": "Renombrar:", "upload": "Notas", "explain": "✨ Explicar", "input": "Pregunta...", "status_think": "Pensando...", "status_ready": "¡Listo!", "limit_msg": "😊 **Descanso necesario.** Límite alcanzado. ¿Mañana?", "safety_msg": "⚠️ **No permitido.** Mis reglas no lo permiten.", "error_msg": "🔌 **Error.** Intenta de nuevo.", "rename_btn": "Guardar"},
    "IT": {"title": "Conversazioni", "new_chat": "➕ Nuova chat", "rename": "Rinomina:", "upload": "Note", "explain": "✨ Spiega", "input": "Chiedi...", "status_think": "Pensando...", "status_ready": "Pronto!", "limit_msg": "😊 **Pausa necessaria.** Limite raggiunto. A domani?", "safety_msg": "⚠️ **Vietato.** Le mie regole non lo consentono.", "error_msg": "🔌 **Errore.** Riprova.", "rename_btn": "Salva"},
    "PL": {"title": "Rozmowy", "new_chat": "➕ Nowy czat", "rename": "Zmień nazwę:", "upload": "Notatki", "explain": "✨ Wyjaśnij", "input": "Zapytaj...", "status_think": "Myślenie...", "status_ready": "Gotowe!", "limit_msg": "😊 **Odpoczynek.** Limit osiągnięty. Do jutra?", "safety_msg": "⚠️ **Nie wolno.** Moje zasady na to nie pozwalają.", "error_msg": "🔌 **Błąd.** Spróbuj ponownie.", "rename_btn": "Zapisz"},
    "UA": {"title": "Розмови", "new_chat": "➕ Новий чат", "rename": "Назва:", "upload": "Нотатки", "explain": "✨ Поясни", "input": "Запитай...", "status_think": "Думаю...", "status_ready": "Готово!", "limit_msg": "😊 **Треба відпочити.** Ліміт вичерпано. До завтра?", "safety_msg": "⚠️ **Недопустимо.** Мої правила забороняють це.", "error_msg": "🔌 **Помилка.** Спробуйте ще раз.", "rename_btn": "Зберегти"},
    "CZ": {"title": "Konverzace", "new_chat": "➕ Nový chat", "rename": "Přejmenovat:", "upload": "Poznámky", "explain": "✨ Vysvětli", "input": "Zeptej se...", "status_think": "Přemýšlím...", "status_ready": "Hotovo!", "limit_msg": "😊 **Potřebuji pauzu.** Limit vyčerpán. Uvidíme se zítra?", "safety_msg": "⚠️ **Zakázané téma.** Pravidla mi to nedovolují.", "error_msg": "🔌 **Chyba.** Zkus to znovu.", "rename_btn": "Uložit"},
    "HU": {"title": "Beszélgetések", "new_chat": "➕ Új chat", "rename": "Átnevezés:", "upload": "Jegyzetek", "explain": "✨ Magyarázat", "input": "Kérdezz...", "status_think": "Gondolkodom...", "status_ready": "Kész!", "limit_msg": "😊 **Pihenésre van szükségem.** Elérted a limitet. Holnap?", "safety_msg": "⚠️ **Tiltott téma.** A szabályaim nem engedik.", "error_msg": "🔌 **Hiba.** Próbáld újra.", "rename_btn": "Mentés"},
    "RU": {"title": "Разговоры", "new_chat": "➕ Новый чат", "rename": "Переименовать:", "upload": "Заметки", "explain": "✨ Объясни", "input": "Спроси...", "status_think": "Думаю...", "status_ready": "Готово!", "limit_msg": "😊 **Нужен отдых.** Лимит исчерпан. До завтра?", "safety_msg": "⚠️ **Запрещено.** Мои правила не позволяют.", "error_msg": "🔌 **Ошибка.** Попробуй снова.", "rename_btn": "Сохранить"},
    "PT": {"title": "Conversas", "new_chat": "➕ Novo chat", "rename": "Renomear:", "upload": "Notas", "explain": "✨ Explicar", "input": "Pergunte...", "status_think": "Pensando...", "status_ready": "Pronto!", "limit_msg": "😊 **Descanso necesario.** Limite atingido. Até amanhã?", "safety_msg": "⚠️ **Não permitido.** Minhas regras não deixam.", "error_msg": "🔌 **Erro.** Tente de novo.", "rename_btn": "Salvar"}
}

# Inicializácia jazyka
if "lang" not in st.session_state:
    st.session_state.lang = "SK"

# Skratka pre aktuálne vybrané texty
L = LANG_MAP[st.session_state.lang]

# API Key check
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key in Streamlit Secrets!")

# Directory for history
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
    # Odstránenie špeciálnych znakov pre bezpečnosť súborov
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    clean = re.sub(r'[^\w\s-]', '', text).strip()
    return clean[:20] if clean else "Chat"

# Načítanie dát pri štarte
if "chats" not in st.session_state:
    st.session_state.chats = load_all_chats()
    if not st.session_state.chats:
        st.session_state.chats = {"New Chat": []}

if "current_chat" not in st.session_state or st.session_state.current_chat not in st.session_state.chats:
    st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# --- 2. SIDEBAR ---
with st.sidebar:
    # Okamžitá zmena jazyka cez on_change
    st.selectbox(
        "🌐 Language / Jazyk", 
        options=list(LANG_MAP.keys()), 
        key="lang", 
        on_change=None # Streamlit automaticky aktualizuje session_state
    )
    
    # Znovu načítame L po možnej zmene jazyka
    L = LANG_MAP[st.session_state.lang]
    
    st.title(f"📂 {L['title']}")
    
    if st.button(L['new_chat'], use_container_width=True):
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
                try: os.remove(os.path.join(HISTORY_DIR, f"{chat_name}.json"))
                except: pass
                del st.session_state.chats[chat_name]
                st.session_state.current_chat = list(st.session_state.chats.keys())[0] if st.session_state.chats else "New Chat"
                if "New Chat" not in st.session_state.chats: st.session_state.chats["New Chat"] = []
                st.rerun()

    st.write("---")
    st.write(L['rename'])
    new_name_input = st.text_input("Rename Field", label_visibility="collapsed", placeholder="...", key="rename_input")
    if st.button(L['rename_btn'], use_container_width=True):
        if new_name_input:
            new_title = slugify(new_name_input)
            old_path = os.path.join(HISTORY_DIR, f"{st.session_state.current_chat}.json")
            new_path = os.path.join(HISTORY_DIR, f"{new_title}.json")
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
            st.session_state.chats[new_title] = st.session_state.chats.pop(st.session_state.current_chat)
            st.session_state.current_chat = new_title
            st.rerun()

# --- 3. MAIN INTERFACE ---
st.title(f"🎓 {st.session_state.current_chat}")

current_messages = st.session_state.chats.get(st.session_state.current_chat, [])
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.write("---")

# --- 4. INPUT & FILES ---
with st.container():
    uploaded_files = st.file_uploader(
        L['upload'], type=["jpg", "jpeg", "png", "pdf"], 
        accept_multiple_files=True, label_visibility="collapsed", key=f"up_{st.session_state.current_chat}"
    )
    
    analyze_clicked = False
    if uploaded_files:
        if st.button(L['explain']):
            analyze_clicked = True

if input_text := st.chat_input(L['input']):
    if st.session_state.current_chat not in st.session_state.chats:
        st.session_state.chats[st.session_state.current_chat] = []
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": input_text})
    save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
    st.rerun()
elif analyze_clicked:
    prompt = "Please explain these files like a teacher."
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
    st.rerun()

# --- 5. AI RESPONSE & ERROR HANDLING ---
if current_messages and current_messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.status(L['status_think'], expanded=True) as status:
            
            # Nastavenie pre automatické meno (iba ak je to nový čet)
            is_generic = st.session_state.current_chat.startswith("Chat_") or st.session_state.current_chat == "New Chat"
            needs_title = is_generic and len(current_messages) <= 2
            
            system_instruction = f"You are a kind teacher. Respond in the user's language. Current UI is {st.session_state.lang}."
            if needs_title:
                system_instruction += " IMPORTANT: Start with [TITLE: 2_word_title] then a newline, then your explanation."

            payload = [system_instruction]
            # Pridanie histórie správ
            for m in current_messages[-5:]:
                payload.append(f"{m['role']}: {m['content']}")
            # Pridanie súborov
            if uploaded_files:
                for f in uploaded_files:
                    payload.append({'mime_type': f.type, 'data': f.getvalue()})

            try:
                model = genai.GenerativeModel('gemini-flash-latest')
                response = model.generate_content(payload).text
                
                final_text = response
                # Ak AI navrhla názov, premenujeme súbor
                if "[TITLE:" in response:
                    try:
                        parts = response.split("]", 1)
                        suggested_title = parts[0].replace("[TITLE:", "").strip()
                        final_text = parts[1].strip()
                        
                        new_name = slugify(suggested_title)
                        old_name = st.session_state.current_chat
                        if new_name and new_name != old_name:
                            old_p = os.path.join(HISTORY_DIR, f"{old_name}.json")
                            new_p = os.path.join(HISTORY_DIR, f"{new_name}.json")
                            if os.path.exists(old_p):
                                os.rename(old_p, new_p)
                            st.session_state.chats[new_name] = st.session_state.chats.pop(old_name)
                            st.session_state.current_chat = new_name
                    except: pass

                status.update(label=L['status_ready'], state="complete", expanded=False)
                st.markdown(final_text)
                
                # Uložíme odpoveď
                if st.session_state.current_chat not in st.session_state.chats:
                    st.session_state.chats[st.session_state.current_chat] = []
                st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": final_text})
                save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
                st.rerun()

            except Exception as e:
                err_str = str(e)
                if "429" in err_str:
                    status.update(label="Limit reached", state="error")
                    st.warning(L['limit_msg'])
                elif "safety" in err_str.lower():
                    status.update(label="Safety", state="error")
                    st.info(L['safety_msg'])
                else:
                    status.update(label="Error", state="error")
                    st.error(L['error_msg'])
                st.stop()
