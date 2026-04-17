import streamlit as st

st.set_page_config(page_title="AI Tutor", layout="wide")
st.title("🤖 AI Tutor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("S čím ti dnes pomôžem?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        res = f"Odpoveď: {prompt}"
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
