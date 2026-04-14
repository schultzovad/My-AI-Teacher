import streamlit as st

# 1. Čistý základ, ktorý Streamlit pozná najlepšie
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# 2. CSS - Len farby a JEDNODUCHÝ posun šípky, aby nezmizla
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sivé pozadie lišty ako si mala na fotke */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
    }

    /* ŠÍPKA - Dáme ju na fixnú pozíciu, kde ju Framer nemôže zabiť */
    [data-testid="collapsedControl"] {
        left: 20px !important;
        top: 20px !important;
        background-color: white !important;
        border-radius: 50% !important;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.2) !important;
        z-index: 1000000 !important;
        display: flex !important;
    }
    
    /* Červené tlačidlo "Nový čet" */
    div.stButton > button {
        background-color: #ff4d4d !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Obsah lišty (to, čo si mala na fotkách)
with st.sidebar:
    st.markdown("### 🎓 EduHub")
    st.selectbox("Jazyk", ["SK", "EN"])
    st.divider()
    if st.button("＋ Nový čet"):
        st.rerun()
    st.text_input("Hľadaj...", placeholder="Hľadaj...")
    st.divider()
    st.radio("Menu", ["🏠 Domov", "📚 Materiály", "👥 Skupiny"])

# 4. Hlavná plocha
st.title("🤖 AI Tutor")
st.chat_input("S čím pomôžem?")
