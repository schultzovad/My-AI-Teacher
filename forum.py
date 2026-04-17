import streamlit as st

st.set_page_config(page_title="Fórum", layout="wide")

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
    "SK": {"title": "📚 Študijné materiály", "upload": "Nahraj svoje poznámky", "success": "Súbor nahraný!"},
    "EN": {"title": "📚 Study Materials", "upload": "Upload your notes", "success": "File uploaded!"},
    "DE": {"title": "📚 Lernmaterialien", "upload": "Notizen hochladen", "success": "Datei hochgeladen!"},
    "ES": {"title": "📚 Materiales de estudio", "upload": "Subir notas", "success": "¡Archivo subido!"},
    "FR": {"title": "📚 Matériels d'étude", "upload": "Télécharger vos notes", "success": "Fichier téléchargé !"},
    "IT": {"title": "📚 Materiali di studio", "upload": "Carica le tue note", "success": "File caricato!"},
    "UA": {"title": "📚 Навчальні матеріали", "upload": "Завантажте нотатки", "success": "Файл завантажено!"},
    "RU": {"title": "📚 Учебные материалы", "upload": "Загрузите заметки", "success": "Файл загружен!"}
}

query_params = st.query_params
selected_lang = query_params.get("lang", "SK")

if selected_lang not in lang_data:
    selected_lang = "SK"

t = lang_data[selected_lang]

with st.sidebar:
    st.write(f"🌐 {selected_lang}")

st.title(t["title"])
uploaded_file = st.file_uploader(t["upload"], type=['pdf', 'png', 'jpg'])
if uploaded_file:
    st.success(t["success"])
