import streamlit as st

st.set_page_config(page_title="Fórum", layout="wide")

lang_data = {
    "SK": {"title": "📚 Študijné materiály", "upload": "Nahraj svoje poznámky", "success": "Súbor nahraný!", "lang_sel": "Jazyk"},
    "EN": {"title": "📚 Study Materials", "upload": "Upload your notes", "success": "File uploaded!", "lang_sel": "Language"},
    "DE": {"title": "📚 Lernmaterialien", "upload": "Notizen hochladen", "success": "Datei hochgeladen!", "lang_sel": "Sprache"},
    "ES": {"title": "📚 Materiales de estudio", "upload": "Subir notas", "success": "¡Archivo subido!", "lang_sel": "Idioma"},
    "FR": {"title": "📚 Matériels d'étude", "upload": "Télécharger vos notes", "success": "Fichier téléchargé !", "lang_sel": "Langue"},
    "IT": {"title": "📚 Materiali di studio", "upload": "Carica le tue note", "success": "File caricato!", "lang_sel": "Lingua"},
    "UA": {"title": "📚 Навчальні матеріали", "upload": "Завантажте нотатки", "success": "Файл завантажено!", "lang_sel": "Мова"},
    "RU": {"title": "📚 Учебные материалы", "upload": "Загрузите заметки", "success": "Файл загружен!", "lang_sel": "Язык"}
}

if "lang" not in st.session_state:
    st.session_state.lang = "SK"

def change_lang():
    st.session_state.lang = st.session_state.new_lang_forum

st.sidebar.selectbox(
    lang_data[st.session_state.lang]["lang_sel"],
    list(lang_data.keys()),
    index=list(lang_data.keys()).index(st.session_state.lang),
    key="new_lang_forum",
    on_change=change_lang
)

t = lang_data[st.session_state.lang]
st.title(t["title"])
uploaded_file = st.file_uploader(t["upload"], type=['pdf', 'png', 'jpg'])
if uploaded_file:
    st.success(t["success"])
