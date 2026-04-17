import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title("👥 Учебные группы")
n = st.text_input("Название новой группы")
if st.button("Создать группу"):
    st.balloons()
    st.success(f"Группа '{n}' создана!")
