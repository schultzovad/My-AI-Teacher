import streamlit as st
import google.generativeai as genai
import json
import os
import re
import unicodedata

# 1. SETUP & MULTILINGUAL DICTIONARY
st.set_page_config(page_title="AI Tutor Pro", layout="wide", page_icon="🎓")

# Definícia textov pre rozhranie
LANG_MAP = {
    "EN": {
        "title": "Conversations", "new_chat": "➕ New Chat", "rename": "Rename chat:", 
        "upload": "Attach notes", "explain": "✨ Explain my files", "input": "Ask your teacher...",
        "status_think": "Teacher is preparing the answer...", "status_ready": "Answer ready!",
        "limit_msg": "😊 **My AI brain needs a rest.** We've covered a lot today and reached the daily limit. See you tomorrow?",
        "safety_msg": "⚠️ **I cannot talk about this topic.** My safety rules don't allow it. Try another question!",
        "error_msg": "🔌 **I have a small technical hiccup.** Please try sending the message again.",
        "rename_btn": "Rename"
    },
    "SK": {
        "title": "Konverzácie", "new_chat": "➕ Nový čet", "rename": "Premenovať čet:", 
        "upload": "Nahrať poznámky", "explain": "✨ Vysvetli moje súbory", "input": "Opýtaj sa učiteľa...",
        "status_think": "Učiteľ pripravuje odpoveď...", "status_ready": "Odpoveď je hotová!",
        "limit_msg": "😊 **Môj AI mozog si potrebuje oddýchnuť.** Dnes sme už prebrali veľa učiva a dosiahli sme limit. Stretneme sa zajtra?",
        "safety_msg": "⚠️ **O tejto téme nemôžem hovoriť.** Moje pravidlá mi to nedovoľujú. Skús inú otázku!",
        "error_msg": "🔌 **Mám malý technický problém.** Skús poslať správu znova.",
        "rename_btn": "Premenovať"
    },
    "FR": {
        "title": "Conversations", "new_chat": "➕ Nouveau chat", "rename": "Renommer le chat :", 
        "upload": "Joindre des notes", "explain": "✨ Expliquer mes fichiers", "input": "Posez une question...",
        "status_think": "Le professeur prépare la réponse...", "status_ready": "Réponse prête !",
        "limit_msg": "😊 **Mon cerveau IA a besoin de repos.** Nous avons beaucoup appris aujourd'hui. On se voit demain ?",
        "safety_msg": "⚠️ **Je ne peux pas parler de ce sujet.** Mes règles de sécurité ne le permettent pas.",
        "error_msg": "🔌 **J'ai un petit problème technique.** Veuillez renvoyer le message.",
        "rename_btn": "Renommer"
    },
    "PL": {
        "title": "Rozmowy", "new_chat": "➕ Nowy czat", "rename": "Zmień nazwę:", 
        "upload": "Załącz notatki", "explain": "✨ Wyjaśnij moje pliki", "input": "Zapytaj nauczyciela...",
        "status_think": "Nauczyciel przygotowuje odpowiedź...", "status_ready": "Odpowiedź gotowa!",
        "limit_msg": "😊 **Mój mózg AI potrzebuje odpoczynku.** Dzisiaj dużo się nauczyliśmy. Do zobaczenia jutro?",
        "safety_msg": "⚠️ **Nie mogę rozmawiać na ten temat.** Moje zasady bezpieczeństwa na to nie pozwalają.",
        "error_msg": "🔌 **Mam mały problem techniczny.** Spróbuj wysłać wiadomość ponownie.",
        "rename_btn": "Zmień nazwę"
    }
}

if "lang" not in st.session_state:
    st.session_state.lang = "SK"

L = LANG_MAP[st.session_state.lang]

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")

HISTORY_DIR = "chat_history"
if not os.path.exists(HISTORY_DIR): os.makedirs(HISTORY_DIR)

