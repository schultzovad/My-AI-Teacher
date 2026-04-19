import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

lang_data = {
    "SK": {"title": "📚 Študijné materiály", "up": "Nahraj svoje poznámky", "ok": "Súbor nahraný!"},
    "EN": {"title": "📚 Study Materials", "up": "Upload your notes", "ok": "File uploaded!"},
    "DE": {"title": "📚 Lernmaterialien", "up": "Notizen hochladen", "ok": "Datei hochgeladen!"},
    "ES": {"title": "📚 Materiales", "up": "Subir notas", "ok": "¡Archivo subido!"},
    "FR": {"title": "📚 Matériels", "up": "Télécharger", "ok": "Fichier téléchargé !"},
    "IT": {"title": "📚 Materiali", "up": "Carica note", "ok": "File caricato!"},
    "UA": {"title": "📚 Навчальні мат.", "up": "Завантажити", "ok": "Файл завантажено!"},
    "RU": {"title": "📚 Учебные мат.", "up": "Загрузить", "ok": "Файл загружен!"}
}

L = st.query_params.get("lang", "SK")
t = lang_data.get(L, lang_data["SK"])

st.title(t["title"])
u = st.file_uploader(t["up"], type=['pdf', 'png', 'jpg'])
if u: st.success(t["ok"])
