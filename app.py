import streamlit as st
import google.generativeai as genai
import json
import os
import re
import unicodedata

# 1. SETUP & MULTILINGUAL DICTIONARY (Top 12 Languages)
st.set_page_config(page_title="AI Tutor Pro", layout="wide", page_icon="🎓")

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
    "PT": {"title": "Conversas", "new_chat": "➕ Novo chat", "rename": "Renomear:", "upload": "Notas", "explain": "✨ Explicar", "input": "Pergunte...", "status_think": "Pensando...", "status_ready": "Pronto!", "limit_msg": "😊 **Descanso necessário.** Limite atingido. Até amanhã?", "safety_msg": "⚠️ **Não permitido.** Minhas regras não deixam.", "error_msg": "🔌 **Erro.** Tente de novo.", "rename_btn": "Salvar"}
}

if "lang" not in st.session_state: st.session_state.lang = "SK"
L = LANG_MAP[st.session_state.lang]

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")

HISTORY_DIR = "chat_history"
if not os.path.exists(HISTORY_DIR): os.makedirs(HISTORY_DIR)

# --- UTILS ---
def save_chat(name, msgs):
    with open(os.path.join(HISTORY_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(msgs, f, ensure_ascii=False, indent=4)

def load_all():
    chats = {}
    if not os.path.exists(HISTORY_DIR): return chats
    for f_name in [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]:
        try:
            with open(os.path.join(HISTORY_DIR, f_name), "r", encoding="utf-8") as f:
                chats[f_name.replace(".json", "")] = json.load(f)
        except: continue
    return chats

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^\w\s-]', '', text).strip()[:20]

# INIT
if "chats" not in st.session_state: st.session_state.chats = load_all() or {"New Chat": []}
if "current_chat" not in st.session_state or st.session_state.current_chat not in st.session_state.chats:
    st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# 2. SIDEBAR
with st.sidebar:
    st.session_state.lang = st.selectbox("🌐 Interface Language", options=list(LANG_MAP.keys()), index=list(LANG_MAP.keys()).index(st.session_state.lang))
    st.title(f"📂 {L['title']}")
    if st.button(L['new_chat'], use_container_width=True):
        n_id = f"Chat_{len(st.session_state.chats)+1}"
        st.session_state.chats[n_id] = []; st.session_state.current_chat = n_id; save_chat(n_id, []); st.rerun()
    st.write("---")
    for c_name in list(st.session_state.chats.keys()):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button(f"💬 {c_name}", key=f"b_{c_name}", use_container_width=True, type="primary" if c_name == st.session_state.current_chat else "secondary"):
                st.session_state.current_chat = c_name; st.rerun()
        with col2:
            if st.button("🗑️", key=f"d_{c_name}"):
                try: os.remove(os.path.join(HISTORY_DIR, f"{c_name}.json"))
                except: pass
                del st.session_state.chats[c_name]
                st.session_state.current_chat = list(st.session_state.chats.keys())[0] if st.session_state.chats else "New Chat"
                if "New Chat" not in st.session_state.chats: st.session_state.chats["New Chat"] = []
                st.rerun()
    st.write("---")
    m_name = st.text_input(L['rename'], placeholder="...")
    if st.button(L['rename_btn'], key="ren_btn"):
        if m_name:
            nn = slugify(m_name)
            os.rename(os.path.join(HISTORY_DIR, f"{st.session_state.current_chat}.json"), os.path.join(HISTORY_DIR, f"{nn}.json"))
            st.session_state.chats[nn] = st.session_state.chats.pop(st.session_state.current_chat)
            st.session_state.current_chat = nn; st.rerun()

# 3. MAIN UI
st.title(f"🎓 {st.session_state.current_chat}")
cur_msgs = st.session_state.chats.get(st.session_state.current_chat, [])
for m in cur_msgs:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# 4. INPUT
st.write("---")
files = st.file_uploader(L['upload'], accept_multiple_files=True, label_visibility="collapsed", key=f"f_{st.session_state.current_chat}")
if prompt := st.chat_input(L['input']):
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
    st.rerun()

# 5. LOGIC
if cur_msgs and cur_msgs[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.status(L['status_think'], expanded=True) as status:
            is_new = st.session_state.current_chat.startswith("Chat_") or st.session_state.current_chat == "New Chat"
            sys_p = f"You are a kind teacher. Respond in the user's language. UI is {st.session_state.lang}."
            if is_new and len(cur_msgs) <= 2: sys_p += " START WITH [TITLE: 2_word_title] THEN your explanation."
            
            payload = [sys_p] + [f"{m['role']}: {m['content']}" for m in cur_msgs[-5:]]
            if files:
                for f in files: payload.append({'mime_type': f.type, 'data': f.getvalue()})

            try:
                model = genai.GenerativeModel('gemini-flash-latest')
                res = model.generate_content(payload).text
                final = res
                if "[TITLE:" in res:
                    parts = res.split("]", 1)
                    final = parts[1].strip()
                    new_t = slugify(parts[0].replace("[TITLE:", "").strip())
                    old_c = st.session_state.current_chat
                    if new_t and new_t != old_c:
                        try:
                            os.rename(os.path.join(HISTORY_DIR, f"{old_c}.json"), os.path.join(HISTORY_DIR, f"{new_t}.json"))
                            st.session_state.chats[new_t] = st.session_state.chats.pop(old_c)
                            st.session_state.current_chat = new_t
                        except: pass
                status.update(label=L['status_ready'], state="complete", expanded=False)
                st.markdown(final)
                st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": final})
                save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
                st.rerun()
            except Exception as e:
                if "429" in str(e): status.update(label="Limit!", state="error"); st.warning(L['limit_msg'])
                elif "safety" in str(e).lower(): status.update(label="Safety", state="error"); st.info(L['safety_msg'])
                else: status.update(label="Error", state="error"); st.error(L['error_msg'])
                st.stop()
