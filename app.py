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

# 2. TITULOK A HISTÓRIA ČETU (Vypíše sa ako prvá)
st.title("🎓 Tvoj osobný AI učiteľ")
st.caption("Nahraj fotku a pýtaj sa. Som tu, aby som ti pomohol všetko pochopiť! 😊")

# Vypísanie všetkých správ, ktoré už v čete sú
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. SPODNÁ ČASŤ - TU JE ZMENA (Nahrávač je až pod históriou)
st.write("---") 

# Tento kontajner zabezpečí, že nahrávač bude vždy na konci
with st.container():
    uploaded_files = st.file_uploader(
        "Prilož poznámky alebo fotku", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="file_uploader_bottom" # Unikátny kľúč pre stabilitu
    )

# 4. LOGIKA VSTUPU
input_text = st.chat_input("Opýtaj sa na čokoľvek...")

# Tlačidlo sa ukáže len ak sú nahrané súbory
analyze_clicked = False
if uploaded_files:
    if st.button("✨ Vysvetli mi nahrané súbory"):
        analyze_clicked = True

if input_text or analyze_clicked:
    # Určenie textu
    prompt = input_text if input_text else "Prosím, vysvetli mi tieto súbory ako učiteľ."
    
    # Pridanie do histórie
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
        
        for m in st.session_state.messages[-6:]:
            payload.append(f"{m['role']}: {m['content']}")

        if uploaded_files:
            for f in uploaded_files:
                payload.append({'mime_type': f.type, 'data': f.getvalue()})

        success = False
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
                else:
                    st.error(f"Chyba: {e}")
                    break
        
        if not success:
            st.warning("⚠️ Prestávka na kávu. Skús o 30 sekúnd.")
            full_response = "Daj mi prosím chvíľku, o 30 sekúnd budem opäť pri tebe! ☕😊"

        container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Po odoslaní môžeme stránku refreshnúť, aby sa vyčistil nahrávač
        # st.rerun() 

with st.sidebar:
    if st.button("🗑️ Nová téma (Vymazať čet)"):
        st.session_state.messages = []
        st.rerun()
