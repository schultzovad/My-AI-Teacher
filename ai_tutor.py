import streamlit as st

st.set_page_config(page_title="AI Tutor", layout="wide")

lang_data = {
    "SK": {"title": "🤖 AI Tutor", "input": "S čím ti dnes pomôžem?", "lang_sel": "Jazyk"},
    "EN": {"title": "🤖 AI Tutor", "input": "How can I help you today?", "lang_sel": "Language"},
    "DE": {"title": "🤖 AI Tutor", "input": "Wie kann ich dir helfen?", "lang_sel": "Sprache"},
    "ES": {"title": "🤖 Tutor AI", "input": "¿Cómo te puedo ayudar?", "lang_sel": "Idioma"},
    "FR": {"title": "🤖 Tuteur IA", "input": "Comment puis-je vous aider ?", "lang_sel": "Langue"},
    "IT": {"title": "🤖 Tutor IA", "input": "Come posso aiutarti?", "lang_sel": "Lingua"},
    "UA": {"title": "🤖 AI Тьютор", "input": "Чим я можу вам допомогти?", "lang_sel": "Мова"},
    "RU": {"title": "🤖 AI Тьютор", "input": "Чем я могу вам помочь?", "lang_sel": "Язык"}
}

# Inicializácia
if "lang" not in st.session_state:
    st.session_state.lang = "SK"

# Funkcia na okamžitú zmenu
def change_lang():
    st.session_state.lang = st.session_state.new_lang_selection

# Dynamický výber jazyka v sidebare
st.sidebar.selectbox(
    lang_data[st.session_state.lang]["lang_sel"],
    list(lang_data.keys()),
    index=list(lang_data.keys()).index(st.session_state.lang),
    key="new_lang_selection",
    on_change=change_lang
)

t = lang_data[st.session_state.lang]

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
