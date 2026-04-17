import streamlit as st

# Nastavenie stránky a skrytie prvkov
st.set_page_config(page_title="AI Tutor", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    .main .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    </style>
    """, unsafe_allow_html=True)

# Dáta pre 8 jazykov
lang_data = {
    "SK": {"title": "🤖 AI Tutor", "input": "S čím ti dnes pomôžem?"},
    "EN": {"title": "🤖 AI Tutor", "input": "How can I help you today?"},
    "DE": {"title": "🤖 AI Tutor", "input": "Wie kann ich dir helfen?"},
    "ES": {"title": "🤖 Tutor AI", "input": "¿Cómo te puedo ayudar?"},
    "FR": {"title": "🤖 Tuteur IA", "input": "Comment puis-je vous aider ?"},
    "IT": {"title": "🤖 Tutor IA", "input": "Come posso aiutarti?"},
    "UA": {"title": "🤖 AI Тьютор", "input": "Чим я можу вам допомогти?"},
    "RU": {"title": "🤖 AI Тьютор", "input": "Чем я могу вам помочь?"}
}

# Získanie jazyka z URL (ak chýba, predvolí SK)
query_params = st.query_params
selected_lang = query_params.get("lang", "SK")

if selected_lang not in lang_data:
    selected_lang = "SK"

t = lang_data[selected_lang]

# Prázdny sidebar len pre šípku (ak ju chceš)
with st.sidebar:
    st.write(f"🌐 {selected_lang}")

st.title(t["title"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(t["input"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        response = f"Odpoveď: {prompt}"
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
