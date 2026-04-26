import streamlit as st

# 1. NASTAVENIE STRÁNKY A ŠTÝLOV
st.set_page_config(layout="wide", page_title="Študovňa")
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;} 
    .stAppDeployButton {display:none;}
    iframe {border-radius: 15px; border: 1px solid #ddd; background-color: white;}
    .stButton>button {border-radius: 10px; font-weight: 500;}
    /* Červené tlačidlo pre nahrávanie, aby svietilo */
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 2. KOMPLETNÉ PREKLADY (8 JAZYKOV)
lang_data = {
    "SK": {"title": "📚 Študijné materiály", "up": "Nahraj svoje poznámky", "ok": "Súbor nahraný!", "bio": "Biológia", "dej": "Dejepis", "fyz": "Fyzika", "che": "Chémia", "mat": "Matematika", "obn": "Občianska náuka", "geo": "Geografia", "inf": "Informatika", "sjl": "Slovenčina", "anj": "Angličtina", "nej": "Nemčina", "frj": "Francúzština", "esp": "Španielčina", "itj": "Taliančina", "ruj": "Ruština", "ukj": "Ukrajinčina"},
    "EN": {"title": "📚 Study Materials", "up": "Upload your notes", "ok": "File uploaded!", "bio": "Biology", "dej": "History", "fyz": "Physics", "che": "Chemistry", "mat": "Mathematics", "obn": "Civics", "geo": "Geography", "inf": "Informatics", "sjl": "Slovak", "anj": "English", "nej": "German", "frj": "French", "esp": "Spanish", "itj": "Italian", "ruj": "Russian", "ukj": "Ukrainian"},
    "DE": {"title": "📚 Lernmaterialien", "up": "Notizen hochladen", "ok": "Datei hochgeladen!", "bio": "Biologie", "dej": "Geschichte", "fyz": "Physik", "che": "Chemie", "mat": "Mathematik", "obn": "Sozialkunde", "geo": "Geographie", "inf": "Informatik", "sjl": "Slowakisch", "anj": "Englisch", "nej": "Deutsch", "frj": "Französisch", "esp": "Spanisch", "itj": "Italienisch", "ruj": "Russisch", "ukj": "Ukrainisch"},
    "ES": {"title": "📚 Materiales de estudio", "up": "Subir notas", "ok": "¡Archivo subido!", "bio": "Biología", "dej": "Historia", "fyz": "Fisica", "che": "Química", "mat": "Matemáticas", "obn": "Cívica", "geo": "Geografía", "inf": "Informática", "sjl": "Eslovaco", "anj": "Inglés", "nej": "Alemán", "frj": "Francés", "esp": "Español", "itj": "Italiano", "ruj": "Ruso", "ukj": "Ucraniano"},
    "FR": {"title": "📚 Matériels d'étude", "up": "Télécharger", "ok": "Téléchargé !", "bio": "Biologie", "dej": "Histoire", "fyz": "Physique", "che": "Chimie", "mat": "Mathématiques", "obn": "Éducation civique", "geo": "Géographie", "inf": "Informatique", "sjl": "Slovaque", "anj": "Anglais", "nej": "Allemand", "frj": "Français", "esp": "Espagnol", "itj": "Italien", "ruj": "Russe", "ukj": "Ukrainien"},
    "IT": {"title": "📚 Materiali di studio", "up": "Carica", "ok": "Caricato!", "bio": "Biologia", "dej": "Storia", "fyz": "Fisica", "che": "Chimica", "mat": "Matematica", "obn": "Educazione civica", "geo": "Geografia", "inf": "Informatica", "sjl": "Slovacco", "anj": "Inglese", "nej": "Tedesco", "frj": "Francese", "esp": "Spagnolo", "itj": "Italiano", "ruj": "Ruso", "ukj": "Ucraino"},
    "UA": {"title": "📚 Навчальні матеріали", "up": "Завантажити", "ok": "Завантажено!", "bio": "Біологія", "che": "Хімія", "dej": "Історія", "fyz": "Фізика", "mat": "Математика", "obn": "Правознавство", "geo": "Географія", "inf": "Інформатика", "sjl": "Словацька", "anj": "Англійська", "nej": "Німецька", "frj": "Французька", "esp": "Іспанська", "itj": "Італійська", "ruj": "Російська", "ukj": "Українська"},
    "RU": {"title": "📚 Учебные материалы", "up": "Загрузить", "ok": "Загружено!", "bio": "Биология", "dej": "История", "fyz": "Физика", "che": "Химия", "mat": "Математика", "obn": "Обществознание", "geo": "География", "inf": "Информатика", "sjl": "Словацкий", "anj": "Anglijskij", "nej": "Nemeckij", "frj": "Francuzskij", "esp": "Ispanskij", "itj": "Italianskij", "ruj": "Russkij", "ukj": "Ukrainskij"}
}

# Zistenie jazyka z URL (predvolená je slovenčina)
L = st.query_params.get("lang", "SK").upper()
t = lang_data.get(L, lang_data["SK"])

# 3. TVOJE ID PRIEČINKOV
ids = {
    "bio": "1HwEr80n2TnaAs7oyixCvcFWF5ZGKPjmf", "dej": "1zbicCs41T0Vrjf5DxyQ-5OJaWGvCl5kk", 
    "fyz": "1LumTX7YUXknUu16WcG9ooUYq6Nchc-XS", "che": "1BrnIjnLQfB9ZjcmMxmz-e-_QvoyRkKaR",
    "mat": "16o7nKWMoIOk7b8m90tXbgA4L2NeZ9STm", "obn": "1kNvYlsNxa64IVyB-QLSXQ_8pC6oQzof_", 
    "geo": "1D7Zn_c3qn18aH5i_GrcxYawxZRoFzbN2", "inf": "1eg0Oq3w-3nDJ9EschjWPLGY2anrv6P7u",
    "sjl": "1GY8gyXFXGIXG3gL5cXBPOlbEjsqowpA-", "anj": "1ffEMvwZA4zTCbcCLx3DqfAQYTmqt4fiB", 
    "nej": "1rejCBuHI8qFm_y2Dr1zR9PtJnMJ9SkCI", "frj": "1qf6u3qAMKLkTK4e1QBbBCVo0VNothU3j",
    "esp": "1ZGTJ3xtPY0nQ5blLiAZ-WcXE5DVzhm68", "itj": "161jDX2VhvCpRIoPpY1FLIj08rp5chhp_", 
    "ruj": "1w7F9_8m4DkFnXx33Iys_kLWgfWPI_Gt5", "ukj": "1FSp1PuT1yAJjR3
