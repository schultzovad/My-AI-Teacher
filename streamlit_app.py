import streamlit as st
import google.generativeai as genai
import pypdf

# 1. NASTAVENIE
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API kľúč chýba v Secrets!")
    st.stop()

genai.configure(api_key=api_key)
model_ai = genai.GenerativeModel('gemini-3-flash-preview')

# 2. DIZAJN
st.set_page_config(page_title="AI Tutor", layout="wide")
st.markdown("<style>header, footer {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

if "m" not in st.session_state: st.session_state.m = []
if "pdf_content" not in st.session_state: st.session_state.pdf_content = ""
if "last_file" not in st.session_state: st.session_state.last_file = None

st.title("🤖 AI Tutor")

# 3. HLAVNÁ PLOCHA ČATU (Tu sa zobrazujú správy)
chat_placeholder = st.container()
with chat_placeholder:
    for m in st.session_state.m:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# 4. FIXNÁ SPODNÁ ČASŤ (Súbor a Text pri sebe)
st.markdown("---") # Oddeľovacia čiara

# Vytvoríme kontajner, ktorý v Streamlite drží veci pokope na konci
spodok = st.container()
with spodok:
    u = st.file_uploader("Priložiť PDF", type=['pdf'], label_visibility="collapsed")
    p = st.chat_input("Napíš otázku...")

# 5. LOGIKA SPRACOVANIA
# Ak sa nahrá súbor
if u is not None and u.name != st.session_state.last_file:
    try:
        reader = pypdf.PdfReader(u)
        text = "".join([page.extract_text() for page in reader.pages]).strip()
        st.session_state.pdf_content = text
        st.session_state.last_file = u.name
        
        st.session_state.m.append({"role": "user", "content": f"*(Nahraný súbor: {u.name})*"})
        with chat_placeholder:
            with st.chat_message("assistant"):
                res = model_ai.generate_content(f"Potvrď 1 vetou prijatie textu: {text[:500]}")
                st.markdown(res.text)
                st.session_state.m.append({"role": "assistant", "content": res.text})
        st.rerun()
    except Exception as e:
        st.error(f"Chyba súboru: {e}")

# Ak sa napíše text
if p:
    st.session_state.m.append({"role": "user", "content": p})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(p)
        with st.chat_message("assistant"):
            prompt = f"Kontext: {st.session_state.pdf_content}\n\nOtázka: {p}" if st.session_state.pdf_content else p
            try:
                res = model_ai.generate_content(prompt)
                st.markdown(res.text)
                st.session_state.m.append({"role": "assistant", "content": res.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
