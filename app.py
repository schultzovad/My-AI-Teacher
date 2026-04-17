import streamlit as st
import streamlit.components.v1 as components

# --- 1. NASTAVENIA ---
st.set_page_config(page_title="EduHub AI Tutor", layout="wide", page_icon="🎓")

# --- CSS PRE ŠÍPKU A VZHĽAD (Aby si ju mala vonku a videla ju) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* TVOJA ŠÍPKA - Vždy viditeľná vľavo hore */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        left: 20px !important;
        top: 20px !important;
        background-color: white !important;
        border: 2px solid #ff4d4d !important;
        border-radius: 50% !important;
        z-index: 999999 !important;
    }

    /* Plynulý scroll pri kliknutí na kotvu */
    html {
        scroll-behavior: smooth;
    }
    
    /* Štýl pre navigačné "tlačidlá", ktoré vyzerajú ako linky */
    .nav-link {
        display: block;
        padding: 10px;
        color: #31333F;
        text-decoration: none;
        background: #f0f2f6;
        border-radius: 8px;
        margin-bottom: 5px;
        text-align: center;
        font-weight: bold;
    }
    .nav-link:hover {
        background: #e0e2e6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SLOVNÍK ---
lang_data = {
    "SK": {"home": "🏠 Domov", "chat": "🤖 AI Tutor", "forum": "📚 Materiály", "groups": "👥 Skupiny", "input": "S čím ti dnes pomôžem?"},
    "EN": {"home": "🏠 Home", "chat": "🤖 AI Tutor", "forum": "📚 Materials", "groups": "👥 Groups", "input": "How can I help you?"}
}

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    lang = st.selectbox("Language", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    # Špeciálne HTML linky pre scroll namiesto st.button
    st.markdown(f'<a href="#ai-tutor" class="nav-link">{t["chat"]}</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="#forum" class="nav-link">{t["forum"]}</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="#groups" class="nav-link">{t["groups"]}</a>', unsafe_allow_html=True)
    
    st.divider()
    if st.button(t["home"], use_container_width=True):
        components.html("<script>window.parent.location.href = 'https://silent-terms-318372.framer.app/';</script>", height=0)

# --- 4. OBSAH POD SEBOU (Všetko na jednej stránke) ---

# --- SEKCIA: CHAT ---
st.markdown('<div id="ai-tutor"></div>', unsafe_allow_html=True) # KOTVA
st.title(t["chat"])
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(t["input"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        res = f"Odpoveď: {prompt}"
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})

st.divider() # Čiara medzi sekciami

# --- SEKCIA: FÓRUM ---
st.markdown('<div id="forum" style="padding-top: 50px;"></div>', unsafe_allow_html=True) # KOTVA
st.title(t["forum"])
st.file_uploader("Nahraj súbor", type=['pdf', 'png', 'jpg'])

st.divider()

# --- SEKCIA: SKUPINY ---
st.markdown('<div id="groups" style="padding-top: 50px;"></div>', unsafe_allow_html=True) # KOTVA
st.title(t["groups"])
st.text_input("Názov novej skupiny")
st.button("Vytvoriť")
