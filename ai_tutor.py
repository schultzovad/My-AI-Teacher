import streamlit as st

st.set_page_config(page_title="AI Tutor", layout="wide")

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

lang = st.sidebar.selectbox("Language / Jazyk", list(lang_data.keys()))
t = lang_data[lang]

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
