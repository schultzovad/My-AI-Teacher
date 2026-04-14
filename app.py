import streamlit as st
import streamlit.components.v1 as components

# --- 1. ZÁKLADNÉ NASTAVENIA (TU SA MENÍ NÁZOV STRÁNKY) ---
st.set_page_config(
    page_title="EduHub", 
    layout="wide", 
    page_icon="🎓"
)

# --- 2. KOMPLETNÝ SLOVNÍK (8 JAZYKOV) ---
lang_data = {
    "SK": {"h": "🏠 Domov", "c": "🤖 AI Tutor", "f": "📚 Študijné materiály", "g": "👥 Študijné skupiny", "i": "S čím ti dnes pomôžem?", "u": "Nahraj svoje poznámky", "s": "Súbor bol úspešne nahraný!", "n": "Vytvoriť novú skupinu"},
    "EN": {"h": "🏠 Home", "c": "🤖 AI Tutor", "f": "📚 Study Materials", "g": "👥 Study Groups", "i": "How can I help you today?", "u": "Upload your notes", "s": "File uploaded successfully!", "n": "Create new group"},
    "DE": {"h": "🏠 Startseite", "c": "🤖 AI Tutor", "f": "📚 Lernmaterialien", "g": "👥 Studiengruppen", "i": "Wie kann ich dir helfen?", "u": "Notizen hochladen", "s": "Datei erfolgreich hochgeladen!", "n": "Neue Gruppe erstellen"},
    "ES": {"h": "🏠 Inicio", "c": "🤖 Tutor AI", "f": "📚 Materiales de estudio", "g": "👥 Grupos de estudio", "i": "¿Cómo te puedo ayudar?", "u": "Subir notas", "s": "¡Archivo subido con éxito!", "n": "Crear nuevo grupo"},
    "FR": {"h": "🏠 Accueil", "c": "🤖 Tuteur IA", "f": "📚 Matériels d'étude", "g": "👥 Groupes d'étude", "i": "Comment puis-je vous aider ?", "u": "Télécharger vos notes", "s": "Fichier téléchargé avec succès !", "n": "Créer un nouveau groupe"},
    "IT": {"h": "🏠 Home", "c": "🤖 Tutor IA", "f": "📚 Materiali di studio", "g": "👥 Gruppi di studio", "i": "Come posso aiutarti?", "u": "Carica le tue note", "s": "File caricato con successo!", "n": "Crea nuovo gruppo"},
    "UA": {"h": "🏠 Головна", "c": "🤖 AI Тьютор", "f": "📚 Навчальні матеріали", "g": "👥 Навчальні групи", "i": "Чим я можу вам допомогти?", "u": "Завантажте свои нотатки", "s": "Файл успішно завантажено!", "n": "Створити нову групу"},
    "RU": {"h": "🏠 Главная", "c": "🤖 AI Тьютор", "f": "📚 Учебные материалы", "g": "👥 Учебные группы", "i": "Чем я могу вам помочь?", "u": "Загрузите свои заметки", "s": "Файл успешно загружен!", "n": "Создать новую группу"}
}

# --- 3. BOČNÁ LIŠTA (SIDEBAR) ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    lang = st.selectbox("Language / Jazyk", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    # TLAČIDLO DOMOV - Posiela ťa na tvoj Framer
    if st.button(t["h"], use_container_width=True):
        hlavna_adresa = "https://silent-terms-318372.framer.app/"
        # Tento kód urobí tvrdý reset a vráti ťa na Framer
        js_code = f"window.parent.location.replace('{hlavna_adresa}');"
        components.html(f"<script>{js_code}</script>", height=0)
        st.stop()

    st.divider()
    page_selection = st.radio(t["h"].replace("🏠 ", ""), [t["c"], t["f"], t["g"]])

# --- 4. LOGIKA SKRÝVANIA ---
if not st.query_params.get("p"):
    st.stop()

# --- 5. ZOBRAZENIE OBSAHU ---
if page_selection == t["c"]:
    st.title(t["c"])
    if "messages" not in st.session_state: st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])
    if prompt := st.chat_input(t["i"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        response = "Analyzujem vaše poznámky a pripravujem odpoveď..."
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

elif page_selection == t["f"]:
    st.title(t["f"])
    st.file_uploader(t["u"], type=['pdf', 'png', 'jpg'])

elif page_selection == t["g"]:
    st.title(t["g"])
    nazov = st.text_input("Name")
    if st.button(t["n"]): st.balloons()
