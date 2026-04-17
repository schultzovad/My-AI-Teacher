import streamlit as st

st.set_page_config(page_title="Skupiny", layout="wide")

lang_data = {
    "SK": {"title": "👥 Študijné skupiny", "create": "Vytvoriť novú skupinu", "name_label": "Názov novej skupiny", "lang_sel": "Jazyk"},
    "EN": {"title": "👥 Study Groups", "create": "Create new group", "name_label": "New group name", "lang_sel": "Language"},
    "DE": {"title": "👥 Studiengruppen", "create": "Neue Gruppe erstellen", "name_label": "Name der neuen Gruppe", "lang_sel": "Sprache"},
    "ES": {"title": "👥 Grupos de estudio", "create": "Crear nuevo grupo", "name_label": "Nombre del nuevo grupo", "lang_sel": "Idioma"},
    "FR": {"title": "👥 Groupes d'étude", "create": "Créer un nouveau groupe", "name_label": "Nom du nouveau groupe", "lang_sel": "Langue"},
    "IT": {"title": "👥 Gruppi di studio", "create": "Crea nuovo grupo", "name_label": "Nome del nuovo gruppo", "lang_sel": "Lingua"},
    "UA": {"title": "👥 Навчальні групи", "create": "Створити нову групу", "name_label": "Назва нової групи", "lang_sel": "Мова"},
    "RU": {"title": "👥 Учебные группы", "create": "Создать новую группу", "name_label": "Название новой группы", "lang_sel": "Язык"}
}

if "lang" not in st.session_state:
    st.session_state.lang = "SK"

st.session_state.lang = st.sidebar.selectbox(
    lang_data[st.session_state.lang]["lang_sel"], 
    list(lang_data.keys()), 
    index=list(lang_data.keys()).index(st.session_state.lang)
)

t = lang_data[st.session_state.lang]

st.title(t["title"])
# Tu je opravený aj label pre textový vstup
nazov = st.text_input(t["name_label"])
if st.button(t["create"]):
    st.balloons()
    st.success(f"{t['title']}: '{nazov}'")
