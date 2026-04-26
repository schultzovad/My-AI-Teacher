import streamlit as st

# 1. ZÁKLADNÉ NASTAVENIE
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

# 2. KOMPLETNÉ PREKLADY PRE VŠETKÝCH 8 JAZYKOV
lang_data = {
    "SK": {
        "title": "📚 Študijné materiály", "up": "Nahraj svoje poznámky", "ok": "Súbor nahraný!", "open": "Otvoriť",
        "bio": "Biológia", "che": "Chémia", "dej": "Dejepis", "fyz": "Fyzika", "mat": "Matematika", "obn": "Občianska náuka", "geo": "Geografia", "inf": "Informatika",
        "sjl": "Slovenčina", "anj": "Angličtina", "nej": "Nemčina", "frj": "Francúzština", "esp": "Španielčina", "itj": "Taliančina", "ruj": "Ruština", "ukj": "Ukrajinčina"
    },
    "EN": {
        "title": "📚 Study Materials", "up": "Upload your notes", "ok": "File uploaded!", "open": "Open",
        "bio": "Biology", "che": "Chemistry", "dej": "History", "fyz": "Physics", "mat": "Mathematics", "obn": "Civics", "geo": "Geography", "inf": "Informatics",
        "sjl": "Slovak", "anj": "English", "nej": "German", "frj": "French", "esp": "Spanish", "itj": "Italian", "ruj": "Russian", "ukj": "Ukrainian"
    },
    "DE": {
        "title": "📚 Lernmaterialien", "up": "Notizen hochladen", "ok": "Datei hochgeladen!", "open": "Öffnen",
        "bio": "Biologie", "che": "Chemie", "dej": "Geschichte", "fyz": "Physik", "mat": "Mathematik", "obn": "Sozialkunde", "geo": "Geographie", "inf": "Informatik",
        "sjl": "Slowakisch", "anj": "Englisch", "nej": "Deutsch", "frj": "Französisch", "esp": "Spanisch", "itj": "Italienisch", "ruj": "Russisch", "ukj": "Ukrainisch"
    },
    "ES": {
        "title": "📚 Materiales de estudio", "up": "Subir notas", "ok": "¡Archivo subido!", "open": "Abrir",
        "bio": "Biología", "che": "Química", "dej": "Historia", "fyz": "Física", "mat": "Matemáticas", "obn": "Cívica", "geo": "Geografía", "inf": "Informática",
        "sjl": "Eslovaco", "anj": "Inglés", "nej": "Alemán", "frj": "Francés", "esp": "Español", "itj": "Italiano", "ruj": "Ruso", "ukj": "Ucraniano"
    },
    "FR": {
        "title": "📚 Matériels d'étude", "up": "Télécharger vos notes", "ok": "Téléchargé !", "open": "Ouvrir",
        "bio": "Biologie", "che": "Chimie", "dej": "Histoire", "fyz": "Physique", "mat": "Mathématiques", "obn": "Éducation civique", "geo": "Géographie", "inf": "Informatique",
        "sjl": "Slovaque", "anj": "Anglais", "nej": "Allemand", "frj": "Français", "esp": "Espagnol", "itj": "Italien", "ruj": "Russe", "ukj": "Ukrainien"
    },
    "IT": {
        "title": "📚 Materiali di studio", "up": "Carica note", "ok": "Caricato!", "open": "Apri",
        "bio": "Biologia", "che": "Chimica", "dej": "Storia", "fyz": "Fisica", "mat": "Matematica", "obn": "Educazione civica", "geo": "Geografia", "inf": "Informatica",
        "sjl": "Slovacco", "anj": "Inglese", "nej": "Tedesco", "frj": "Francese", "esp": "Spagnolo", "itj": "Italiano", "ruj": "Russo", "ukj": "Ucraino"
    },
    "UA": {
        "title": "📚 Навчальні матеріали", "up": "Завантажити", "ok": "Завантажено!", "open": "Відкрити",
        "bio": "Біологія", "che": "Хімія", "dej": "Історія", "fyz": "Фізика", "mat": "Математика", "obn": "Правознавство", "geo": "Географія", "inf": "Інформатика",
        "sjl": "Словацька", "anj": "Англійська", "nej": "Німецька", "frj": "Французька", "esp": "Іспанська", "itj": "Італійська", "ruj": "Російська", "ukj": "Українська"
    },
    "RU": {
        "title": "📚 Учебные материалы", "up": "Загрузить", "ok": "Загружено!", "open": "Открыть",
        "bio": "Биология", "che": "Химия", "dej": "История", "fyz": "Физика", "mat": "Математика", "obn": "Обществознание", "geo": "География", "inf": "Информатика",
        "sjl": "Словацкий", "anj": "Английский", "nej": "Немецкий", "frj": "Французский", "esp": "Испанский", "itj": "Итальянский", "ruj": "Русский", "ukj": "Украинский"
    }
}

