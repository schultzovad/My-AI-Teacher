import streamlit as st
import google.generativeai as genai
import pypdf

# 1. NASTAVENIE MODELU (Meno, ktoré nám zafungovalo)
try:
    api_key = st.secrets["tutor"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')
except Exception as e:
    st.error("Chyba API kľúča.")

# 2. DIZAJN A JAZYK
st.set_page_config(page_title="AI Tutor", layout="wide")
st.markdown("<style>header, footer {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

if "m" not in st.session_state: st.session_state.m = []
if "pdf_text" not in st.session_state: st.session_state.pdf_text = ""

# 3. CHAT INTERFACE
st.title("🤖 AI Tutor")

# Zobrazenie histórie správ
for m in st.session_state.m:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 4. FIXNÁ ZÓNA PRE VSTUP (Súbor a Text pri sebe)
with st.container():
    st.write("---") # Čiara na oddelenie
    # Nahrávanie súboru
    u = st.file_uploader("Nahraj súbor (PDF)", type=['pdf'], label_visibility="collapsed")
    
    # Kontrola, či sa nahral nový súbor
    if u and not st.session_state.pdf_text:
        reader = pypdf.PdfReader(u)
        st.session_state.pdf_text = "".join([p.extract_text() for p in reader.pages])
        
        # Automatické odoslanie informácie o súbore do chatu
        pripomienka = "Nahral som súbor. Prosím, zosumarizuj mi ho alebo mi povedz, o čom je."
        st.session_state.m.append({"role": "user", "content": "*(Odoslaný PDF dokument)*"})
        
        with st.chat_message("assistant"):
            kontext = f"Používateľ nahral tento text: {st.session_state.pdf_text}\n\nÚloha: Potvrď prijatie a stručne povedz, o čom je tento dokument."
            response = model.generate_content(kontext)
            st.markdown(response.text)
            st.session_state.m.append({"role": "assistant", "content": response.text})

    # Písanie textu
    if p := st.chat_input("Napíš otázku..."):
        st.session_state.m.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)
        
        with st.chat_message("assistant"):
            # Ak máme v pamäti PDF, pošleme ho ako kontext
            full_prompt = f"Kontext z dokumentu: {st.session_state.pdf_text}\n\nOtázka: {p}" if st.session_state.pdf_text else p
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.m.append({"role": "assistant", "content": response.text})
