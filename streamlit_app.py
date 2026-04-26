import streamlit as st
import google.generativeai as genai
import pypdf
import docx

# 1. NASTAVENIE API
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ API kľúč chýba v Secrets!")
    st.stop()

genai.configure(api_key=api_key)
model_ai = genai.GenerativeModel('gemini-1.5-flash') # Odporúčaný stabilný model

# --- INICIALIZÁCIA ---
if "m" not in st.session_state: st.session_state.m = []
if "doc_content" not in st.session_state: st.session_state.doc_content = ""

# 2. JAZYKOVÁ LOGIKA (8 Jazykov + Knižnica)
query_params = st.query_params
jazyk = query_params.get("lang", "SK").upper()

texty = {
    "SK": {
        "title": "🤖 AI Tutor", "lib_title": "📚 Knižnica", "menu": "Menu", 
        "nav_chat": "🤖 AI Tutor", "nav_lib": "📚 Knižnica materiálov",
        "selected": "Vybraný súbor:", "send_file": "Odoslať ⬆️", "input": "Napíš otázku...",
        "file_msg": "*(Súbor: {name})*", "sys_prompt": "Odpovedaj výhradne v slovenskom jazyku.",
        "lib_desc": "Tu nájdeš spoločné poznámky. Klikni na predmet pre otvorenie priečinka:"
    },
    "EN": {
        "title": "🤖 AI Tutor", "lib_title": "📚 Library", "menu": "Menu",
        "nav_chat": "🤖 AI Tutor", "nav_lib": "📚 Study Materials",
        "selected": "Selected file:", "send_file": "Send ⬆️", "input": "Ask a question...",
        "file_msg": "*(File: {name})*", "sys_prompt": "Answer exclusively in English.",
        "lib_desc": "Find shared notes here. Click a subject to open the folder:"
    },
    "DE": {
        "title": "🤖 KI-Tutor", "lib_title": "📚 Bibliothek", "menu": "Menü",
        "nav_chat": "🤖 KI-Tutor", "nav_lib": "📚 Lernmaterialien",
        "selected": "Datei:", "send_file": "Senden ⬆️", "input": "Frage stellen...",
        "file_msg": "*(Datei: {name})*", "sys_prompt": "Antworten Sie auf Deutsch.",
        "lib_desc": "Hier finden Sie Notizen. Klicken Sie auf ein Fach:"
    },
    "IT": {
        "title": "🤖 Tutor IA", "lib_title": "📚 Biblioteca", "menu": "Menu",
        "nav_chat": "🤖 Tutor IA", "nav_lib": "📚 Materiali di studio",
        "selected": "File:", "send_file": "Invia ⬆️", "input": "Fai una domanda...",
        "file_msg": "*(File: {name})*", "sys_prompt": "Rispondi in italiano.",
        "lib_desc": "Trova note condivise qui. Clicca su una materia:"
    },
    "ES": {
        "title": "🤖 Tutor IA", "lib_title": "📚 Biblioteca", "menu": "Menú",
        "nav_chat": "🤖 Tutor IA", "nav_lib": "📚 Materiales de estudio",
        "selected": "Archivo:", "send_file": "Enviar ⬆️", "input": "Preguntar...",
        "file_msg": "*(Archivo: {name})*", "sys_prompt": "Responde en español.",
        "lib_desc": "Encuentra notas aquí. Haz clic en una materia:"
    },
    "FR": {
        "title": "🤖 Tuteur IA", "lib_title": "📚 Bibliothèque", "menu": "Menu",
        "nav_chat": "🤖 Tuteur IA", "nav_lib": "📚 Matériels d'étude",
        "selected": "Fichier:", "send_file": "Envoyer ⬆️", "input": "Question...",
        "file_msg": "*(Fichier: {name})*", "sys_prompt": "Répondez en français.",
        "lib_desc": "Trouvez des notes ici. Cliquez sur une matière :"
    },
    "UA": {
        "title": "🤖 AI Тьютор", "lib_title": "📚 Бібліотека", "menu": "Меню",
        "nav_chat": "🤖 AI Тьютор", "nav_lib": "📚 Навчальні матеріаly",
        "selected": "Файл:", "send_file": "Надіслати ⬆️", "input": "Запитати...",
        "file_msg": "*(Файл: {name})*", "sys_prompt": "Відповідайте українською.",
        "lib_desc": "Тут ви знаjdete нотатки. Натисніть на предмет:"
    },
    "RU": {
        "title": "🤖 AI Тьютор", "lib_title": "📚 Библиотека", "menu": "Меню",
        "nav_chat": "🤖 AI Тьютор", "nav_lib": "📚 Учебные материалы",
        "selected": "Файл:", "send_file": "Отправить ⬆️", "input": "Спросить...",
        "file_msg": "*(Файл: {name})*", "sys_prompt": "Отвечайте на русском.",
        "lib_desc": "Здесь вы найдете заметки. Нажмите на предмет:"
    }
}
T = texty.get(jazyk, texty["SK"])

