import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title("👥 Навчальні групи")
n = st.text_input("Назва нової групи")
if st.button("Створити груpu"):
    st.balloons()
    st.success(f"Група '{n}' створена!")
