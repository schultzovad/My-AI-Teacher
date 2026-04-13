import streamlit as st
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="AI Tutor Pro", layout="centered", page_icon="🎓")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Chýba API kľúč v Secrets!")

AVAILABLE_MODELS = ['gemini-flash-latest', 'gemini-2.0-flash', 'gemini-pro-latest']

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. ZOBRAZENIE HISTÓRIE ČETU (Hore)
st.title("🎓 AI Tutor")
st.caption("Nahraj súbory a pýtaj sa, alebo len pošli fotku príkladov.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. SPODNÁ ČASŤ - NAHRÁVANIE A TEXT (Dole pod četom)
st.write("---") # Oddelovacia čiara

# Kontajner pre nahrávanie súborov - bude sa posúvať s četom
with st.container():
    uploaded_files = st.file_uploader(
        "Prilož súbory (fotky, PDF)", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

# Četové pole
if prompt := st.chat_input("Napíš správu..."):
    # Spracovanie, ak máme text alebo súbory
    process_input = True
elif uploaded_files and not st.session_state.get('last_uploaded') == uploaded_files:
    # Ak sú nahrané nové súbory, ale nie je text, môžeme pridať tlačidlo alebo 
    # v tomto prípade použijeme fintu - ak užívateľ stlačí Enter v prázdnom poli
    process_input = False 
else:
    process_input = False

# Špeciálne tlačidlo pre prípady, keď chceš poslať LEN súbory bez písania
if uploaded_files:
    if st.button("🚀 Odoslať len prílohy"):
        process_input = True
        prompt = "Analyzuj tieto priložené súbory a vyrieš úlohy, ktoré na nich uvidíš."

# 4. LOGIKA SPRACOVANIA
if process_input and (prompt or uploaded_files):
    
    # Pridáme správu do histórie
    display_text = prompt if prompt else "📎 (Odoslané prílohy na analýzu)"
    st.session_state.messages.append({"role": "user", "content": display_text})
    
    # Vymažeme vizuálne súbory pre ďalšie kolo (voliteľné)
    # st.rerun() by tu mohlo pomôcť, ale skúsme najprv plynulý beh
    
    with st.chat_message("user"):
        st.markdown(display_text)

    with st.chat_message("assistant"):
        container = st.empty()
        payload = []
        
        # Inštrukcie pre okamžité riešenie príkladov
        payload.append("""
        Si expert AI Tutor. Tvojou prioritou je:
        1. Ak sú v prílohách príklady alebo úlohy, okamžite ich VYRIEŠ krok po kroku.
        2. Ak je priložený text, zhrň ho.
        3. Odpovedaj vždy v jazyku, v ktorom sú poznámky alebo otázka.
        """)
        
        # Pridanie histórie
        for m in st.session_state.messages[-8:]:
            payload.append(f"{m['role']}: {m['content']}")

        # Pridanie súborov
        if uploaded_files:
            for f in uploaded_files:
                payload.append({'mime_type': f.type, 'data': f.getvalue()})

        success = False
        for model_name in AVAILABLE_MODELS:
            if success: break
            try:
                with st.spinner('Počítam a premýšľam...'):
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
            st.warning("⚠️ Učitelia majú pauzu. Skús to o 30 sekúnd.")
            full_response = "Prepáč, momentálne som preťažený. Skús to prosím o chvíľu znova! ☕"

        container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Zabezpečíme, aby sa stránka obnovila a nahrávač sa vyčistil (ak chceš)
        # st.rerun() 

# Bočná lišta ostane len na nastavenia
with st.sidebar:
    if st.button("🗑️ Vymazať konverzáciu"):
        st.session_state.messages = []
        st.rerun()
