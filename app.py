import streamlit as st

# 1. Čistá konfigurácia
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# 2. CSS, KTORÉ TÚ ŠÍPKU "PRIKLINCUJE" DO BIELÉHO PRIESTORU
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    /* SIVÁ LIŠTA */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        min-width: 260px !important;
    }

    /* ŠÍPKA - MUSÍ BYŤ VIDITEĽNÁ VŽDY A VŠADE */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        position: fixed !important;
        
        /* TOTO ju hodí do bieleho priestoru aplikácie */
        left: 40px !important; 
        top: 40px !important;
        
        z-index: 9999999 !important;
        background-color: #ffffff !important;
        border: 3px solid #ff4d4d !important; /* HRUBÝ ČERVENÝ OKRAJ */
        border-radius: 50% !important;
        width: 60px !important; /* EŠTE VÄČŠIA */
        height: 60px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important; /* OBROVSKÝ TIEŇ */
    }

    /* Červené tlačidlo "Nový čet" */
    div.stButton > button {
        background-color: #ff4d4d !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    
    /* Posunieme text aplikácie, aby ho šípka nezakrývala */
    .block-container {
        padding-top: 100px !important;
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

# 4. Obsah
st.title("🤖 AI Tutor")
st.write("Ak túto červenú šípku vľavo hore nevidíš, skús vo Frameri zväčšiť ten Embed box.")
st.chat_input("Skús mi niečo napísať...")
