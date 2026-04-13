import streamlit as st
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="AI Tutor", layout="centered", page_icon="🎓")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Chýba API kľúč!")

AVAILABLE_MODELS = ['gemini-flash-latest', 'gemini-2.0-flash', 'gemini-pro-latest']

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. TITULOK A HISTÓRIA ČETU
st.title("🎓 Tvoj osobný AI učiteľ")

# Vypísanie histórie (toto bude rásť a posúvať všetko pod sebou nižšie)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. MIESTO PRE NOVÚ ODPOVEĎ (keď práve AI píše)
placeholder_for_new_response = st.container()

st.write("---")

# 4. NAHRÁVAČ SÚBOROV (Teraz je až pod históriou)
with st.container():
    uploaded_files = st.file_uploader(
        "Prilož poznámky alebo fotku", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="file_uploader_fixed"
    )
    
    # Tlačidlo "Vysvetli" hneď pod nahrávačom
    analyze_clicked = False
    if uploaded_files:
        if st.button("✨ Vysvetli mi nahrané súbory"):
            analyze_clicked = True

# 5. ČETOVACIE POLE (Úplne naspodu)
input_text = st.chat_input("Opýtaj sa na čokoľvek...")

# 6. LOGIKA SPRACOVANIA
if input_text or analyze_clicked:
    prompt = input_text if input_text else "Prosím, vysvetli mi tieto súbory ako učiteľ."
    
    # Pridáme do histórie a hneď zobrazíme
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Musíme urobiť rerun, aby sa nahrávač posunul pod novú správu
    # Alebo to môžeme zobraziť manuálne:
    st.rerun()

# Táto časť sa spustí po rerun-e, ak posledná správa je od užívateľa
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        container = st.empty()
        payload = []
        
        teacher_prompt = """
        Si skúsený, milý a trpezlivý učiteľ. 
        Tvojou úlohou je vysvetľovať učivo ľudsky a zrozumiteľne.
        Ak sú na fotkách príklady, vyrieš ich krok po kroku.
        Buď povzbudivý, ale 100% odborne správny.
        """
        payload.append(teacher_prompt)
        
        # Posledné správy pre kontext
        for m in st.session_state.messages[-6:]:
            payload.append(f"{m['role']}: {m['content']}")

        # Súbory (ak sú prítomné v nahrávači)
        if uploaded_files:
            for f in uploaded_files:
                payload.append({'mime_type': f.type, 'data': f.getvalue()})

        success = False
        full_response = ""
        for model_name in AVAILABLE_MODELS:
            if success: break
            try:
                with st.spinner('Učiteľ premýšľa...'):
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(payload)
                    full_response = response.text
                    success = True
            except Exception as e:
                if "429" in str(e): continue
                else: break
        
        if not success:
            full_response = "Daj mi prosím 30 sekúnd, pauza na kávu! ☕😊"

        container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        # Opätovný rerun, aby sa nahrávač a chat_input vykreslili pod novou odpoveďou
        st.rerun()

with st.sidebar:
    if st.button("🗑️ Nová téma"):
        st.session_state.messages = []
        st.rerun()
