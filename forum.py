import streamlit as st

# 1. ZÁKLADNÉ NASTAVENIE
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;} 
    .stAppDeployButton {display:none;}
    iframe {border-radius: 15px; border: 1px solid #ddd; background-color: white;}
    .stButton>button {border-radius: 10px; font-weight: 500;}
    </style>
""", unsafe_allow_html=True)

# 2. KOMPLETNÉ PREKLADY (8 JAZYKOV)
lang_data = {
    "SK": {
        "title": "📚 Študijné materiály", "up": "Nahraj svoje poznámky", "ok": "Súbor nahraný!",
        "bio": "Biológia", "dej": "Dejepis", "fyz": "Fyzika", "che": "Chémia", "mat": "Matematika", "obn": "Občianska náuka", "geo": "Geografia", "inf": "Informatika",
        "sjl": "Slovenčina", "anj": "Angličtina", "nej": "Nemčina", "frj": "Francúzština", "esp": "Španielčina", "itj": "Taliančina", "ruj": "Ruština", "ukj": "Ukrajinčina"
    },
    "EN": {
        "title": "📚 Study Materials", "up": "Upload your notes", "ok": "File uploaded!",
        "bio": "Biology", "dej": "History", "fyz": "Physics", "che": "Chemistry", "mat": "Mathematics", "obn": "Civics", "geo": "Geography", "inf": "Informatics",
        "sjl": "Slovak", "anj": "English", "nej": "German", "frj": "French", "esp": "Spanish", "itj": "Italian", "ruj": "Russian", "ukj": "Ukrainian"
    },
    "DE": {
        "title": "📚 Lernmaterialien", "up": "Notizen hochladen", "ok": "Datei hochgeladen!",
        "bio": "Biologie", "dej": "Geschichte", "fyz": "Physik", "che": "Chemie", "mat": "Mathematik", "obn": "Sozialkunde", "geo": "Geographie", "inf": "Informatik",
        "sjl": "Slowakisch", "anj": "Englisch", "nej": "Deutsch", "frj": "Französisch", "esp": "Spanisch", "itj": "Italienisch", "ruj": "Russisch", "ukj": "Ukrainisch"
    },
    "ES": {
        "title": "📚 Materiales de estudio", "up": "Subir notas", "ok": "¡Archivo subido!",
        "bio": "Biología", "dej": "Historia", "fyz": "Física", "che": "Química", "mat": "Matemáticas", "obn": "Cívica", "geo": "Geografía", "inf": "Informática",
        "sjl": "Eslovaco", "anj": "Inglés", "nej": "Alemán", "frj": "Francés", "esp": "Español", "itj": "Italiano", "ruj": "Ruso", "ukj": "Ucraniano"
    },
    "FR": {
        "title": "📚 Matériels d'étude", "up": "Télécharger", "ok": "Téléchargé !",
        "bio": "Biologie", "dej": "Histoire", "fyz": "Physique", "che": "Chimie", "mat": "Mathématiques", "obn": "Éducation civique", "geo": "Géographie", "inf": "Informatique",
        "sjl": "Slovaque", "anj": "Anglais", "nej": "Allemand", "frj": "Français", "esp": "Espagnol", "itj": "Italien", "ruj": "Russe", "ukj": "Ukrainien"
    },
    "IT": {
        "title": "📚 Materiali di studio", "up": "Carica", "ok": "Caricato!",
        "bio": "Biologia", "dej": "Storia", "fyz": "Fisica", "che": "Chimica", "mat": "Matematica", "obn": "Educazione civica", "geo": "Geografia", "inf": "Informatica",
        "sjl": "Slovacco", "anj": "Inglese", "nej": "Tedesco", "frj": "Francese", "esp": "Spagnolo", "itj": "Italiano", "ruj": "Russo", "ukj": "Ucraino"
    },
    "UA": {
        "title": "📚 Навчальні матеріали", "up": "Завантажити", "ok": "Завантажено!",
        "bio": "Біологія", "che": "Хімія", "dej": "Історія", "fyz": "Фізика", "mat": "Математика", "obn": "Правознавство", "geo": "Географія", "inf": "Інформатика",
        "sjl": "Словацька", "anj": "Англійська", "nej": "Німецька", "frj": "Французька", "esp": "Іспанська", "itj": "Італійська", "ruj": "Російська", "ukj": "Українська"
    },
    "RU": {
        "title": "📚 Учебные материалы", "up": "Загрузить", "ok": "Загружено!",
        "bio": "Биология", "che": "Химия", "dej": "История", "fyz": "Физика", "che": "Химия", "mat": "Математика", "obn": "Обществознание", "geo": "География", "inf": "Информатика",
        "sjl": "Словацкий", "anj": "Английский", "nej": "Немецкий", "frj": "Французский", "esp": "Испанский", "itj": "Итальянский", "ruj": "Русский", "ukj": "Украинский"
    }
}

L = st.query_params.get("lang", "SK").upper()
t = lang_data.get(L, lang_data["SK"])

# 3. ID PRIEČINKOV (Nezabudni doplniť svoje ID z Drive!)
ids = {
    "bio": "1HwEr80n2TnaAs7oyixCvcFWF5ZGKPjmf", "dej": "1zbicCs41T0Vrjf5DxyQ-5OJaWGvCl5kk", "fyz": "1LumTX7YUXknUu16WcG9ooUYq6Nchc-XS", "che": "1BrnIjnLQfB9ZjcmMxmz-e-_QvoyRkKaR",
    "mat": "16o7nKWMoIOk7b8m90tXbgA4L2NeZ9STm", "obn": "1kNvYlsNxa64IVyB-QLSXQ_8pC6oQzof_", "geo": "1D7Zn_c3qn18aH5i_GrcxYawxZRoFzbN2", "inf": "1eg0Oq3w-3nDJ9EschjWPLGY2anrv6P7u",
    "sjl": "1GY8gyXFXGIXG3gL5cXBPOlbEjsqowpA-", "anj": "1ffEMvwZA4zTCbcCLx3DqfAQYTmqt4fiB", "nej": "1rejCBuHI8qFm_y2Dr1zR9PtJnMJ9SkCI", "frj": "1qf6u3qAMKLkTK4e1QBbBCVo0VNothU3j",
    "esp": "1ZGTJ3xtPY0nQ5blLiAZ-WcXE5DVzhm68", "itj": "161jDX2VhvCpRIoPpY1FLIj08rp5chhp_", "ruj": "1w7F9_8m4DkFnXx33Iys_kLWgfWPI_Gt5", "ukj": "1FSp1PuT1yAJjR3HW17sgvXXIyIWrYHYO"
}

if "selected_folder" not in st.session_state:
    st.session_state.selected_folder = ids["bio"]

def set_folder(folder_id):
    st.session_state.selected_folder = folder_id

# 4. UI - TITULOK A UPLOADER
st.title(t["title"])
u = st.file_uploader(t["up"], type=['pdf', 'png', 'jpg'])
if u: st.success(t["ok"])

st.write("---")

# 5. TLAČIDLÁ PREDMETOV
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button(t["bio"], use_container_width=True): set_folder(ids["bio"])
    if st.button(t["dej"], use_container_width=True): set_folder(ids["dej"])
with c2:
    if st.button(t["fyz"], use_container_width=True): set_folder(ids["fyz"])
    if st.button(t["che"], use_container_width=True): set_folder(ids["che"])
with c3:
    if st.button(t["mat"], use_container_width=True): set_folder(ids["mat"])
    if st.button(t["obn"], use_container_width=True): set_folder(ids["obn"])
with c4:
    if st.button(t["geo"], use_container_width=True): set_folder(ids["geo"])
    if st.button(t["inf"], use_container_width=True): set_folder(ids["inf"])

# 6. TLAČIDLÁ JAZYKOV (Bez skratiek a vlajok, len čisté slová)
st.write("---")
j1, j2, j3, j4 = st.columns(4)
with j1:
    if st.button(t["sjl"], use_container_width=True): set_folder(ids["sjl"])
    if st.button(t["anj"], use_container_width=True): set_folder(ids["anj"])
with j2:
    if st.button(t["nej"], use_container_width=True): set_folder(ids["nej"])
    if st.button(t["frj"], use_container_width=True): set_folder(ids["frj"])
with j3:
    if st.button(t["esp"], use_container_width=True): set_folder(ids["esp"])
    if st.button(t["itj"], use_container_width=True): set_folder(ids["itj"])
with j4:
    if st.button(t["ruj"], use_container_width=True): set_folder(ids["ruj"])
    if st.button(t["ukj"], use_container_width=True): set_folder(ids["ukj"])

st.write("---")

# 7. OKNO S DOKUMENTMI
drive_url = f"https://drive.google.com/embeddedfolderview?id={st.session_state.selected_folder}#grid"
st.components.v1.iframe(drive_url, height=600, scrolling=True)
