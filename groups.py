import streamlit as st

st.set_page_config(page_title="Skupiny", layout="wide")

lang_data = {
    "SK": {"title": "👥 Študijné skupiny", "create": "Vytvoriť novú skupinu"},
    "EN": {"title": "👥 Study Groups", "create": "Create new group"},
    "DE": {"title": "👥 Studiengruppen", "create": "Neue Gruppe erstellen"},
    "ES": {"title": "👥 Grupos de estudio", "create": "Crear nuevo grupo"},
    "FR": {"title": "👥 Groupes d'étude", "create": "Créer un nouveau groupe"},
    "IT": {"title": "👥 Gruppi di studio", "create": "Crea nuovo gruppo"},
    "UA": {"title": "👥 Навчальні групи", "create": "Створити нову групу"},
    "RU": {"title": "👥 Учебные группы", "create": "Создать новую группу"}
}

lang = st.sidebar.selectbox("Language / Jazyk", list(lang_data.keys()))
t = lang_data[lang]

st.title(t["title"])
nazov = st.text_input("Name / Názov")
if st.button(t["create"]):
    st.balloons()
    st.success(f"Skupina '{nazov}' vytvorená!")
