import streamlit as st
import google.generativeai as genai
import pypdf

# 1. NASTAVENIE - tvoj overený kľúč a model
try:
    api_key = st.secrets["tutor"]
    genai.configure(api_key=api_key)
    # Používame ten model, ktorý ti v Playgrounde fungoval
    moj_model = genai.GenerativeModel('gemini-3-flash-preview')
except Exception as e:
    st.error("Chyba API kľúča v Secrets!")

# 2. DIZAJN
st.set_page_config(page_title="AI Tutor", layout="wide")
st.markdown("<style>header, footer {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

if "m" not in st.session_state: st.session_state.m = []
if "pdf_text" not in st.session_state: st.session_state.pdf_text = ""

st.title("🤖 AI Tutor")

# 3. ZOBRAZENIE ČATU (História)
for m in st.session_state.m:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 4. SPODNÁ ZÓNA (Nahrávanie a písanie spolu)
st.write("---")

# Nahrávanie súboru (zostáva stále viditeľné nad chatom)
u = st.file_uploader("Priložiť súbor (PDF)", type=['pdf'], label_visibility="collapsed")

# Ak sa nahrá súbor, hneď ho spracujeme a AI odpovie
if u and not st.session_state.pdf_text:
    try:
        reader = pypdf.PdfReader(u)
        st.session_state.pdf_text = "".join([p.extract_text() for p in reader.pages])
        
        # AI hneď zareaguje na dokument
        with st.chat_message("assistant"):
            info_prompt = f"Používateľ nahral dokument s týmto obsahom: {st.session_state.pdf_text[:2000]}... Potvrď prijatie dokumentu a stručne (2 vetami) povedz, o čom je."
            odpoved = moj_model.generate_content(info_prompt)
            st.session_state.m.append({"role": "user", "content": "*(Odoslaný PDF súbor)*"})
            st.session_state.m.append({"role": "assistant", "content": odpoved.text})
            st.rerun() # Refreshne stránku, aby sa správa hneď ukázala
    except:
        st.error("Nepodarilo sa spracovať PDF.")

# Písanie textu
if p := st.chat_input("Napíš otázku k dokumentu alebo len tak..."):
    st.session_state.m.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    
    with st.chat_message("assistant"):
        # Ak máme v pamäti PDF, pošleme ho ako kontext
        finalny_prompt = f"Kontext z dokumentu: {st.session_state.pdf_text}\n\nOtázka: {p}" if st.session_state.pdf_text else p
        odpoved = moj_model.generate_content(finalny_prompt)
        st.markdown(odpoved.text)
        st.session_state.m.append({"role": "assistant", "content": odpoved.text})
