import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURÁCIA (VYNÚTENIE BOČNEJ LIŠTY) ---
st.set_page_config(
    page_title="EduHub", 
    layout="wide", 
    initial_sidebar_state="expanded" # Toto povie Streamlitu: "Vždy ukáž lištu!"
)

# --- 2. CSS OPRAVY PRE VIDITEĽNOSŤ ---
st.markdown("""
    <style>
    /* Skryje nepotrebné veci */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Vynútenie šírky bočnej lišty, aby ju Framer nezmenšil na nulu */
    [data-testid="stSidebar"] {
        min-width: 250px;
        max-width: 300px;
    }
    
    /* Odstránenie bielych okrajov okolo obsahu */
    .block-container {
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SLOVNÍK ---
lang_data = {
    "SK": {"h": "🏠 Domov", "c": "🤖 AI Tutor", "f": "📚 Študijné materiály", "g": "👥 Študijné skupiny", "i": "S čím ti dnes pomôžem?"},
    "EN": {"h": "🏠 Home", "c": "🤖 AI Tutor", "f": "📚 Study Materials", "g": "👥 Study Groups", "i": "How can I help you today?"}
}

# --- 4. BOČNÁ LIŠTA (SIDEBAR) ---
with st.sidebar:
    st.title("🎓 EduHub")
    lang = st.selectbox("Jazyk / Language", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    # Tlačidlo DOMOV
    if st.button(t["h"], use_container_width=True):
        moj_web = "https://silent-terms-318372.framer.app/"
        components.html(f"<script>window.top.location.href = '{moj_web}';</script>", height=0)
        st.stop()

    st.divider()
    page_selection = st.radio("Menu", [t["c"], t["f"], t["g"]])

# --- 5. OBSAH ---
if page_selection == t["c"]:
    st.title(t["c"])
    if "m" not in st.session_state: st.session_state.m = []
    for m in st.session_state.m:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if p := st.chat_input(t["i"]):
        st.session_state.m.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        res = "Analyzujem vaše zadanie..."
        with st.chat_message("assistant"): st.markdown(res)
        st.session_state.m.append({"role": "assistant", "content": res})

elif page_selection == t["f"]:
    st.title(t["f"])
    st.file_uploader("Nahraj súbor", type=['pdf', 'png', 'jpg'])

elif page_selection == t["g"]:
    st.title(t["g"])
    st.text_input("Názov novej skupiny")
    if st.button("Vytvoriť"): st.balloons()
