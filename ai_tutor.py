import streamlit as st

st.set_page_config(page_title="AI Tutor", layout="wide")

lang_data = {
    "SK": {"title": "🤖 AI Tutor", "input": "S čím ti dnes pomôžem?", "lang_label": "Vyber jazyk"},
    "EN": {"title": "🤖 AI Tutor", "input": "How can I help you today?", "lang_label": "Select Language"},
    "DE": {"title": "🤖 AI Tutor", "input": "Wie kann ich dir helfen?", "lang_label": "Sprache wählen"},
    "ES": {"title": "🤖 Tutor AI", "input": "¿Cómo te puedo ayudar?", "lang_label": "Seleccionar idioma"},
    "FR": {"title": "🤖 Tuteur IA", "input": "Comment puis-je vous aider ?", "lang_label": "Choisir la langue"},
    "IT": {"title": "🤖 Tutor IA", "input": "Come posso aiutarti?", "lang_label": "Seleziona lingua"},
    "UA": {"title": "🤖 AI Тьютор", "input": "Чим я можу вам допомогти?", "lang_label": "Оберіть мову"},
    "RU": {"title": "🤖 AI Тьютор", "input": "Чем я могу вам помочь?", "lang_label": "Выберите язык"}
}

# Najprv vytvoríme sidebar, aby sme vedeli, aký jazyk je vybraný
# Použijeme dočasný kľúč, aby sme vedeli preložiť label
if "temp_lang" not in st.session_state:
    st.session_state.temp_lang = "SK"

selected_lang = st.sidebar.selectbox("Language / Jazyk / Sprache", list(lang_data.keys()), index=list(lang_data.keys()).index(st.session_state.temp_lang))
st.session_state.temp_lang = selected_lang

t = lang_data[selected_lang]

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
