import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)
st.title("👥 Groupes d'étude")
n = st.text_input("Nom du nouveau groupe")
if st.button("Créer un groupe"):
    st.balloons()
    st.success(f"Groupe '{n}' créé !")
