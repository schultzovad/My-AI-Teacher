import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURÁCIA ---
st.set_page_config(
    page_title="EduHub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS PRE BIELU LIŠTU A SPRÁVNU ŠÍPKU ---
st.markdown("""
    <style>
    /* Skryje nepotrebné lišty Streamlitu */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* VRÁTIME BIELU FARBU LIŠTY */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #e6e9ef;
        min-width: 250px !important;
    }

    /* OPRAVA ŠÍPKY - posunieme ju k okraju a zmeníme farbu */
    [data-testid="collapsedControl"] {
        top: 10px;
        left: 10px;
        background-color: white;
        border-radius: 50%;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
    }

    /* Čistý priestor pre obsah */
    .block-container {
        padding-top: 1rem;
    }
    
    /* Aby text v lište nebol biely (keďže pozadie je už biele) */
    [data-testid="stSidebar"] * {
        color: #31333F !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SLOVNÍK ---
lang_data = {
    "SK": {"h": "🏠 Domov", "c": "🤖 AI Tutor", "f": "📚 Materiály", "g": "👥 Skupiny", "i": "S čím ti dnes pomôžem?"},
    "EN": {"h": "🏠 Home", "c": "🤖 AI Tutor", "f": "📚 Materials", "g": "👥 Groups", "i": "How can I help you today?"}
}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    lang = st.selectbox("Language", list(lang_data.keys()))
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
