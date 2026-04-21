import streamlit as st
import google.generativeai as genai
import pypdf

# 1. NASTAVENIE - Skúsime oba názvy kľúča
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API kľúč chýba! Skontroluj Secrets v Streamlit Cloud (Advanced Settings).")
    st.stop()

genai.configure(api_key=api_key)
model_ai = genai.GenerativeModel('gemini-3-flash-preview')

# 2. DIZAJN
st.set_page_config(page_title="AI Tutor", layout="wide")
st.markdown("<style>header, footer {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

# Inicializácia pamäte, ak ešte neexistuje
if "m" not in st.session_state: st.session_state.m = []
if "last_file" not in st.session_state: st.session_state.last_file = None
if "pdf_content" not in st.session_state: st.session_state.pdf_content = ""

st.title("🤖 AI Tutor")

# 3. ZOBRAZENIE CHATU
for m in st.session_state.m:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 4. NAHRÁVANIE SÚBORU (v spodnej časti)
st.write("---")
u = st.file_uploader("Priložiť PDF", type=['pdf'], label_visibility="collapsed")

# Spracovanie súboru LEN ak je nový
if u is not None and u.name != st.session_state.last_file:
    try:
        reader = pypdf.PdfReader(u)
        text = "".join([page.extract_text() for page in reader.pages]).strip()
        
        if text:
            st.session_state.pdf_content = text
            st.session_state.last_file = u.name
            
            # Pridáme info do chatu
            st.session_state.m.append({"role": "user", "content": f"*(Nahraný súbor: {u.name})*"})
            
            with st.chat_message("assistant"):
                res = model_ai.generate_content(f"Používateľ nahral súbor: {text[:2000]}. Krátko (1 veta) potvrď, že ho máš.")
                st.markdown(res.text)
                st.session_state.m.append({"role": "assistant", "content": res.text})
            st.rerun()
        else:
            st.warning("Súbor sa zdá byť prázdny alebo je to len obrázok.")
    except Exception as e:
        st.error(f"Chyba PDF: {e}")

# 5. PÍSANIE OTÁZKY
if p := st.chat_input("Napíš otázku k dokumentu..."):
    st.session_state.m.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    
    with st.chat_message("assistant"):
        full_p = f"Kontext z dokumentu: {st.session_state.pdf_content}\n\nOtázka: {p}" if st.session_state.pdf_content else p
        try:
            res = model_ai.generate_content(full_p)
            st.markdown(res.text)
            st.session_state.m.append({"role": "assistant", "content": res.text})
        except Exception as e:
            st.error(f"AI Error: {e}")
