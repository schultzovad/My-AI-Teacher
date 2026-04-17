import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title("👥 Gruppi di studio")
n = st.text_input("Nome del nuovo gruppo")
if st.button("Crea gruppo"):
    st.balloons()
    st.success(f"Gruppo '{n}' creato!")
