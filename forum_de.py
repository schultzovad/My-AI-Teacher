import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title("📚 Lernmaterialien")
up = st.file_uploader("Laden Sie Ihre Notizen hoch", type=['pdf', 'png', 'jpg'])
if up: st.success("Datei erfolgreich hochgeladen!")
