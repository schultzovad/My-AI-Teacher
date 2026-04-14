import streamlit as st

# 1. Vynútenie otvorenia
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# 2. CSS, ktoré tú šípku "vystrelí" do viditeľnej zóny
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* TOTO JE ONO: Posunie šípku tak, aby ju Framer neorezal */
    [data-testid="collapsedControl"] {
        left: 30px !important;    /* Posun doprava */
        top: 30px !important;     /* Posun dole */
        background-color: #ffffff !important;
        border: 2px solid #000000 !important; /* Čierny krúžok aby si ju videla */
        border-radius: 50% !important;
        display: flex !important;
        visibility: visible !important;
        z-index: 999999 !important;
        width: 40px !important;
        height: 40px !important;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🎓 EduHub Menu")
    st.radio("Navigácia", ["AI Tutor", "Materiály", "Skupiny"])

st.title("🤖 AI Tutor")
st.chat_input("S čím pomôžem?")
