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

# 2. HISTÓRIA ČETU
st.title("🎓 Tvoj osobný AI učiteľ")
st.caption("Nahraj fotku poznámok alebo sa čokoľvek opýtaj. Vysvetlím ti to polopatě!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.write("---")

# 3. SPODNÝ PANEL (Vždy viditeľný pri písaní)
with st.container():
    uploaded_files = st.file_uploader(
        "Prilož poznámky alebo fotku príkladu", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

if prompt := st.chat_input("Opýtaj sa na čokoľvek..."):
    process_input = True
elif uploaded_files and st.button("✨ Vysvetli mi nahrané súbory"):
    process_input = True
    prompt = "Prosím, vysvetli mi tieto poznámky ako učiteľ a ak sú tam príklady, vyrieš ich."
else:
    process_input = False

# 4. LOGIKA UČITEĽA
if process_input:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        container = st.empty()
        payload = []
        
        # OSOBNOSŤ UČITEĽA: Milý, ľudský, ale odborný
        teacher_prompt = """
        Si skúsený, milý a trpezlivý učiteľ v škole. Tvojou úlohou nie je robiť 'analýzu', ale 'vysvetľovať' učivo.
        
        PRAVIDLÁ:
        1. Buď povzbudivý a používaj milý tón (napr. 'Pozrime sa na to spolu', 'To je skvelá otázka').
        2. Ak sú na fotkách príklady, najprv ich vypočítaj krok po kroku a potom jemne vysvetli logiku.
        3. Ak sú tam poznámky, vysvetli ich jednoducho a zrozumiteľne, ako keby si doučoval obľúbeného žiaka.
        4. NIKDY nemeň správnosť faktov. Odbornosť musí byť 100%.
        5. Odpovedaj v jazyku, ktorý používa žiak (slovenčina).
        """
        payload.append(teacher_prompt)
        
        # Pridanie histórie pre kontext
        for m in st.session_state.messages[-6:]:
            payload.append(f"{m['role']}: {m['content']}")

        # Pridanie súborov
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
                    st.error(f"Technická chybička: {e}")
                    break
        
        if not success:
            st.warning("⚠️ Naši učitelia majú práve krátku prestávku na kávu.")
            full_response = "Prepáč, trošku som sa zamotal v limitoch. Skús mi túto otázku poslať ešte raz o 30 sekúnd, budem pripravený! 😊☕"

        container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with st.sidebar:
    if st.button("🗑️ Nová téma (Vymazať čet)"):
        st.session_state.messages = []
        st.rerun()
