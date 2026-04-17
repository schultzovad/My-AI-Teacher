import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title("📚 Materiali didattici")
up = st.file_uploader("Carica i tuoi appunti", type=['pdf', 'png', 'jpg'])
if up: st.success("File caricato con successo!")
