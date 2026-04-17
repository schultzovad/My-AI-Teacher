import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

st.title("👥 Študijné skupiny")
n = st.text_input("Názov novej skupiny")
if st.button("Vytvoriť novú skupinu"):
    st.balloons()
    st.success(f"Skupina '{n}' vytvorená!")
