import streamlit as st

st.set_page_config(page_title="Študijné materiály", layout="wide")
st.title("📚 Študijné materiály")
uploaded_file = st.file_uploader("Nahraj svoje poznámky", type=['pdf', 'png', 'jpg'])
if uploaded_file:
    st.success("Súbor bol úspešne nahraný!")
