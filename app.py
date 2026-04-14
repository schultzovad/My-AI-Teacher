import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURÁCIA (Vynútenie otvorenej lišty) ---
st.set_page_config(
    page_title="EduHub", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CSS "ZVIDITEĽŇOVAČ" ---
st.markdown("""
    <style>
    /* Skryje Streamlit lišty */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* VYNÚTENIE FARBY BOČNEJ LIŠTY (Aby nebola biela na bielom) */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6 !important; /* Jemná sivá, aby si ju videla */
        visibility: visible !important;
        display: block !important;
        border-right: 1px solid #e6e9ef;
    }

    /* Zabezpečí, aby text v lište bol čierny a viditeľný */
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #31333F !important;
    }

    /* Odstránenie bielych okrajov */
    .block-container {
        padding-top: 1rem;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SLOVNÍK ---
lang_data = {
    "SK": {"h": "🏠 Domov", "c": "🤖 AI Tutor", "f": "📚 Materiály", "g": "👥 Skupiny", "i": "S čím ti dnes pomôžem?"},
    "EN": {"h": "🏠 Home", "c": "🤖 AI Tutor", "f": "📚 Materials", "g": "👥 Groups", "i": "How can I help you today?"}
}

# --- 4. SIDEBAR (TOTO JE TÁ LIŠTA) ---
with st.sidebar:
    st.markdown("### 🎓 EduHub Menu")
    lang = st.selectbox("Language", list(lang_data.keys()), key="lang_selector")
    t = lang_data[lang]
    st.divider()
    
    if st.button(t["h"], use_container_width=True):
        moj_web = "https://silent-terms-318372.framer.app/"
        components.html(f"<script>window.top.location.href = '{moj_web}';</script>", height=0)
        st.stop()

    st.divider()
    page = st.radio("Sekcia", [t["c"], t["f"], t["g"]])

# --- 5. OBSAH ---
if page == t["c"]:
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
else:
    st.title(page)
    st.write("Obsah sa pripravuje...")
