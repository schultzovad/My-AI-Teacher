import streamlit as st
from streamlit_option_menu import option_menu

# --- KONFIGURÁCIA ---
st.set_page_config(page_title="EduHub", layout="wide", initial_sidebar_state="expanded")

# --- CSS PRE VYSUNUTÚ ŠÍPKU A VZHĽAD ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ŠÍPKA, KTORÁ NEZMIZNE */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        left: 30px !important; 
        top: 30px !important;
        background-color: white !important;
        border: 1px solid #ddd !important;
        border-radius: 50% !important;
        z-index: 999999 !important;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1) !important;
    }

    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
    }
    
    /* Červené tlačidlo */
    div.stButton > button {
        background-color: #ff4d4d !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR S TVOJÍM DIZAJNOM ---
with st.sidebar:
    st.markdown("🌐 **Jazyk**")
    lang = st.selectbox("", ["SK", "EN"], label_visibility="collapsed")
    
    st.markdown("<br>📁 💬 **AI Tutor**", unsafe_allow_html=True)
    
    if st.button("＋ Nový čet"):
        st.rerun()

    selected = option_menu(
        menu_title=None,
        options=["Čety", "Nastavenia"],
        icons=["chat", "gear"],
        default_index=0,
    )

# --- OBSAH ---
st.title("🤖 AI Tutor")
st.divider()
st.chat_input("S čím pomôžem?")
