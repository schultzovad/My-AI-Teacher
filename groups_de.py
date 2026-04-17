import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title("👥 Studiengruppen")
n = st.text_input("Name der neuen Gruppe")
if st.button("Neue Gruppe erstellen"):
    st.balloons()
    st.success(f"Gruppe '{n}' erstellt!")
