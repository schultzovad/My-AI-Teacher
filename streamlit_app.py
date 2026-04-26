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

# --- INICIALIZÁCIA (Dôležité pre odstránenie Erroru) ---
if "m" not in st.session_state: st.session_state.m = []
if "doc_content" not in st.session_state: st.session_state.doc_content = ""

# 2. JAZYKOVÁ LOGIKA
query_params = st.query_params
jazyk = query_params.get("lang", "SK").upper()

texty = {
    "SK": {"title": "🤖 AI Tutor", "up_button": "Nahrať súbor", "up_prompt": "PDF alebo DOCX", "send_file": "Odoslať ⬆️", "input": "Napíš otázku...", "file_msg": "*(Súbor: {name})*", "sys_prompt": "Odpovedaj výhradne v slovenskom jazyku."},
    "EN": {"title": "🤖 AI Tutor", "up_button": "Upload file", "up_prompt": "PDF or DOCX", "send_file": "Send ⬆️", "input": "Ask a question...", "file_msg": "*(File: {name})*", "sys_prompt": "Answer exclusively in English."},
    "DE": {"title": "🤖 KI-Tutor", "up_button": "Hochladen", "up_prompt": "PDF oder DOCX", "send_file": "Senden ⬆️", "input": "Stellen Sie eine Frage...", "file_msg": "*(Datei: {name})*", "sys_prompt": "Antworten Sie ausschließlich auf Deutsch."},
    "IT": {"title": "🤖 Tutor IA", "up_button": "Carica", "up_prompt": "PDF o DOCX", "send_file": "Invia ⬆️", "input": "Fai una domanda...", "file_msg": "*(File: {name})*", "sys_prompt": "Rispondi esclusivamente in italiano."},
    "ES": {"title": "🤖 Tutor IA", "up_button": "Subir", "up_prompt": "PDF o DOCX", "send_file": "Enviar ⬆️", "input": "Haz una pregunta...", "file_msg": "*(Archivo: {name})*", "sys_prompt": "Responde exclusivamente en español."},
    "FR": {"title": "🤖 Tuteur IA", "up_button": "Charger", "up_prompt": "PDF ou DOCX", "send_file": "Envoyer ⬆️", "input": "Posez une question...", "file_msg": "*(Fichier: {name})*", "sys_prompt": "Répondez exclusivement en français."},
    "UA": {"title": "🤖 AI Тьютор", "up_button": "Завантажити", "up_prompt": "PDF або DOCX", "send_file": "Надіслати ⬆️", "input": "Запитайте щось...", "file_msg": "*(Файл: {name})*", "sys_prompt": "Відповідайте виключно українською мовою."},
    "RU": {"title": "🤖 AI Тьютор", "up_button": "Загрузить", "up_prompt": "PDF или DOCX", "send_file": "Отправить ⬆️", "input": "Задайте вопрос...", "file_msg": "*(Файл: {name})*", "sys_prompt": "Отвечайте исключительно на русском языке."}
}
T = texty.get(jazyk, texty["SK"])

# 3. DIZAJN + CSS (Štíhly a elegantný uploader)
st.set_page_config(page_title=T["title"], layout="wide")

st.markdown(f"""
    <style>
    header, footer {{visibility: hidden;}} 
    .stAppDeployButton {{display:none;}}
    
    /* Zmenšenie celého nahrávacieho boxu na jeden riadok */
    div[data-testid="stFileUploader"] section {{
        display: flex;
        flex-direction: row; /* Všetko v jednom riadku */
        align-items: center;
        justify-content: flex-start;
        padding: 5px 15px !important;
        min-height: 50px !important;
        border: 1px solid #ddd;
        border-radius: 8px;
    }}

    /* Biele tlačidlo so šípkou (naľavo) */
    div[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] {{
        width: 40px !important;
        height: 30px !important;
        background-color: white !important;
        border: 1px solid #ccc !important;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 10px 0 0 !important;
        color: transparent !important;
        position: relative;
    }}

    /* Ikona šípky v strede malého tlačidla */
    div[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] svg {{
        fill: #333 !important;
        width: 18px;
        height: 18px;
        position: absolute;
    }}

    /* Skrytie všetkých pôvodných textov */
    div[data-testid="stFileUploader"] section div[data-testid="stMarkdownContainer"] p {{
        display: none !important;
    }}
    
    /* Vloženie textu HNEĎ NAPRAVO od tlačidla */
    div[data-testid="stFileUploader"] section::after {{
        content: "{T['up_button']} (200MB • {T['up_prompt']})";
        color: #555;
        font-size: 14px;
        white-space: nowrap;
    }}
    
    /* Odstránenie prebytočných kontajnerov a ikoniek napravo */
    div[data-testid="stFileUploader"] section > div:nth-child(2),
    div[data-testid="stFileUploader"] section svg[data-testid="stIcon"] {{
        display: none !important;
    }}
    </style>
""", unsafe_allow_html=True)
# 4. CHAT AREA (Teraz bezpečne po inicializácii)
chat_container = st.container()
with chat_container:
    for m in st.session_state.m:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.write("---")

# 5. SPODNÝ PANEL
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

# 6. PÍSANIE OTÁZKY
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
