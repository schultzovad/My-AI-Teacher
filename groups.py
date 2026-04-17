import streamlit as st

st.set_page_config(page_title="Študijné skupiny", layout="wide")
st.title("👥 Študijné skupiny")
nazov = st.text_input("Názov novej skupiny")
if st.button("Vytvoriť novú skupinu"):
    st.balloons()
    st.success(f"Skupina '{nazov}' vytvorená!")
