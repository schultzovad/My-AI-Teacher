import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURÁCIA ---
st.set_page_config(
    page_title="EduHub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS PRE VIDITEĽNÚ ŠÍPKU A BIELU LIŠTU ---
st.markdown("""
    <style>
    /* Skryje nepotrebné veci */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* BIELA LIŠTA */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #e6e9ef;
    }

    /* ŠÍPKA (CONTROL), KTORÁ NEZMIZNE */
    [data-testid="collapsedControl"] {
        top: 20px !important;    /* Posun od horného okraja */
        left: 20px !important;   /* Posun od ľavého okraja (aby nebola v rohu) */
        display: flex !important;
        visibility: visible !important;
        background-color: #ffffff !important;
        border-radius: 50% !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important; /* Výrazný tieň */
        width: 40px !important;
        height: 40px !important;
        z-index: 999999 !important;
    }

    /* Ikona vo vnútri šípky (aby bola tmavá) */
    [data-testid="collapsedControl"] svg {
        fill: #31333F !important;
        width: 25px !important;
        height: 25px !important;
    }

    /* Farba textu v lište */
    [data-testid="stSidebar"] * {
        color: #31333F !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR OBSAH ---
with st.sidebar:
    st.markdown("## 🎓 EduHub Menu")
    lang = st.selectbox("Language / Jazyk", ["SK", "EN"])
    st.divider()
    
    page = st.radio("Sekcia", ["🤖 AI Tutor", "📚 Materiály", "👥 Skupiny"])
    
    st.divider()
    if st.button("🏠 Domov", use_container_width=True):
        moj_web = "https://silent-terms-318372.framer.app/"
        components.html(f"<script>window.top.location.href = '{moj_web}';</script>", height=0)

# --- 4. HLAVNÝ OBSAH ---
if page == "🤖 AI Tutor":
    st.title("🤖 AI Tutor")
    if "m" not in st.session_state: st.session_state.m = []
    for m in st.session_state.m:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if p := st.chat_input("S čím ti dnes pomôžem?"):
        st.session_state.m.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        res = "Analyzujem..."
        with st.chat_message("assistant"): st.markdown(res)
        st.session_state.m.append({"role": "assistant", "content": res})
else:
    st.title(page)
    st.write("Obsah sa pripravuje...")
