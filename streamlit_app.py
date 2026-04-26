import streamlit as st
import google.generativeai as genai
import pypdf
import docx

# 1. NASTAVENIE API
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ API kľúč chýba! Skontroluj Secrets v Streamlit Cloud (Advanced settings).")
    st.stop()

genai.configure(api_key=api_key)
# Používame model, ktorý ti overene funguje
model_ai = genai.GenerativeModel('gemini-3-flash-preview')

# 2. JAZYKOVÁ LOGIKA (Prepojené s URL parametrom ?lang=)
query_params = st.query_params
jazyk = query_params.get("lang", "SK").upper()

# Slovník všetkých textov v aplikácii
texty = {
    "SK": {
        "title": "🤖 AI Tutor",
        "upload": "Vybrať súbor (PDF, DOCX)",
        "send_file": "Odoslať súbor ⬆️",
        "input": "Napíš otázku k dokumentu...",
        "file_msg": "*(Odoslaný súbor: {name})*",
        "ai_confirm": "Súbor som prijal. Čo ťa z neho zaujíma?",
        "error_read": "Chyba pri čítaní súboru.",
        "no_text": "Súbor neobsahuje čitateľný text.",
        "sys_prompt": "Hovor a odpovedaj výhradne v slovenskom jazyku. Buď stručný a nápomocný."
    },
    "EN": {
        "title": "🤖 AI Tutor",
        "upload": "Select file (PDF, DOCX)",
        "send_file": "Send file ⬆️",
        "input": "Ask a question...",
        "file_msg": "*(Uploaded file: {name})*",
        "ai_confirm": "File received. What would you like to know?",
        "error_read": "Error reading file.",
        "no_text": "File contains no readable text.",
        "sys_prompt": "Speak and answer exclusively in English. Be concise and helpful."
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
    /* Úprava okrajov, aby to vo Frameri lepšie sedelo */
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    </style>
""", unsafe_allow_html=True)

# Inicializácia pamäte (session state)
if "m" not in st.session_state: st.session_state.m = []
if "doc_content" not in st.session_state: st.session_state.doc_content = ""

st.title(T["title"])

# 4. ZOBRAZENIE ČATU (Hlavná plocha)
chat_container = st.container()
with chat_container:
    for m in st.session_state.m:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.write("---")

# 5. SPODNÁ ZÓNA (Nahrávanie a tlačidlo na odoslanie súboru)
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        u = st.file_uploader(T["upload"], type=['pdf', 'docx'], label_visibility="collapsed")
    with col2:
        # Tlačidlo na manuálne odoslanie súboru
        if st.button(T["send_file"], use_container_width=True):
            if u:
                try:
                    text = ""
                    if u.name.endswith('.pdf'):
                        # Čítanie PDF
                        reader = pypdf.PdfReader(u)
                        text = "".join([p.extract_text() for p in reader.pages]).strip()
                    else:
                        # Čítanie Wordu
                        doc = docx.Document(u)
                        text = "\n".join([para.text for para in doc.paragraphs]).strip()
                    
                    if text:
                        st.session_state.doc_content = text
                        # Pridáme vizuálnu info do čatu o nahraní
                        st.session_state.m.append({"role": "user", "content": T["file_msg"].format(name=u.name)})
                        
                        # AI hneď potvrdí prijatie v správnom jazyku
                        with chat_container:
                            with st.chat_message("assistant"):
                                res = model_ai.generate_content(f"{T['sys_prompt']} Potvrď jednou vetou prijatie dokumentu {u.name}.")
                                st.markdown(res.text)
                                st.session_state.m.append({"role": "assistant", "content": res.text})
                        st.rerun()
                    else:
                        st.warning(T["no_text"])
                except Exception as e:
                    st.error(f"{T['error_read']}: {e}")
            else:
                st.info("Najprv vyber súbor.")

# 6. PÍSANIE OTÁZOK
p = st.chat_input(T["input"])
if p:
    st.session_state.m.append({"role": "user", "content": p})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(p)
        
        with st.chat_message("assistant"):
            # Kombinujeme systémový príkaz na jazyk + obsah dokumentu + otázku
            if st.session_state.doc_content:
                full_prompt = f"{T['sys_prompt']}\n\nKontext z dokumentu: {st.session_state.doc_content}\n\nOtázka používateľa: {p}"
            else:
                full_prompt = f"{T['sys_prompt']}\n\nOtázka používateľa: {p}"
            
            try:
                res = model_ai.generate_content(full_prompt)
                st.markdown(res.text)
                st.session_state.m.append({"role": "assistant", "content": res.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
