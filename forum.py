import streamlit as st

# 1. ZÁKLADNÉ NASTAVENIE
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;} 
    .stAppDeployButton {display:none;}
    iframe {border-radius: 15px; border: 1px solid #ddd; background-color: white;}
    /* Štýl pre tlačidlá, aby boli pekné */
    .stButton>button {border-radius: 10px;}
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
        "bio": "Біологія", "che": "Хімія", "dej": "Історія", "fyz": "Фізика", "mat": "Математика", "obn": "Праvoзнавство", "geo": "Географія", "inf": "Інформатика",
        "sjl": "Словацька", "anj": "Англійська", "nej": "Німецька", "frj": "Французька", "esp": "Іспанська", "itj": "Італійська", "ruj": "Російська", "ukj": "Українська"
    },
    "RU": {
        "title": "📚 Учебные материалы", "up": "Загрузить", "ok": "Загружено!",
        "bio": "Биология", "che": "Химия", "dej": "История", "fyz": "Физика", "mat": "Математика", "obn": "Обществознание", "geo": "География", "inf": "Информатика",
        "sjl": "Словацкий", "anj": "Английский", "nej": "Немецкий", "frj": "Французский", "esp": "Испанский", "itj": "Итальянский", "ruj": "Русский", "ukj": "Украинский"
    }
}

L = st.query_params.get("lang", "SK").upper()
t = lang_data.get(L, lang_data["SK"])

# 3. ID TVOJICH PRIEČINKOV (Tu vlož ID kódiky z Drive)
ids = {
    "bio": "ID_BIOLOGIA", "dej": "ID_DEJEPIS", "fyz": "ID_FYZIKA", "che": "ID_CHEMIA",
    "mat": "ID_MATEMATIKA", "obn": "ID_OBCIANSKA", "geo": "ID_GEOGRAFIA", "inf": "ID_INFORMATIKA",
    "sjl": "ID_SLOVENCINA", "anj": "ID_ANGLICTINA", "nej": "ID_NEMCINA", "frj": "ID_FRANCUZSTINA",
    "esp": "ID_SPANIELCINA", "itj": "ID_TALIANCINA", "ruj": "ID_RUSTINA", "ukj": "ID_UKRAJINCINA"
}

# Nastavenie predvoleného priečinka (Biológia)
if "selected_folder" not in st.session_state:
    st.session_state.selected_folder = ids["bio"]

# Funkcia na zmenu priečinka
def set_folder(folder_id):
    st.session_state.selected_folder = folder_id

# 4. ZOBRAZENIE UI
st.title(t["title"])

u = st.file_uploader(t["up"], type=['pdf', 'png', 'jpg'])
if u: st.success(t["ok"])

st.write("---")

# DLAŽDICE PREDMETOV
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button(f"🧬 {t['bio']}", use_container_width=True): set_folder(ids["bio"])
    if st.button(f"🏺 {t['dej']}", use_container_width=True): set_folder(ids["dej"])
with c2:
    if st.button(f"⚛️ {t['fyz']}", use_container_width=True): set_folder(ids["fyz"])
    if st.button(f"🧪 {t['che']}", use_container_width=True): set_folder(ids["che"])
with c3:
    if st.button(f"📐 {t['mat']}", use_container_width=True): set_folder(ids["mat"])
    if st.button(f"⚖️ {t['obn']}", use_container_width=True): set_folder(ids["obn"])
with c4:
    if st.button(f"🌍 {t['geo']}", use_container_width=True): set_folder(ids["geo"])
    if st.button(f"💻 {t['inf']}", use_container_width=True): set_folder(ids["inf"])

# JAZYKOVÉ DLAŽDICE
st.write("---")
j1, j2, j3, j4 = st.columns(4)
with j1:
    if st.button(f"🇸🇰 {t['sjl']}", use_container_width=True): set_folder(ids["sjl"])
    if st.button(f"🇬🇧 {t['anj']}", use_container_width=True): set_folder(ids["anj"])
with j2:
    if st.button(f"🇩🇪 {t['nej']}", use_container_width=True): set_folder(ids["nej"])
    if st.button(f"🇫🇷 {t['frj']}", use_container_width=True): set_folder(ids["frj"])
with j3:
    if st.button(f"🇪🇸 {t['esp']}", use_container_width=True): set_folder(ids["esp"])
    if st.button(f"🇮🇹 {t['itj']}", use_container_width=True): set_folder(ids["itj"])
with j4:
    if st.button(f"🇷🇺 {t['ruj']}", use_container_width=True): set_folder(ids["ruj"])
    if st.button(f"🇺🇦 {t['ukj']}", use_container_width=True): set_folder(ids["ukj"])

st.write("---")

# 5. DYNAMICKÉ OKNO S DOKUMENTMI
drive_url = f"https://drive.google.com/embeddedfolderview?id={st.session_state.selected_folder}#grid"
st.components.v1.iframe(drive_url, height=600, scrolling=True)
