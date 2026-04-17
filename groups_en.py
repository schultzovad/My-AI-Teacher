import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

st.title("👥 Study Groups")
n = st.text_input("New group name")
if st.button("Create new group"):
    st.balloons()
    st.success(f"Group '{n}' created!")
