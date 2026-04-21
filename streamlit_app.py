import streamlit as st
import google.generativeai as genai
import pypdf

# 1. NASTAVENIE - Skúsime obidva názvy kľúča, aby sme sa trafili
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Chyba: API kľúč sa nenašiel! Skontroluj Secrets v Streamlite.")
else:
    try:
        genai.configure(api_key=api_key)
        # Toto meno sme si overili v Playgrounde, že funguje
        model_ai = genai.GenerativeModel('gemini-3-flash-preview')
    except Exception as e:
        st.error(f"Chyba pripojenia k AI: {e}")

# 2. DIZAJN
st.set_page_config(page_title="AI Tutor", layout="wide")
st.markdown("<style>header, footer {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

if "m" not in st.session_state: st.session_state.m = []
if "pdf_text" not in st.session_state: st.session_state.pdf_text = ""

st.title("🤖 AI Tutor")

# 3. ZOBRAZENIE HISTÓRIE ČATU
for m in st.session_state.m:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 4. SPODNÁ ZÓNA (Nahrávanie a písanie spolu)
st.write("---")

# Nahrávanie súboru
u = st.file_uploader("Priložiť PDF dokument", type=['pdf'], label_visibility="collapsed")

# Spracovanie súboru hneď po nahratí
if u and not st.session_state.pdf_text:
    try:
        reader = pypdf.PdfReader(u)
        st.session_state.pdf_text = "".join([p.extract_text() for p in reader.pages])
        
        # AI hneď zareaguje na dokument
        with st.chat_message("assistant"):
            info_prompt = f"Používateľ nahral dokument. Tu je jeho obsah: {st.session_state.pdf_text[:2000]}. Krátko potvrď prijatie dokumentu a povedz, čo v ňom je."
            odpoved = model_ai.generate_content(info_prompt)
            st.session_state.m.append({"role": "user", "content": "*(Odoslaný PDF súbor)*"})
            st.session_state.m.append({"role": "assistant", "content": odpoved.text})
            st.rerun()
    except Exception as e:
        st.error(f"Nepodarilo sa spracovať PDF: {e}")

# Písanie textu
if p := st.chat_input("Napíš otázku k dokumentu..."):
    st.session_state.m.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    
    with st.chat_message("assistant"):
        # Pošleme otázku spolu s textom z PDF (ak existuje)
        finalny_prompt = f"Dokument: {st.session_state.pdf_text}\n\nOtázka: {p}" if st.session_state.pdf_text else p
        try:
            odpoved = model_ai.generate_content(finalny_prompt)
            st.markdown(odpoved.text)
            st.session_state.m.append({"role": "assistant", "content": odpoved.text})
        except Exception as e:
            st.error(f"AI teraz nemôže odpovedať: {e}")
