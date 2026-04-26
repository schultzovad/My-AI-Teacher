import streamlit as st
import google.generativeai as genai
import pypdf

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
        "upload": "Vybrať PDF súbor",
        "send_file": "Odoslať súbor ⬆️",
        "input": "Napíš otázku k dokumentu...",
        "file_msg": "*(Odoslaný súbor: {name})*",
        "ai_confirm": "Súbor som úspešne prijal. Čo ťa z neho zaujíma?",
        "error_pdf": "Nepodarilo sa prečítať PDF (skontroluj, či nie je chránené heslom)."
    },
    "EN": {
        "title": "🤖 AI Tutor",
        "upload": "Select PDF file",
        "send_file": "Send file ⬆️",
        "input": "Ask a question about the document...",
        "file_msg": "*(Uploaded file: {name})*",
        "ai_confirm": "I've received the file successfully. What would you like to know?",
        "error_pdf": "Failed to read PDF (check if it's not password protected)."
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
if "pdf_content" not in st.session_state: st.session_state.pdf_content = ""

st.title(T["title"])

# 4. ZOBRAZENIE ČATU (Hlavná plocha)
chat_container = st.container()
with chat_container:
    for m in st.session_state.m:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

st.write("---")

# 5. FIXNÁ SPODNÁ ZÓNA (Nahrávanie a tlačidlo na odoslanie)
spodny_panel = st.container()
with spodny_panel:
    col1, col2 = st.columns([4, 1])
    with col1:
        u = st.file_uploader(T["upload"], type=['pdf'], label_visibility="collapsed")
    with col2:
        # 6. LOGIKA ODOSLANIA SÚBORU
        if st.button(T["send_file"], use_container_width=True):
            if u is not None:
                try:
                    reader = pypdf.PdfReader(u)
                    raw_text = "".join([p.extract_text() for p in reader.pages]).strip()
                    if raw_text:
                        st.session_state.pdf_content = raw_text
                        st.session_state.m.append({"role": "user", "content": T["file_msg"].format(name=u.name)})
                        
                        with chat_container:
                            with st.chat_message("assistant"):
                                prompt_intro = f"System: User uploaded document. Context: {raw_text[:500]}. Briefly confirm receipt in {jazyk}: {T['ai_confirm']}"
                                res = model_ai.generate_content(prompt_intro)
                                st.markdown(res.text)
                                st.session_state.m.append({"role": "assistant", "content": res.text})
                        st.rerun()
                    else:
                        st.warning("Tento PDF súbor neobsahuje čitateľný text.")
                except Exception as e:
                    st.error(f"{T['error_pdf']}: {e}")
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
            # Spojíme kontext z PDF (ak existuje) a otázku
            if st.session_state.pdf_content:
                full_prompt = f"Kontext z nahraného dokumentu: {st.session_state.pdf_content}\n\nOtázka používateľa: {p}\nOdpovedaj v jazyku: {jazyk}"
            else:
                full_prompt = f"{p}\nOdpovedaj v jazyku: {jazyk}"
            
            try:
                res = model_ai.generate_content(full_prompt)
                st.markdown(res.text)
                st.session_state.m.append({"role": "assistant", "content": res.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
