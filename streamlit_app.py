import streamlit as st
import google.generativeai as genai
import pypdf
import docx  # Knižnica pre Word dokumenty

# 1. NASTAVENIE API A MODELU
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ API kľúč chýba! Skontroluj Secrets v Streamlit Cloud.")
    st.stop()

genai.configure(api_key=api_key)
model_ai = genai.GenerativeModel('gemini-3-flash-preview')

# 2. JAZYKOVÉ NASTAVENIA (podľa ?lang= v URL)
query_params = st.query_params
jazyk = query_params.get("lang", "SK").upper()

texty = {
    "SK": {
        "title": "🤖 AI Tutor",
        "upload": "Vybrať PDF alebo Word súbor",
        "send_file": "Odoslať súbor ⬆️",
        "input": "Napíš otázku k dokumentu...",
        "file_msg": "*(Odoslaný súbor: {name})*",
        "ai_confirm": "Súbor som úspešne prijal. Čo ťa z neho zaujíma?",
        "error_read": "Nepodarilo sa prečítať súbor.",
        "no_text": "Súbor neobsahuje žiadny čitateľný text."
    },
    "EN": {
        "title": "🤖 AI Tutor",
        "upload": "Select PDF or Word file",
        "send_file": "Send file ⬆️",
        "input": "Ask a question about the document...",
        "file_msg": "*(Uploaded file: {name})*",
        "ai_confirm": "I've received the file successfully. What would you like to know?",
        "error_read": "Failed to read the file.",
        "no_text": "The file contains no readable text."
    }
}
T = texty.get(jazyk, texty["SK"])

# 3. DIZAJN STRÁNKY
st.set_page_config(page_title=T["title"], layout="wide")
st.markdown("""
    <style>
    header, footer {visibility: hidden;} 
    .stAppDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Inicializácia pamäte (session state)
if "m" not in st.session_state: st.session_state.m = []
if "doc_content" not in st.session_state: st.session_state.doc_content = ""

st.title(T["title"])

# 4. ZOBRAZENIE ČATU
chat_container = st.container()
with chat_container:
    for m in st.session_state.m:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.write("---")

# 5. FIXNÁ SPODNÁ ZÓNA (Nahrávanie a tlačidlo)
spodny_panel = st.container()
with spodny_panel:
    col1, col2 = st.columns([4, 1])
    with col1:
        # Pridaná podpora pre .docx
        u = st.file_uploader(T["upload"], type=['pdf', 'docx'], label_visibility="collapsed")
    with col2:
        # 6. LOGIKA ODOSLANIA SÚBORU
        if st.button(T["send_file"], use_container_width=True):
            if u is not None:
                try:
                    raw_text = ""
                    # Spracovanie podľa typu súboru
                    if u.name.endswith('.pdf'):
                        reader = pypdf.PdfReader(u)
                        raw_text = "".join([p.extract_text() for p in reader.pages]).strip()
                    elif u.name.endswith('.docx'):
                        doc = docx.Document(u)
                        raw_text = "\n".join([para.text for para in doc.paragraphs]).strip()
                    
                    if raw_text:
                        st.session_state.doc_content = raw_text
                        st.session_state.m.append({"role": "user", "content": T["file_msg"].format(name=u.name)})
                        
                        with chat_container:
                            with st.chat_message("assistant"):
                                prompt_intro = f"System: User uploaded a document named {u.name}. Context start: {raw_text[:500]}. Briefly confirm receipt in {jazyk}: {T['ai_confirm']}"
                                res = model_ai.generate_content(prompt_intro)
                                st.markdown(res.text)
                                st.session_state.m.append({"role": "assistant", "content": res.text})
                        st.rerun()
                    else:
                        st.warning(T["no_text"])
                except Exception as e:
                    st.error(f"{T['error_read']}: {e}")
            else:
                st.info("Najprv vyber súbor v okienku vľavo.")

# 7. LOGIKA PÍSANIA OTÁZOK
p = st.chat_input(T["input"])
if p:
    st.session_state.m.append({"role": "user", "content": p})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(p)
        with st.chat_message("assistant"):
            # Spojíme kontext z dokumentu a otázku
            if st.session_state.doc_content:
                full_prompt = f"Kontext z nahraného dokumentu: {st.session_state.doc_content}\n\nOtázka používateľa: {p}\nOdpovedaj v jazyku: {jazyk}"
            else:
                full_prompt = f"{p}\nOdpovedaj v jazyku: {jazyk}"
            
            try:
                res = model_ai.generate_content(full_prompt)
                st.markdown(res.text)
                st.session_state.m.append({"role": "assistant", "content": res.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
