import streamlit as st
import google.generativeai as genai
import pypdf

# 1. NASTAVENIE API A MODELU
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API kľúč chýba! Skontroluj Secrets v Streamlit Cloud.")
    st.stop()

genai.configure(api_key=api_key)
# Používame tvoj overený model z Playgroundu
model_ai = genai.GenerativeModel('gemini-3-flash-preview')

# 2. JAZYKOVÉ NASTAVENIA (podľa ?lang= v URL)
query_params = st.query_params
jazyk = query_params.get("lang", "SK").upper()

texty = {
    "SK": {
        "title": "🤖 AI Tutor",
        "upload": "Priložiť PDF dokument",
        "input": "Napíš otázku k dokumentu...",
        "file_msg": "*(Nahraný súbor: {name})*",
        "ai_confirm": "Súbor som prijal. O čom sa chceš dozvedieť?",
        "error_pdf": "Nepodarilo sa prečítať PDF."
    },
    "EN": {
        "title": "🤖 AI Tutor",
        "upload": "Attach PDF document",
        "input": "Ask a question about the document...",
        "file_msg": "*(Uploaded file: {name})*",
        "ai_confirm": "I've received the file. What would you like to know?",
        "error_pdf": "Failed to read PDF."
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
if "last_file" not in st.session_state: st.session_state.last_file = None

st.title(T["title"])

# 4. ZOBRAZENIE ČATU (Hlavná plocha)
chat_container = st.container()
with chat_container:
    for m in st.session_state.m:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# 5. FIXNÁ SPODNÁ ČASŤ (Súbor a Text pri sebe)
st.write("---")
spodny_panel = st.container()

with spodny_panel:
    u = st.file_uploader(T["upload"], type=['pdf'], label_visibility="collapsed")
    p = st.chat_input(T["input"])

# 6. LOGIKA SÚBORU (Spracuje sa hneď po nahratí)
if u is not None and u.name != st.session_state.last_file:
    try:
        reader = pypdf.PdfReader(u)
        raw_text = "".join([page.extract_text() for page in reader.pages]).strip()
        
        if raw_text:
            st.session_state.pdf_content = raw_text
            st.session_state.last_file = u.name
            
            # Pridáme záznam o súbore do čatu
            st.session_state.m.append({"role": "user", "content": T["file_msg"].format(name=u.name)})
            
            with chat_container:
                with st.chat_message("assistant"):
                    # Krátka AI reakcia na nový súbor
                    prompt_intro = f"System: User uploaded a document. Context: {raw_text[:500]}. Respond in {jazyk} briefly: {T['ai_confirm']}"
                    res = model_ai.generate_content(prompt_intro)
                    st.markdown(res.text)
                    st.session_state.m.append({"role": "assistant", "content": res.text})
            st.rerun()
    except Exception as e:
        st.error(f"{T['error_pdf']}: {e}")

# 7. LOGIKA OTÁZOK
if p:
    st.session_state.m.append({"role": "user", "content": p})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(p)
        
        with st.chat_message("assistant"):
            # Spojíme kontext z PDF a otázku
            if st.session_state.pdf_content:
                plny_prompt = f"Kontext z dokumentu: {st.session_state.pdf_content}\n\nOtázka používateľa: {p}\nOdpovedaj v jazyku: {jazyk}"
            else:
                plny_prompt = p
            
            try:
                res = model_ai.generate_content(plny_prompt)
                st.markdown(res.text)
                st.session_state.m.append({"role": "assistant", "content": res.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
