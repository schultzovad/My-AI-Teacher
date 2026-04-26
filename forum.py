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
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/1HwEr80n2TnaAs7oyixCvcFWF5ZGKPjmf")
        
        st.info("🏺 **Dejepis**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/1zbicCs41T0Vrjf5DxyQ-5OJaWGvCl5kk")

    with c2:
        st.info("⚛️ **Fyzika**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/1LumTX7YUXknUu16WcG9ooUYq6Nchc-XS")
        
        st.info("🧪 **Chémia**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/1BrnIjnLQfB9ZjcmMxmz-e-_QvoyRkKaR")

    with c3:
        st.info("📐 **Matematika**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/16o7nKWMoIOk7b8m90tXbgA4L2NeZ9STm")
        
        st.info("⚖️ **Občianska náuka**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/1kNvYlsNxa64IVyB-QLSXQ_8pC6oQzof_")

    st.write("---")
    st.subheader("🌍 Jazyky")
    j1, j2, j3, j4 = st.columns(4)
    with j1:
        st.link_button("🇸🇰 Slovenčina", "https://drive.google.com/drive/u/1/folders/1GY8gyXFXGIXG3gL5cXBPOlbEjsqowpA-")
        st.link_button("🇬🇧 Angličtina", "https://drive.google.com/drive/u/1/folders/1ffEMvwZA4zTCbcCLx3DqfAQYTmqt4fiB")
    with j2:
        st.link_button("🇩🇪 Nemčina", "https://drive.google.com/drive/u/1/folders/1rejCBuHI8qFm_y2Dr1zR9PtJnMJ9SkCI")
        st.link_button("🇫🇷 Francúzština", "https://drive.google.com/drive/u/1/folders/1qf6u3qAMKLkTK4e1QBbBCVo0VNothU3j")
    with j3:
        st.link_button("🇪🇸 Španielčina", "https://drive.google.com/drive/u/1/folders/1qf6u3qAMKLkTK4e1QBbBCVo0VNothU3j")
        st.link_button("🇮🇹 Taliančina", "https://drive.google.com/drive/u/1/folders/161jDX2VhvCpRIoPpY1FLIj08rp5chhp_")
    with j4:
        st.link_button("🇷🇺 Ruština", "https://drive.google.com/drive/u/1/folders/1w7F9_8m4DkFnXx33Iys_kLWgfWPI_Gt5")
        st.link_button("🇺🇦 U
