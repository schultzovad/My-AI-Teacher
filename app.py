import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURÁCIA (VŽDY OTVORENÁ LIŠTA) ---
st.set_page_config(
    page_title="EduHub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS - ŽIADNE SKRÝVANIE, LEN FARBY ---
st.markdown("""
    <style>
    /* Vynútime, aby bočná lišta bola VŽDY viditeľná a mala farbu */
    [data-testid="stSidebar"] {
        background-color: #2E3440 !important; /* Tmavomodrá/Sivá farba */
        min-width: 250px !important;
        visibility: visible !important;
        display: block !important;
    }
    
    /* Text v lište bude biely, aby bol vidieť na tmavom pozadí */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Zrušíme to podozrivé skrývanie hlavičky, aby sme videli všetko */
    header { visibility: visible !important; background: rgba(255,255,255,0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. OBSAH LIŠTY ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    lang = st.selectbox("Language", ["SK", "EN"])
    st.divider()
    page = st.radio("Sekcia", ["🤖 AI Tutor", "📚 Materiály", "👥 Skupiny"])
    
    if st.button("🏠 Domov", use_container_width=True):
        moj_web = "https://silent-terms-318372.framer.app/"
        components.html(f"<script>window.top.location.href = '{moj_web}';</script>", height=0)

# --- 4. HLAVNÝ OBSAH ---
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
