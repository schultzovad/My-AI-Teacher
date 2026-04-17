import streamlit as st

st.set_page_config(page_title="Skupiny", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    .main .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    </style>
    """, unsafe_allow_html=True)

lang_data = {
    "SK": {"title": "👥 Študijné skupiny", "create": "Vytvoriť novú skupinu", "name_label": "Názov novej skupiny"},
    "EN": {"title": "👥 Study Groups", "create": "Create new group", "name_label": "New group name"},
    "DE": {"title": "👥 Studiengruppen", "create": "Neue Gruppe erstellen", "name_label": "Name der Gruppe"},
    "ES": {"title": "👥 Grupos de estudio", "create": "Crear nuevo grupo", "name_label": "Nombre del grupo"},
    "FR": {"title": "👥 Groupes d'étude", "create": "Créer un groupe", "name_label": "Nom du groupe"},
    "IT": {"title": "👥 Gruppi di studio", "create": "Crea nuovo grupo", "name_label": "Nome del gruppo"},
    "UA": {"title": "👥 Навчальні групи", "create": "Створити групу", "name_label": "Назва групи"},
    "RU": {"title": "👥 Учебные группы", "create": "Создать группу", "name_label": "Название группы"}
}

query_params = st.query_params
selected_lang = query_params.get("lang", "SK")

if selected_lang not in lang_data:
    selected_lang = "SK"

t = lang_data[selected_lang]

with st.sidebar:
    st.write(f"🌐 {selected_lang}")

st.title(t["title"])
nazov = st.text_input(t["name_label"])
if st.button(t["create"]):
    st.balloons()
    st.success(f"{t['title']}: '{nazov}'")
