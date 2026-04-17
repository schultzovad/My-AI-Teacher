import streamlit as st

st.set_page_config(page_title="Fórum", layout="wide")

lang_data = {
    "SK": {"title": "📚 Študijné materiály", "upload": "Nahraj svoje poznámky", "success": "Súbor bol úspešne nahraný!", "lang_label": "Vyber jazyk"},
    "EN": {"title": "📚 Study Materials", "upload": "Upload your notes", "success": "File uploaded successfully!", "lang_label": "Select Language"},
    "DE": {"title": "📚 Lernmaterialien", "upload": "Notizen hochladen", "success": "Datei erfolgreich hochgeladen!", "lang_label": "Sprache wählen"},
    "ES": {"title": "📚 Materiales de estudio", "upload": "Subir notas", "success": "¡Archivo subido con éxito!", "lang_label": "Seleccionar idioma"},
    "FR": {"title": "📚 Matériels d'étude", "upload": "Télécharger vos notes", "success": "Fichier téléchargé avec succès !", "lang_label": "Choisir la langue"},
    "IT": {"title": "📚 Materiali di studio", "upload": "Carica le tue note", "success": "File caricato con successo!", "lang_label": "Seleziona lingua"},
    "UA": {"title": "📚 Навчальні матеріали", "upload": "Завантажте свої нотатки", "success": "Файл успішно завантажено!", "lang_label": "Оберіть мову"},
    "RU": {"title": "📚 Учебные материалы", "upload": "Загрузите свои заметки", "success": "Файл успешно загружен!", "lang_label": "Выберите язык"}
}

selected_lang = st.sidebar.selectbox("Language / Jazyk", list(lang_data.keys()))
t = lang_data[selected_lang]

st.title(t["title"])
uploaded_file = st.file_uploader(t["upload"], type=['pdf', 'png', 'jpg'])
if uploaded_file:
    st.success(t["success"])
