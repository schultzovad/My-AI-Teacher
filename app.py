import streamlit as st

# --- 1. NASTAVENIA (Vynútenie otvorenia na úvod) ---
st.set_page_config(
    page_title="EduHub AI", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CSS - TOTO JE TO "KURA", ČO HĽADÁME ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* ŠÍPKA, KTORÁ BUDE VŽDY VONKU A VIDITEĽNÁ */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        left: 20px !important;    /* Posun od okraja, aby ju Framer nezhltol */
        top: 20px !important;
        background-color: #ffffff !important; /* Biela, aby svietila */
        border: 2px solid #31333F !important; /* Čierny okraj pre istotu */
        border-radius: 50% !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
        z-index: 999999 !important;
        width: 40px !important;
        height: 40px !important;
    }

    /* Keď je lišta OTVORENÁ, šípka sa posunie doprava, aby nezavadzala v menu */
    section[data-testid="stSidebar"][aria-expanded="true"] + section [data-testid="collapsedControl"] {
        left: 270px !important; 
    }

    /* Celý biely blok pre lištu */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #e6e9ef;
    }
    
    .block-container {
        padding-top: 4rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SLOVNÍK ---
lang_data = {
    "SK": {"t": "🤖 AI Tutor", "f": "📚 Materiály", "g": "👥 Skupiny", "i": "S čím pomôžem?"},
    "EN": {"t": "🤖 AI Tutor", "f": "📚 Materials", "g": "👥 Groups", "i": "How can I help?"}
}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎓 EduHub")
    lang = st.selectbox("Language", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    choice = st.radio("Menu", [t["t"], t["f"], t["g"]])

# --- 5. LOGIKA STRÁNOK ---
if choice == t["f"]:
    st.title(t["f"])
    st.file_uploader("Upload")
elif choice == t["g"]:
    st.title(t["g"])
    st.text_input("Názov skupiny")
else:
    st.title(t["t"])
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if p := st.chat_input(t["i"]):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        res = "Rozumiem."
        with st.chat_message("assistant"): st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
