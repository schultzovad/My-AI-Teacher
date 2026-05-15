import streamlit as st
import google.generativeai as genai
import pypdf
import docx
from PIL import Image

# 1. NASTAVENIE API
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ API kľúč chýba v Secrets!")
    st.stop()

genai.configure(api_key=api_key)

# POUŽIJEME MODEL, KTORÝ TI FUNGUJE (podľa tvojho zoznamu)
# Ak by gemini-3.1-flash-lite nešiel, prepíš to na gemini-2.0-flash
MODEL_NAME = 'gemini-3.1-flash-lite'
model_ai = genai.GenerativeModel(MODEL_NAME)

# --- INICIALIZÁCIA ---
if "m" not in st.session_state: st.session_state.m = []
if "doc_content" not in st.session_state: st.session_state.doc_content = ""

# 2. JAZYKOVÁ LOGIKA
query_params = st.query_params
jazyk = query_params.get("lang", "SK").upper()

texty = {
    "SK": {"title": "🤖 AI Tutor", "selected": "Vybraný súbor:", "send_file": "Odoslať ⬆️", "input": "Napíš otázku...", "file_msg": "*(Súbor: {name})*", "sys_prompt": "Si akademický tutor. Odpovedaj VŽDY v jazyku, v ktorom ti píše používateľ (napr. slovensky), aj keď je rozhranie v inom jazyku."},
    "EN": {"title": "🤖 AI Tutor", "selected": "Selected file:", "send_file": "Send ⬆️", "input": "Ask a question...", "file_msg": "*(File: {name})*", "sys_prompt": "You are an academic tutor. Always answer in the language the user is writing in."},
    "DE": {"title": "🤖 KI-Tutor", "selected": "Ausgewählte Datei:", "send_file": "Senden ⬆️", "input": "Frage stellen...", "file_msg": "*(Datei: {name})*", "sys_prompt": "Antworten Sie immer in der Sprache, in der der Benutzer schreibt."},
    "IT": {"title": "🤖 Tutor IA", "selected": "File selezionato:", "send_file": "Invia ⬆️", "input": "Fai una domanda...", "file_msg": "*(File: {name})*", "sys_prompt": "Rispondi sempre nella lingua in cui scrive l'utente."},
    "ES": {"title": "🤖 Tutor IA", "selected": "Archivo seleccionado:", "send_file": "Enviar ⬆️", "input": "Preguntar...", "file_msg": "*(Archivo: {name})*", "sys_prompt": "Responde siempre en el idioma en que escribe el usuario."},
    "FR": {"title": "🤖 Tuteur IA", "selected": "Fichier sélectionné:", "send_file": "Envoyer ⬆️", "input": "Question...", "file_msg": "*(Fichier: {name})*", "sys_prompt": "Répondez TOUJOURS dans la langue utilisée par l'utilisateur. S'il écrit en slovaque, répondez en slovaque."},
    "UA": {"title": "🤖 AI Тьютор", "selected": "Вибраний файл:", "send_file": "Надіслати ⬆️", "input": "Запитати...", "file_msg": "*(Файл: {name})*", "sys_prompt": "Завжди відповідайте мовою користувача."},
    "RU": {"title": "🤖 AI Тьютор", "selected": "Выбранный файл:", "send_file": "Отправить ⬆️", "input": "Спросить...", "file_msg": "*(Файл: {name})*", "sys_prompt": "Всегда отвечайте на языке пользователя."}
}
T = texty.get(jazyk, texty["SK"])

# 3. DIZAJN + CSS (Tvoj pôvodný štýl)
st.set_page_config(page_title=T["title"], layout="wide")

st.markdown(f"""
    <style>
    header, footer {{visibility: hidden;}} 
    .stAppDeployButton {{display:none;}}
    
    div[data-testid="stFileUploader"] section {{
        display: flex; flex-direction: row; align-items: center; justify-content: center;
        padding: 0 !important; min-height: 45px !important; height: 45px !important;
        border: 1px solid #eee; border-radius: 8px; background-color: #fafafa; overflow: hidden;
    }}
    div[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] {{
        width: 40px !important; height: 30px !important; background-color: white !important;
        border: 1px solid #ccc !important; color: transparent !important; position: relative;
    }}
    div[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] svg {{
        fill: #333 !important; width: 18px; height: 18px; position: absolute;
    }}
    div[data-testid="stFileUploader"] section::after, div[data-testid="stFileUploader"] label {{ display: none !important; }}
    div[data-testid="stFileUploader"] section + div {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)

# 4. TITULOK
st.title(T["title"])

# 5. CHAT AREA
chat_container = st.container()
with chat_container:
    for m in st.session_state.m:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.write("---")

# 6. SPODNÝ PANEL (Uploader a vstup)
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        # Povolené PDF, DOCX aj OBRÁZKY
        u = st.file_uploader("uploader", type=['pdf', 'docx', 'jpg', 'jpeg', 'png'], label_visibility="collapsed")
        if u is not None:
            st.info(f"📄 **{T['selected']}** {u.name}")
            
    with col2:
        if st.button(T["send_file"], use_container_width=True):
            if u:
                try:
                    text = ""
                    if u.name.lower().endswith('.pdf'):
                        text = "".join([p.extract_text() for p in pypdf.PdfReader(u).pages])
                    elif u.name.lower().endswith('.docx'):
                        text = "\n".join([para.text for para in docx.Document(u).paragraphs])
                    
                    if text.strip():
                        st.session_state.doc_content = text
                    
                    st.session_state.m.append({"role": "user", "content": T["file_msg"].format(name=u.name)})
                    with chat_container:
                        with st.chat_message("assistant"):
                            res = model_ai.generate_content(f"{T['sys_prompt']} Potvrď prijatie súboru {u.name}.")
                            st.markdown(res.text)
                            st.session_state.m.append({"role": "assistant", "content": res.text})
                    st.rerun()
                except Exception as e:
                    st.error(f"Chyba: {e}")

# 7. LOGIKA ODPOVEDE
if p := st.chat_input(T["input"]):
    st.session_state.m.append({"role": "user", "content": p})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(p)
        with st.chat_message("assistant"):
            try:
                # Kombinácia inštrukcie, kontextu z dokumentov a otázky
                full_prompt = f"{T['sys_prompt']}\n\nKontext: {st.session_state.doc_content}\n\nOtázka: {p}"
                content_to_send = [full_prompt]
                
                # Ak je v uploaderi obrázok, pridaj ho do správy
                if u and u.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img = Image.open(u)
                    content_to_send.append(img)
                
                res = model_ai.generate_content(content_to_send)
                st.markdown(res.text)
                st.session_state.m.append({"role": "assistant", "content": res.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
