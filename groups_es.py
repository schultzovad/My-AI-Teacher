import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title("📚 Materiales de estudio")
up = st.file_uploader("Sube tus notas", type=['pdf', 'png', 'jpg'])
if up: st.success("¡Archivo subido con éxito!")
