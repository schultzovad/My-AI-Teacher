import streamlit as st

st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

lang_data = {
    "SK": {"title": "🤖 AI Tutor", "input": "S čím ti dnes pomôžem?"},
    "EN": {"title": "🤖 AI Tutor", "input": "How can I help you?"},
    "DE": {"title": "🤖 AI Tutor", "input": "Wie kann ich helfen?"},
    "ES": {"title": "🤖 Tutor AI", "input": "¿Cómo te ayudo?"},
    "FR": {"title": "🤖 Tuteur IA", "input": "Comment aider ?"},
    "IT": {"title": "🤖 Tutor IA", "input": "Come posso aiutarti?"},
    "UA": {"title": "🤖 AI Тьютор", "input": "Чим допомогти?"},
    "RU": {"title": "🤖 AI Тьютор", "input": "Чем помочь?"}
}

# Prečítanie jazyka z URL
q = st.query_params
L = q.get("lang", "SK")
t = lang_data.get(L, lang_data["SK"])

st.title(t["title"])
if "m" not in st.session_state: st.session_state.m = []
for m in st.session_state.m:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input(t["input"]):
    st.session_state.m.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"):
        res = f"Odpoveď: {p}"
        st.markdown(res)
    st.session_state.m.append({"role": "assistant", "content": res})
