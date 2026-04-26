import streamlit as st
import google.generativeai as genai
import pypdf
import docx

# 1. NASTAVENIE API
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ API kľúč chýba!")
    st.stop()

genai.configure(api_key=api_key)
model_ai = genai.GenerativeModel('gemini-3-flash-preview')

# 2. JAZYKOVÁ LOGIKA (Prepojené s Framerom cez ?lang=)
query_params = st.query_params
jazyk = query_params.get("lang", "SK").upper()

texty = {
    "SK": {
        "title": "🤖 AI Tutor",
        "up_button": "Nahrať",       # Text na tlačidle (namiesto Upload)
        "up_prompt": "alebo pretiahnite súbor (PDF, DOCX)", # Prompt (namiesto Drag & Drop)
        "send_file": "Odoslať ⬆️",
        "input": "Napíš otázku...",
        "file_msg": "*(Súbor: {name})*",
        "ai_confirm": "Prijaté. Čo chceš vedieť?",
        "sys_prompt": "Odpovedaj výhradne v slovenskom jazyku."
    },
    "EN": {
        "title": "🤖 AI Tutor",
        "up_button": "Upload",
        "up_prompt": "or drag file (PDF, DOCX)",
        "send_file": "Send ⬆️",
        "input": "Ask a question...",
        "file_msg": "*(File: {name})*",
        "ai_confirm": "Received. What do you want to know?",
        "sys_prompt": "Answer exclusively in English."
    },
    "DE": {
        "title": "🤖 KI-Tutor",
        "up_button": "Hochladen",
        "up_prompt": "oder Datei ziehen (PDF, DOCX)",
        "send_file": "Senden ⬆️",
        "input": "Stellen Sie eine Frage...",
        "file_msg": "*(Datei: {name})*",
        "ai_confirm": "Erhalten. Was möchten Sie wissen?",
        "sys_prompt": "Antworten Sie ausschließlich auf Deutsch."
    },
    # Taliansky, Španielsky, Francúzsky atď. sa sem pridajú rovnako
    "IT": {"title": "🤖 Tutor IA", "up_button": "Carica", "up_prompt": "o trascina file (PDF, DOCX)", "send_file": "Invia ⬆️", "input": "Fai una domanda...", "file_msg": "*(File: {name})*", "ai_confirm": "Ricevuto. Cosa vuoi sapere?", "sys_prompt": "Rispondi esclusivamente in italiano."},
    "ES": {"title": "🤖 Tutor IA", "up_button": "Subir", "up_prompt": "o arrastra archivo (PDF, DOCX)", "send_file": "Enviar ⬆️", "input": "Haz una pregunta...", "file_msg": "*(Archivo: {name})*", "ai_confirm": "Recibido. ¿Qué quieres saber?", "sys_prompt": "Responde exclusivamente en español."},
    "FR": {"title": "🤖 Tuteur IA", "up_button": "Charger", "up_prompt": "ou faites glisser le fichier (PDF, DOCX)", "send_file": "Envoyer ⬆️", "input": "Posez une question...", "file_msg": "*(Fichier: {name})*", "ai_confirm": "Reçu. Que voulez-vous savoir ?", "sys_prompt": "Répondez exclusivement en français."},
    "UA": {"title": "🤖 AI Тьютор", "up_button": "Завантажити", "up_prompt": "або перетягніть файл (PDF, DOCX)", "send_file": "Надіслати ⬆️", "input": "Запитайте щось...", "file_msg": "*(Файл: {name})*", "ai_confirm": "Отримано. Що ви хочете знати?", "sys_prompt": "Відповідайте виключно українською мовою."},
    "RU": {"title": "🤖 AI Тьютор", "up_button": "Загрузить", "up_prompt": "или перетащите файл (PDF, DOCX)", "send_file": "Отправить ⬆️", "input": "Задайте вопрос...", "file_msg": "*(Файл: {name})*", "ai_confirm": "Получено. Что вы хотите знать?", "sys_prompt": "Отвечайте исключительно на русском языке."}
}
T = texty.get(jazyk, texty["SK"])

# 3. DIZAJN + CSS (Trik na preklad nahrávacieho boxu)
st.set_page_config(page_title=T["title"], layout="wide")

st.markdown(f"""
    <style>
    /* Skryje hlavnú lištu a pätu */
    header, footer {{visibility: hidden;}} 
    .stAppDeployButton {{display:none;}}
    
    /* PREKLAD NAHRÁVACIEHO BOXU */
    /* Nápis na tlačidle (Upload) */
    div[data-testid="stFileUploader"] section > div[data-testid="stMarkdownContainer"] button::before {{
        content: "{T['up_button']}";
        font-weight: bold;
    }}
    div[data-testid="stFileUploader"] section > div[data-testid="stMarkdownContainer"] button {{
        color: transparent;
    }}
    
    /* Zvýraznený text (Limit 200MB...) a prompt (Drag & Drop) */
    /* Tento kód skryje pôvodné anglické texty */
    div[data-testid="stFileUploader"] div[data-testid="stMarkdownContainer"] p {{
        visibility: hidden;
    }}
    
    /* Tento kód vloží tvoj preložený text na ich miesto */
    div[data-testid="stFileUploader"] div[data-testid="stMarkdownContainer"]::before {{
        content: "{T['up_prompt']}";
        visibility: visible;
        display: block;
        color: #555;
        font-size: 14px;
        margin-top: -15px; /* Zarovnanie */
    }}
    </style>
""", unsafe_allow_html=True)

if "m" not in st.session_state: st.session_state.m = []
if "doc_content" not in st.session_state: st.session_state.doc_content = ""

st.title(T["title"])

# 4. CHAT AREA
chat_container = st.container()
with chat_container:
    for m in st.session_state.m:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.write("---")

# 5. SPODNÝ PANEL (Uploader a tlačidlo)
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        u = st.file_uploader("uploader", type=['pdf', 'docx'], label_visibility="collapsed")
    with col2:
        if st.button(T["send_file"], use_container_width=True):
            if u:
                try:
                    text = ""
                    if u.name.endswith('.pdf'):
                        text = "".join([p.extract_text() for p in pypdf.PdfReader(u).pages])
                    else:
                        text = "\n".join([para.text for para in docx.Document(u).paragraphs])
                    
                    if text.strip():
                        st.session_state.doc_content = text
                        st.session_state.m.append({"role": "user", "content": T["file_msg"].format(name=u.name)})
                        with chat_container:
                            with st.chat_message("assistant"):
                                res = model_ai.generate_content(f"{T['sys_prompt']} Krátko potvrď prijatie dokumentu {u.name}.")
                                st.markdown(res.text)
                                st.session_state.m.append({"role": "assistant", "content": res.text})
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# 6. LOGIKA PÍSANIA
if p := st.chat_input(T["input"]):
    st.session_state.m.append({"role": "user", "content": p})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(p)
        with st.chat_message("assistant"):
            full_prompt = f"{T['sys_prompt']}\n\nKontext: {st.session_state.doc_content}\n\nOtázka: {p}"
            try:
                res = model_ai.generate_content(full_prompt)
                st.markdown(res.text)
                st.session_state.m.append({"role": "assistant", "content": res.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