# --- FUNKCIE (save, load, slugify ostávajú rovnaké) ---
def save_chat(chat_name, messages):
    with open(os.path.join(HISTORY_DIR, f"{chat_name}.json"), "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

def load_all_chats():
    chats = {}
    if not os.path.exists(HISTORY_DIR): return chats
    for file in [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]:
        name = file.replace(".json", "")
        with open(os.path.join(HISTORY_DIR, file), "r", encoding="utf-8") as f:
            chats[name] = json.load(f)
    return chats

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^\w\s-]', '', text).strip()[:25]

# INICIALIZÁCIA
if "chats" not in st.session_state:
    st.session_state.chats = load_all_chats() or {"New Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# 2. SIDEBAR
with st.sidebar:
    st.session_state.lang = st.selectbox("🌐 Language / Jazyk", options=["SK", "EN", "FR", "PL"], index=["SK", "EN", "FR", "PL"].index(st.session_state.lang))
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
            if st.button(f"💬 {chat_name}", key=f"b_{chat_name}", use_container_width=True, type="primary" if chat_name == st.session_state.current_chat else "secondary"):
                st.session_state.current_chat = chat_name
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"d_{chat_name}"):
                os.remove(os.path.join(HISTORY_DIR, f"{chat_name}.json"))
                del st.session_state.chats[chat_name]
                st.session_state.current_chat = list(st.session_state.chats.keys())[0] if st.session_state.chats else "New Chat"
                st.rerun()

    st.write("---")
    man_name = st.text_input(L['rename'], placeholder="...")
    if st.button(L['rename_btn']):
        if man_name:
            new_n = slugify(man_name)
            os.rename(os.path.join(HISTORY_DIR, f"{st.session_state.current_chat}.json"), os.path.join(HISTORY_DIR, f"{new_n}.json"))
            st.session_state.chats[new_n] = st.session_state.chats.pop(st.session_state.current_chat)
            st.session_state.current_chat = new_n
            st.rerun()

# 3. MAIN UI
st.title(f"🎓 {st.session_state.current_chat}")
messages = st.session_state.chats.get(st.session_state.current_chat, [])
for m in messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# 4. INPUT
st.write("---")
up_files = st.file_uploader(L['upload'], accept_multiple_files=True, label_visibility="collapsed")
if input_t := st.chat_input(L['input']):
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": input_t})
    save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
    st.rerun()

# 5. GENERATE
if messages and messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.status(L['status_think'], expanded=True) as status:
            is_new = st.session_state.current_chat.startswith("Chat_") or st.session_state.current_chat == "New Chat"
            system_msg = f"You are a kind teacher. Respond in the language used by the user. Current UI language is {st.session_state.lang}."
            if is_new and len(messages) <= 2:
                system_msg += " Start with [TITLE: 2_word_title] then your explanation."

            try:
                model = genai.GenerativeModel('gemini-flash-latest')
                res = model.generate_content([system_msg] + [f"{m['role']}: {m['content']}" for m in messages[-5:]]).text
                
                final_res = res
                if "[TITLE:" in res:
                    parts = res.split("]", 1)
                    final_res = parts[1].strip()
                    new_t = slugify(parts[0].replace("[TITLE:", "").strip())
                    old_c = st.session_state.current_chat
                    os.rename(os.path.join(HISTORY_DIR, f"{old_c}.json"), os.path.join(HISTORY_DIR, f"{new_t}.json"))
                    st.session_state.chats[new_t] = st.session_state.chats.pop(old_c)
                    st.session_state.current_chat = new_t

                status.update(label=L['status_ready'], state="complete", expanded=False)
                st.markdown(final_res)
                st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": final_res})
                save_chat(st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
                st.rerun()

            except Exception as e:
                if "429" in str(e):
                    status.update(label="Limit!", state="error")
                    st.warning(L['limit_msg'])
                else:
                    status.update(label="Error!", state="error")
                    st.error(L['error_msg'])
                st.stop()