# 3. DIZAJN + CSS (Očistený uploader)
st.set_page_config(page_title=T["title"], layout="wide")

st.markdown(f"""
    <style>
    header, footer {{visibility: hidden;}} 
    .stAppDeployButton {{display:none;}}
    
    /* Štíhla lišta pre uploader */
    div[data-testid="stFileUploader"] section {{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        padding: 0 !important;
        min-height: 45px !important;
        border: 1px solid #eee;
        border-radius: 8px;
        background-color: #fafafa;
    }}

    /* Biele tlačidlo so šípkou */
    div[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] {{
        width: 40px !important;
        height: 30px !important;
        background-color: white !important;
        border: 1px solid #ccc !important;
        color: transparent !important;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 !important;
    }}

    div[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] svg {{
        fill: #333 !important;
        width: 18px;
        height: 18px;
        position: absolute;
    }}

    /* Odstránenie nápisov v uploaderi */
    div[data-testid="stFileUploader"] section::after,
    div[data-testid="stFileUploader"] section::before,
    div[data-testid="stFileUploader"] div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stFileUploader"] label {{
        display: none !important;
        content: "" !important;
    }}
    
    div[data-testid="stFileUploader"] section + div {{
        display: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. BOČNÉ MENU (NAVIGÁCIA)
with st.sidebar:
    st.title(T["menu"])
    volba = st.radio("Select:", [T["nav_chat"], T["nav_lib"]], label_visibility="collapsed")

# --- SEKCIJA 1: AI TUTOR ---
if volba == T["nav_chat"]:
    st.title(T["title"])
    
    chat_container = st.container()
    with chat_container:
        for m in st.session_state.m:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    st.write("---")

    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            u = st.file_uploader("uploader", type=['pdf', 'docx'], label_visibility="collapsed")
            if u is not None:
                st.info(f"📄 **{T['selected']}** {u.name}")
                
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

# --- SEKCIJA 2: KNIŽNICA ---
else:
    st.title(T["lib_title"])
    st.write(T["lib_desc"])
    
    # TU VLOŽ SVOJE ODKAZY Z GOOGLE DRIVE
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🇸🇰 Slovenčina")
        st.link_button("Open Folder", "TU_VLOŽ_LINK_NA_PRIEČINOK_SJL", use_container_width=True)
        
        st.subheader("🇬🇧 Angličtina")
        st.link_button("Open Folder", "TU_VLOŽ_LINK_NA_PRIEČINOK_ANJ", use_container_width=True)

    with c2:
        st.subheader("🔢 Matematika")
        st.link_button("Open Folder", "TU_VLOŽ_LINK_NA_PRIEČINOK_MAT", use_container_width=True)
        
        st.subheader("🧪 Ostatné predmety")
        st.link_button("Open Folder", "TU_VLOŽ_LINK_NA_PRIEČINOK_OSTATNE", use_container_width=True)
