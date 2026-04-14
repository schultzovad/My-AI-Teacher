import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURÁCIA ---
st.set_page_config(
    page_title="EduHub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS PRE MAXIMÁLNU VIDITEĽNOSŤ ŠÍPKY ---
st.markdown("""
    <style>
    /* Skryje prebytočný balast */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* CELÉ POZADIE STRÁNKY */
    .stApp {
        background-color: white;
    }

    /* ŠÍPKA (VYSÚVACÍ PRVOK) - POSUNUTÁ PORIADNE DOVNÚTRA */
    [data-testid="collapsedControl"] {
        top: 40px !important;    /* Viac miesta zhora */
        left: 40px !important;   /* Viac miesta zľava - teraz už musí byť v zábere */
        display: flex !important;
        visibility: visible !important;
        background-color: #f0f2f6 !important; /* Jemne sivá, aby "svietila" na bielom */
        border: 2px solid #31333F !important; /* Čierny okraj, aby bola jasne ohraničená */
        border-radius: 10px !important;       /* Zaoblený štvorec/obdĺžnik */
        width: 50px !important;
        height: 50px !important;
        z-index: 999999 !important;
        cursor: pointer !important;
    }

    /* HLAVNÝ OBSAH POSUNIEME, ABY ŠÍPKA DOŇHO NEZASAHOVALA */
    .block-container {
        padding-top: 80px !important; /* Vytvorí priestor pod šípkou */
        padding-left: 50px !important;
    }

    /* BIELA BOČNÁ LIŠTA */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #e6e9ef;
    }

    /* Farba textu a ikony */
    [data-testid="stSidebar"] * { color: #31333F !important; }
    [data-testid="collapsedControl"] svg { fill: #31333F !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🎓 EduHub Menu")
    lang = st.selectbox("Language / Jazyk", ["SK", "EN"])
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
