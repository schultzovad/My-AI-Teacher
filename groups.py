import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

lang_data = {
    "SK": {"title": "👥 Študijné skupiny", "label": "Názov skupiny", "btn": "Vytvoriť"},
    "EN": {"title": "👥 Study Groups", "label": "Group name", "btn": "Create"},
    "DE": {"title": "👥 Studiengruppen", "label": "Name", "btn": "Erstellen"},
    "ES": {"title": "👥 Grupos", "label": "Nombre", "btn": "Crear"},
    "FR": {"title": "👥 Groupes", "label": "Nom", "btn": "Créer"},
    "IT": {"title": "👥 Gruppi", "label": "Nome", "btn": "Crea"},
    "UA": {"title": "👥 Групи", "label": "Назва", "btn": "Створити"},
    "RU": {"title": "👥 Группы", "label": "Название", "btn": "Создать"}
}

L = st.query_params.get("lang", "SK")
t = lang_data.get(L, lang_data["SK"])

st.title(t["title"])
n = st.text_input(t["label"])
if st.button(t["btn"]):
    st.balloons()
    st.success(f"{t['title']}: '{n}'")
