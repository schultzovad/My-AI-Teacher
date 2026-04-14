import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURÁCIA ---
st.set_page_config(
    page_title="EduHub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS - ŠÍPKA VON Z LIŠTY ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp { background-color: white; }

    /* ŠÍPKA - POSUNUTÁ ÚPLNE MIMO LIŠTU */
    [data-testid="collapsedControl"] {
        top: 30px !important;
        left: 280px !important; /* TOTO ju vystrelí von z lišty (lišta má cca 250px) */
        display: flex !important;
        visibility: visible !important;
        background-color: #ffffff !important;
        border: 2px solid #000000 !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        z-index: 999999 !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3) !important;
    }

    /* Keď je lišta ZATVORENÁ, šípka sa vráti na viditeľné miesto pri kraji */
    section[data-testid="stSidebar"][aria-expanded="false"] + section [data-testid="collapsedControl"] {
        left: 30px !important;
    }

    /* Vzhľad bočnej lišty */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #e6e9ef;
    }

    /* Úprava obsahu aby nezavadzal */
    .block-container {
        padding-top: 50px !important;
        padding-left: 80px !important;
    }
    
    [data-testid="stSidebar"] * { color: #31333F !important; }
    [data-testid="collapsedControl"] svg { fill: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    lang = st.selectbox("Language", ["SK", "EN"])
    st.divider()
    page = st.radio("Sekcia", ["🤖 AI Tutor", "📚 Materiály", "👥 Skupiny"])
    st.divider()
    if st.button("🏠 Domov", use_container_width=True):
        components.html("<script>window.top.location.href='https://silent-terms-318372.framer.app/'</script>", height=0)

# --- 4. OBSAH ---
st.title(page)
if page == "🤖 AI Tutor":
    if "m" not in st.session_state: st.session_state.m = []
    for m in st.session_state.m:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if p := st.chat_input("S čím ti dnes pomôžem?"):
        st.session_state.m.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        res = "Analyzujem..."
        with st.chat_message("assistant"): st.markdown(res)
        st.session_state.m.append({"role": "assistant", "content": res})
