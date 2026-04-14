import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURÁCIA ---
st.set_page_config(
    page_title="EduHub", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CSS "SILNÁ RUKA" (VYNÚTENIE LIŠTY) ---
st.markdown("""
    <style>
    /* Skryje nepotrebné prvky */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* TOTO VYNÚTI ZOBRAZENIE LIŠTY AJ V MALOM EMBED BOXE */
    [data-testid="stSidebar"] {
        visibility: visible !important;
        display: block !important;
        min-width: 250px !important;
    }
    
    /* Odstráni tlačidlo na schovávanie lišty, aby sa náhodou nezavrela */
    [data-testid="collapsedControl"] {
        display: none;
    }

    .block-container {
        padding-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SLOVNÍK ---
lang_data = {
    "SK": {"h": "🏠 Domov", "c": "🤖 AI Tutor", "f": "📚 Študijné materiály", "g": "👥 Študijné skupiny", "i": "S čím ti dnes pomôžem?"},
    "EN": {"h": "🏠 Home", "c": "🤖 AI Tutor", "f": "📚 Study Materials", "g": "👥 Study Groups", "i": "How can I help you today?"}
}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎓 EduHub")
    lang = st.selectbox("Language", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
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
        res = "Analyzujem..."
        with st.chat_message("assistant"): st.markdown(res)
        st.session_state.m.append({"role": "assistant", "content": res})

elif page_selection == t["f"]:
    st.title(t["f"])
    st.file_uploader("Upload")

elif page_selection == t["g"]:
    st.title(t["g"])
    st.text_input("Group Name")
