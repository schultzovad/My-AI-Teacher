import streamlit as st

st.set_page_config(page_title="Fórum", layout="wide")

lang_data = {
    "SK": {"title": "📚 Študijné materiály", "upload": "Nahraj svoje poznámky", "success": "Súbor bol úspešne nahraný!", "lang_sel": "Jazyk"},
    "EN": {"title": "📚 Study Materials", "upload": "Upload your notes", "success": "File uploaded successfully!", "lang_sel": "Language"},
    "DE": {"title": "📚 Lernmaterialien", "upload": "Notizen hochladen", "success": "Datei erfolgreich hochgeladen!", "lang_sel": "Sprache"},
    "ES": {"title": "📚 Materiales de estudio", "upload": "Subir notas", "success": "¡Archivo subido con éxito!", "lang_sel": "Idioma"},
    "FR": {"title": "📚 Matériels d'étude", "upload": "Télécharger vos notes", "success": "Fichier téléchargé avec succès !", "lang_sel": "Langue"},
    "IT": {"title": "📚 Materiali di studio", "upload": "Carica le tue note", "success": "File caricato con successo!", "lang_sel": "Lingua"},
    "UA": {"title": "📚 Навчальні матеріали", "upload": "Завантажте свої нотатки", "success": "Файл успішно завантажено!", "lang_sel": "Мова"},
    "RU": {"title": "📚 Учебные материалы", "upload": "Загрузите свои заметки", "success": "Файл успешно загружен!", "lang_sel": "Язык"}
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
uploaded_file = st.file_uploader(t["upload"], type=['pdf', 'png', 'jpg'])
if uploaded_file:
    st.success(t["success"])
