import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title("🤖 AI Tutor")
if "msg" not in st.session_state: st.session_state.msg = []
for m in st.session_state.msg:
    with st.chat_message(m["role"]): st.markdown(m["content"])
if p := st.chat_input("How can I help you today?"):
    st.session_state.msg.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"):
        res = f"Response: {p}"
        st.markdown(res)
    st.session_state.msg.append({"role": "assistant", "content": res})
