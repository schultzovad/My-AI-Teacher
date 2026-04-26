import streamlit as st

# 1. ZÁKLADNÉ NASTAVENIE (Tvoj pôvodný kód)
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

lang_data = {
    "SK": {"title": "📚 Študijné materiály", "up": "Nahraj svoje poznámky", "ok": "Súbor nahraný!", "subjects": "Predmety", "lang_sect": "Jazyky"},
    "EN": {"title": "📚 Study Materials", "up": "Upload your notes", "ok": "File uploaded!", "subjects": "Subjects", "lang_sect": "Languages"},
    "DE": {"title": "📚 Lernmaterialien", "up": "Notizen hochladen", "ok": "Datei hochgeladen!", "subjects": "Fächer", "lang_sect": "Sprachen"},
    "ES": {"title": "📚 Materiales", "up": "Subir notas", "ok": "¡Archivo subido!", "subjects": "Materias", "lang_sect": "Idiomas"},
    "FR": {"title": "📚 Matériels", "up": "Télécharger", "ok": "Fichier téléchargé !", "subjects": "Matières", "lang_sect": "Langues"},
    "IT": {"title": "📚 Materiali", "up": "Carica note", "ok": "File caricato!", "subjects": "Materie", "lang_sect": "Lingue"},
    "UA": {"title": "📚 Навчальні мат.", "up": "Завантажити", "ok": "Файл завантажено!", "subjects": "Предмети", "lang_sect": "Мови"},
    "RU": {"title": "📚 Учебные мат.", "up": "Загрузить", "ok": "Файл загружен!", "subjects": "Предметы", "lang_sect": "Языки"}
}

L = st.query_params.get("lang", "SK").upper()
t = lang_data.get(L, lang_data["SK"])

# 2. TITULOK A UPLOADER (Tvoj pôvodný funkčný kód)
st.title(t["title"])
u = st.file_uploader(t["up"], type=['pdf', 'png', 'jpg'])
if u: 
    st.success(t["ok"])

st.write("---")

# 3. KNIŽNICA PRIEČINKOV (Nová časť podľa tvojich fotiek)
st.subheader(t["subjects"])

# Rozdelenie na 3 stĺpce pre predmety
c1, c2, c3 = st.columns(3)

with c1:
    st.info("🧬 **Biológia**")
    st.link_button("Otvoriť", "LINK_NA_TVOJ_PRIECINOK_BIOLOGIA", use_container_width=True)
    
    st.info("🏺 **Dejepis**")
    st.link_button("Otvoriť", "LINK_NA_TVOJ_PRIECINOK_DEJEPIS", use_container_width=True)

with c2:
    st.info("⚛️ **Fyzika**")
    st.link_button("Otvoriť", "LINK_NA_TVOJ_PRIECINOK_FYZIKA", use_container_width=True)
    
    st.info("🧪 **Chémia**")
    st.link_button("Otvoriť", "LINK_NA_TVOJ_PRIECINOK_CHEMIA", use_container_width=True)

with c3:
    st.info("📐 **Matematika**")
    st.link_button("Otvoriť", "LINK_NA_TVOJ_PRIECINOK_MATEMATIKA", use_container_width=True)
    
    st.info("⚖️ **Občianska náuka**")
    st.link_button("Otvoriť", "LINK_NA_TVOJ_PRIECINOK_OBCIANSKA", use_container_width=True)

st.write("")
st.subheader(t["lang_sect"])

# Rozdelenie na 4 stĺpce pre jazyky (podľa tvojej fotky)
j1, j2, j3, j4 = st.columns(4)

with j1:
    st.link_button("🇸🇰 Slovenčina", "LINK_NA_SLOVENCINA", use_container_width=True)
    st.link_button("🇬🇧 Angličtina", "LINK_NA_ANGLICTINA", use_container_width=True)

with j2:
    st.link_button("🇩🇪 Nemčina", "LINK_NA_NEMCINA", use_container_width=True)
    st.link_button("🇫🇷 Francúzština", "LINK_NA_FRANCUZSTINA", use_container_width=True)

with j3:
    st.link_button("🇪🇸 Španielčina", "LINK_NA_SPANIELCINA", use_container_width=True)
    st.link_button("🇮🇹 Taliančina", "LINK_NA_TALIANCINA", use_container_width=True)

with j4:
    st.link_button("🇷🇺 Ruština", "LINK_NA_RUSTINA", use_container_width=True)
    st.link_button("🇺🇦 Ukrajinčina", "LINK_NA_UKRAJINCINA", use_container_width=True)
