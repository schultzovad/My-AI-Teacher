import streamlit as st

st.set_page_config(page_title="Skupiny", layout="wide")

lang_data = {
    "SK": {"title": "👥 Študijné skupiny", "create": "Vytvoriť novú skupinu", "name_label": "Názov novej skupiny", "lang_label": "Vyber jazyk"},
    "EN": {"title": "👥 Study Groups", "create": "Create new group", "name_label": "New group name", "lang_label": "Select Language"},
    "DE": {"title": "👥 Studiengruppen", "create": "Neue Gruppe erstellen", "name_label": "Name der neuen Gruppe", "lang_label": "Sprache wählen"},
    "ES": {"title": "👥 Grupos de estudio", "create": "Crear nuevo grupo", "name_label": "Nombre del nuevo grupo", "lang_label": "Seleccionar idioma"},
    "FR": {"title": "👥 Groupes d'étude", "create": "Créer un nouveau groupe", "name_label": "Nom du nouveau groupe", "lang_label": "Choisir la langue"},
    "IT": {"title": "👥 Gruppi di studio", "create": "Crea nuovo grupo", "name_label": "Nome del nuovo gruppo", "lang_label": "Seleziona lingua"},
    "UA": {"title": "👥 Навчальні групи", "create": "Створити ноvu групу", "name_label": "Назва нової групи", "lang_label": "Оберіть мову"},
    "RU": {"title": "👥 Учебные группы", "create": "Создать новую группу", "name_label": "Название новой группы", "lang_label": "Выберите язык"}
}

selected_lang = st.sidebar.selectbox("Language / Jazyk", list(lang_data.keys()))
t = lang_data[selected_lang]

st.title(t["title"])
nazov = st.text_input(t["name_label"])
if st.button(t["create"]):
    st.balloons()
    st.success(f"{t['title']}: '{nazov}'")
