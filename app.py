import streamlit as st

# 1. Konfigurácia
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# 2. CSS - TOTÁLNE VYSTRELENIE ŠÍPKY VON
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* SIVÁ LIŠTA */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        min-width: 260px !important;
    }

    /* ŠÍPKA - MUSÍ BYŤ VONKU Z LIŠTY */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        
        /* Fixná pozícia v bielom priestore aplikácie */
        position: fixed !important;
        left: 30px !important;  /* Toto ju udrží VŽDY 3 centimetre od ľavého okraja boxu */
        top: 30px !important;
        
        z-index: 1000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #ff4d4d !important; /* Červená, aby si ju videla */
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.2) !important;
        cursor: pointer !important;
    }

    /* Keď je lišta OTVORENÁ, šípka sa posunie doprava, aby nezavadzala v menu */
    section[data-testid="stSidebar"][aria-expanded="true"] + section [data-testid="collapsedControl"] {
        left: 280px !important; /* Skočí za okraj otvorenej lišty */
    }

    /* Odstúpime obsah, aby šípka nič neprekrývala */
    .block-container {
        padding-top: 80px !important;
        padding-left: 60px !important;
    }

    /* Červené tlačidlo */
    div.stButton > button {
        background-color: #ff4d4d !important;
        color: white !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("### 🎓 EduHub")
    st.selectbox("Jazyk", ["SK", "EN"])
    st.divider()
    if st.button("＋ Nový čet"):
        st.rerun()
    st.text_input("Hľadaj...", placeholder="Hľadaj...")
    st.divider()
    st.write("📁 💬 **AI Tutor**")

# 4. Hlavná plocha
st.title("🤖 AI Tutor")
st.chat_input("S čím dnes pomôžem?")
