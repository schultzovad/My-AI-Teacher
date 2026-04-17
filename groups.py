import streamlit as st

st.set_page_config(page_title="Skupiny", layout="wide")

lang_data = {
    "SK": {"title": "👥 Študijné skupiny", "create": "Vytvoriť novú skupinu", "name_label": "Názov novej skupiny", "lang_sel": "Jazyk", "menu": "Menu"},
    "EN": {"title": "👥 Study Groups", "create": "Create new group", "name_label": "New group name", "lang_sel": "Language", "menu": "Menu"},
    "DE": {"title": "👥 Studiengruppen", "create": "Neue Gruppe erstellen", "name_label": "Name der Gruppe", "lang_sel": "Sprache", "menu": "Menü"},
    "ES": {"title": "👥 Grupos de estudio", "create": "Crear nuevo grupo", "name_label": "Nombre del grupo", "lang_sel": "Idioma", "menu": "Menú"},
    "FR": {"title": "👥 Groupes d'étude", "create": "Créer un groupe", "name_label": "Nom du groupe", "lang_sel": "Langue", "menu": "Menu"},
    "IT": {"title": "👥 Gruppi di studio", "create": "Crea nuovo grupo", "name_label": "Nome del gruppo", "lang_sel": "Lingua", "menu": "Menu"},
    "UA": {"title": "👥 Навчальні групи", "create": "Створити групу", "name_label": "Назва групи", "lang_sel": "Мова", "menu": "Меню"},
    "RU": {"title": "👥 Учебные группы", "create": "Создать группу", "name_label": "Название группы", "lang_sel": "Язык", "menu": "Меню"}
}

if "lang" not in st.session_state:
    st.session_state.lang = "SK"

def change_lang():
    st.session_state.lang = st.session_state.new_lang_groups

# Vytvorenie sidebaru so šípkou
with st.sidebar:
    st.title(lang_data[st.session_state.lang]["menu"])
    st.selectbox(
        lang_data[st.session_state.lang]["lang_sel"],
        list(lang_data.keys()),
        index=list(lang_data.keys()).index(st.session_state.lang),
        key="new_lang_groups",
        on_change=change_lang
    )
    st.divider()

t = lang_data[st.session_state.lang]
st.title(t["title"])
nazov = st.text_input(t["name_label"])
if st.button(t["create"]):
    st.balloons()
    st.success(f"{t['title']}: '{nazov}'")
