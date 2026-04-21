import streamlit as st
import google.generativeai as genai
import pypdf

# 1. Napojenie na Secrets (to, čo si dala do Advanced Settings)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Chyba: Kľúč v Secrets sa nenašiel alebo je nesprávny.")

# 2. Jazyky podľa adresy (?lang=SK)
L = st.query_params.get("lang", "SK").upper()
lang_data = {
    "SK": {"t": "🤖 AI Tutor", "up": "📁 Nahrať PDF", "ok": "Hotovo!", "ask": "Opýtaj sa..."},
    "EN": {"t": "🤖 AI Tutor", "up": "📁 Upload PDF", "ok": "Ready!", "ask": "Ask me..."}
}
t = lang_data.get(L, lang_data["SK"])

# 3. Vzhľad
st.set_page_config(page_title=t["t"], layout="wide")
st.markdown("<style>header, footer {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title(t["t"])

# 4. Nahrávanie PDF
if "pdf_text" not in st.session_state: st.session_state.pdf_text = ""

with st.expander(t["up"]):
    u = st.file_uploader("PDF", type=['pdf'], label_visibility="collapsed")
    if u:
        reader = pypdf.PdfReader(u)
        st.session_state.pdf_text = "".join([p.extract_text() for p in reader.pages])
        st.success(t["ok"])

# 5. Chat
if "m" not in st.session_state: st.session_state.m = []
for m in st.session_state.m:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input(t["ask"]):
    st.session_state.m.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)
    
    with st.chat_message("assistant"):
        context = f"Tu sú podklady: {st.session_state.pdf_text}\n\nOtázka: {p}" if st.session_state.pdf_text else p
        try:
            res = model.generate_content(context)
            st.markdown(res.text)
            st.session_state.m.append({"role": "assistant", "content": res.text})
        except Exception as e:
            st.error(f"AI neodpovedá: {e}")