L = st.query_params.get("lang", "SK").upper()
t = lang_data.get(L, lang_data["SK"])

# 3. ZOBRAZENIE
st.title(t["title"])

u = st.file_uploader(t["up"], type=['pdf', 'png', 'jpg'])
if u: st.success(t["ok"])

st.write("---")

# 4. TVORBA DLAŽDÍC PRE PREDMETY
c1, c2, c3, c4 = st.columns(4)

# Definícia linkov (Tu si vlož svoje URL z Google Drive)
links = {
    "bio": "URL_BIOLOGIA", "dej": "URL_DEJEPIS", "fyz": "URL_FYZIKA", "che": "URL_CHEMIA",
    "mat": "URL_MATEMATIKA", "obn": "URL_OBCIANSKA", "geo": "URL_GEOGRAFIA", "inf": "URL_INFORMATIKA",
    "sjl": "URL_SLOVENCINA", "anj": "URL_ANGLICTINA", "nej": "URL_NEMCINA", "frj": "URL_FRANCUZSTINA",
    "esp": "URL_SPANIELCINA", "itj": "URL_TALIANCINA", "ruj": "URL_RUSTINA", "ukj": "URL_UKRAJINCINA"
}

with c1:
    st.info(f"🧬 **{t['bio']}**")
    st.link_button(t["open"], links["bio"], use_container_width=True)
    st.info(f"🏺 **{t['dej']}**")
    st.link_button(t["open"], links["dej"], use_container_width=True)

with c2:
    st.info(f"⚛️ **{t['fyz']}**")
    st.link_button(t["open"], links["fyz"], use_container_width=True)
    st.info(f"🧪 **{t['che']}**")
    st.link_button(t["open"], links["che"], use_container_width=True)

with c3:
    st.info(f"📐 **{t['mat']}**")
    st.link_button(t["open"], links["mat"], use_container_width=True)
    st.info(f"⚖️ **{t['obn']}**")
    st.link_button(t["open"], links["obn"], use_container_width=True)

with c4:
    st.info(f"🌍 **{t['geo']}**")
    st.link_button(t["open"], links["geo"], use_container_width=True)
    st.info(f"💻 **{t['inf']}**")
    st.link_button(t["open"], links["inf"], use_container_width=True)

st.write("---")
st.subheader("🌐 Languages")

j1, j2, j3, j4 = st.columns(4)
with j1:
    st.link_button(f"🇸🇰 {t['sjl']}", links["sjl"], use_container_width=True)
    st.link_button(f"🇬🇧 {t['anj']}", links["anj"], use_container_width=True)
with j2:
    st.link_button(f"🇩🇪 {t['nej']}", links["nej"], use_container_width=True)
    st.link_button(f"🇫🇷 {t['frj']}", links["frj"], use_container_width=True)
with j3:
    st.link_button(f"🇪🇸 {t['esp']}", links["esp"], use_container_width=True)
    st.link_button(f"🇮🇹 {t['itj']}", links["itj"], use_container_width=True)
with j4:
    st.link_button(f"🇷🇺 {t['ruj']}", links["ruj"], use_container_width=True)
    st.link_button(f"🇺🇦 {t['ukj']}", links["ukj"], use_container_width=True)
