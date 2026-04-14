import streamlit as st

# 1. Konfigurácia
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# 2. CSS - AGRESÍVNE NASTAVENIE ŠÍPKY
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* SIVÁ LIŠTA */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        min-width: 260px !important;
    }

    /* TÁTO ŠÍPKA TI UŽ NEZMIZNE */
    [data-testid="collapsedControl"] {
        display: flex !important;      /* Vynúti zobrazenie */
        visibility: visible !important; /* Vynúti viditeľnosť */
        left: 20px !important;         /* Posun od kraja boxu vo Frameri */
        top: 20px !important;
        z-index: 1000001 !important;   /* Musí byť nad všetkým */
        background-color: white !important;
        border: 2px solid #ff4d4d !important; /* ČERVENÝ OKRAJ aby si ju hneď videla */
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3) !important;
    }

    /* Ak je lišta OTVORENÁ, šípka sa posunie kúsok doprava k jej okraju */
    section[data-testid="stSidebar"][aria-expanded="true"] + section [data-testid="collapsedControl"] {
        left: 230px !important;
    }

    /* Červené tlačidlo "Nový čet" */
    div.stButton > button {
        background-color: #ff4d4d !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Tvoj dizajn)
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
st.chat_input("S čím pomôžem?")
