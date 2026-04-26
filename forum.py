import streamlit as st

# 1. ZÁKLADNÉ NASTAVENIE
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;} 
    .stAppDeployButton {display:none;}
    iframe {border-radius: 15px; border: 1px solid #ddd;}
    </style>
""", unsafe_allow_html=True)

# 2. KOMPLETNÉ JAZYKOVÉ DÁTA (8 JAZYKOV)
lang_data = {
    "SK": {
        "title": "📚 Študijné materiály", "up": "Nahraj svoje poznámky", "ok": "Súbor nahraný!",
        "subj_list": "Zoznam predmetov a jazykov:",
        "bio": "Biológia", "dej": "Dejepis", "fyz": "Fyzika", "che": "Chémia", "mat": "Matematika", "obn": "Občianska náuka", "geo": "Geografia", "inf": "Informatika",
        "sjl": "Slovenčina", "anj": "Angličtina", "nej": "Nemčina", "frj": "Francúzština", "esp": "Španielčina", "itj": "Taliančina", "ruj": "Ruština", "ukj": "Ukrajinčina"
    },
    "EN": {
        "title": "📚 Study Materials", "up": "Upload your notes", "ok": "File uploaded!",
        "subj_list": "List of subjects and languages:",
        "bio": "Biology", "dej": "History", "fyz": "Physics", "che": "Chemistry", "mat": "Mathematics", "obn": "Civics", "geo": "Geography", "inf": "Informatics",
        "sjl": "Slovak", "anj": "English", "nej": "German", "frj": "French", "esp": "Spanish", "itj": "Italian", "ruj": "Russian", "ukj": "Ukrainian"
    },
    "DE": {
        "title": "📚 Lernmaterialien", "up": "Notizen hochladen", "ok": "Datei hochgeladen!",
        "subj_list": "Liste der Fächer und Sprachen:",
        "bio": "Biologie", "dej": "Geschichte", "fyz": "Physik", "che": "Chemie", "mat": "Mathematik", "obn": "Sozialkunde", "geo": "Geographie", "inf": "Informatik",
        "sjl": "Slowakisch", "anj": "Englisch", "nej": "Deutsch", "frj": "Französisch", "esp": "Spanisch", "itj": "Italienisch", "ruj": "Russisch", "ukj": "Ukrainisch"
    },
    "ES": {
        "title": "📚 Materiales de estudio", "up": "Subir notas", "ok": "¡Archivo subido!",
        "subj_list": "Lista de materias e idiomas:",
        "bio": "Biología", "dej": "Historia", "fyz": "Física", "che": "Química", "mat": "Matemáticas", "obn": "Educación cívica", "geo": "Geografía", "inf": "Informática",
        "sjl": "Eslovaco", "anj": "Inglés", "nej": "Alemán", "frj": "Francés", "esp": "Español", "itj": "Italiano", "ruj": "Ruso", "ukj": "Ucraniano"
    },
    "FR": {
        "title": "📚 Matériels d'étude", "up": "Télécharger vos notes", "ok": "Fichier téléchargé !",
        "subj_list": "Liste des matières et langues :",
        "bio": "Biologie", "dej": "Histoire", "fyz": "Physique", "che": "Chimie", "mat": "Mathématiques", "obn": "Éducation civique", "geo": "Géographie", "inf": "Informatique",
        "sjl": "Slovaque", "anj": "Anglais", "nej": "Allemand", "frj": "Français", "esp": "Espagnol", "itj": "Italien", "ruj": "Russe", "ukj": "Ukrainien"
    },
    "IT": {
        "title": "📚 Materiali di studio", "up": "Carica note", "ok": "File caricato!",
        "subj_list": "Elenco delle materie e delle lingue:",
        "bio": "Biologia", "dej": "Storia", "fyz": "Fisica", "che": "Chimica", "mat": "Matematica", "obn": "Educazione civica", "geo": "Geografia", "inf": "Informatica",
        "sjl": "Slovacco", "anj": "Inglese", "nej": "Tedesco", "frj": "Francese", "esp": "Spagnolo", "itj": "Italiano", "ruj": "Russo", "ukj": "Ucraino"
    },
    "UA": {
        "title": "📚 Навчальні матеріали", "up": "Завантажити нотатки", "ok": "Файл завантажено!",
        "subj_list": "Список предметів та мов:",
        "bio": "Біологія", "dej": "Історія", "fyz": "Фізика", "che": "Хімія", "mat": "Математика", "obn": "Громадянська освіта", "geo": "Географія", "inf": "Інформатика",
        "sjl": "Словацька", "anj": "Англійська", "nej": "Німецька", "frj": "Французька", "esp": "Іспанська", "itj": "Італійська", "ruj": "Російська", "ukj": "Українська"
    },
    "RU": {
        "title": "📚 Учебные материалы", "up": "Загрузить заметки", "ok": "Файл загружен!",
        "subj_list": "Список предметов и языков:",
        "bio": "Биология", "dej": "История", "fyz": "Физика", "che": "Химия", "mat": "Математика", "obn": "Обществознание", "geo": "География", "inf": "Информатика",
        "sjl": "Словацкий", "anj": "Английский", "nej": "Немецкий", "frj": "Французский", "esp": "Испанский", "itj": "Итальянский", "ruj": "Русский", "ukj": "Украинский"
    }
}

L = st.query_params.get("lang", "SK").upper()
t = lang_data.get(L, lang_data["SK"])

# 3. UPLOADER (Tvoj pôvodný)
st.title(t["title"])
u = st.file_uploader(t["up"], type=['pdf', 'png', 'jpg'])
if u: st.success(t["ok"])

st.write("---")

# 4. EMBED GOOGLE DRIVE (Okno priamo v stránke)
# DÔLEŽITÉ: Tu nahraď ID tvojho hlavného priečinka "Study materials"
# Získaš ho z URL adresy priečinka (to dlhé za /folders/)
FOLDER_ID = "1abc123_SEM_VLOZ_SVOJE_ID" 

st.subheader(t["subj_list"])

# Toto vytvorí okno s tvojimi priečinkami priamo v Streamlite
drive_url = f"https://drive.google.com/embeddedfolderview?id={FOLDER_ID}#grid"
st.components.v1.iframe(drive_url, height=600, scrolling=True)

st.info("💡 Tip: V okne vyššie uvidíte všetky predmety. Po kliknutí na priečinok uvidíte jeho obsah.")
