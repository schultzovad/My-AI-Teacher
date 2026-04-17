import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title("📚 Навчальні матеріали")
up = st.file_uploader("Завантажте свої нотатки", type=['pdf', 'png', 'jpg'])
if up: st.success("Файл успішно завантажено!")
