

Prejsť na obsah
Používanie služby Gmail s čítačkami obrazovky
1 z 15
(bez predmetu)
Doručené

daniela schultzova <schultzovad@gmail.com>
14:12 (pred 2 minútami)
komu: mne

import streamlit as st
import streamlit.components.v1 as components

# --- 1. NASTAVENIA ---
st.set_page_config(page_title="EduHub AI Tutor", layout="wide", page_icon="🎓")

# --- 2. SLOVNÍK (8 JAZYKOV) ---
lang_data = {
    "SK": {"nav_title": "Navigácia", "home": "🏠 Domov", "chat_title": "🤖 AI Tutor", "forum_title": "📚 Študijné materiály", "groups_title": "👥 Študijné skupiny", "input_placeholder": "S čím ti dnes pomôžem?", "upload_label": "Nahraj svoje poznámky", "success_upload": "Súbor bol úspešne nahraný!", "create_group": "Vytvoriť novú skupinu"},
    "EN": {"nav_title": "Navigation", "home": "🏠 Home", "chat_title": "🤖 AI Tutor", "forum_title": "📚 Study Materials", "groups_title": "👥 Study Groups", "input_placeholder": "How can I help you today?", "upload_label": "Upload your notes", "success_upload": "File uploaded successfully!", "create_group": "Create new group"},
    "DE": {"nav_title": "Navigation", "home": "🏠 Startseite", "chat_title": "🤖 AI Tutor", "forum_title": "📚 Lernmaterialien", "groups_title": "👥 Studiengruppen", "input_placeholder": "Wie kann ich dir helfen?", "upload_label": "Notizen hochladen", "success_upload": "Datei erfolgreich hochgeladen!", "create_group": "Neue Gruppe erstellen"},
    "ES": {"nav_title": "Navegación", "home": "🏠 Inicio", "chat_title": "🤖 Tutor AI", "forum_title": "📚 Materiales de estudio", "groups_title": "👥 Grupos de estudio", "input_placeholder": "¿Cómo te puedo ayudar?", "upload_label": "Subir notas", "success_upload": "¡Archivo subido con éxito!", "create_group": "Crear nuevo grupo"},
    "FR": {"nav_title": "Navigation", "home": "🏠 Accueil", "chat_title": "🤖 Tuteur IA", "forum_title": "📚 Matériels d'étude", "groups_title": "👥 Groupes d'étude", "input_placeholder": "Comment puis-je vous aider ?", "upload_label": "Télécharger vos notes", "success_upload": "Fichier téléchargé avec succès !", "create_group": "Créer un nouveau groupe"},
    "IT": {"nav_title": "Navigazione", "home": "🏠 Home", "chat_title": "🤖 Tutor IA", "forum_title": "📚 Materiali di studio", "groups_title": "👥 Gruppi di studio", "input_placeholder": "Come posso aiutarti?", "upload_label": "Carica le tue note", "success_upload": "File caricato con successo!", "create_group": "Crea nuovo gruppo"},
    "UA": {"nav_title": "Навігація", "home": "🏠 Головна", "chat_title": "🤖 AI Тьютор", "forum_title": "📚 Навчальні матеріали", "groups_title": "👥 Навчальні групи", "input_placeholder": "Чим я можу вам допомогти?", "upload_label": "Завантажте свої нотатки", "success_upload": "Файл успішно завантажено!", "create_group": "Створити нову групу"},
    "RU": {"nav_title": "Навигация", "home": "🏠 Главная", "chat_title": "🤖 AI Тьютор", "forum_title": "📚 Учебные материалы", "groups_title": "👥 Учебные группы", "input_placeholder": "Чем я могу вам помочь?", "upload_label": "Загрузите свои заметки", "success_upload": "Файл успешно загружен!", "create_group": "Создать новую группу"}
}

# --- 3. BOČNÁ LIŠTA (SIDEBAR) - MUSÍ BYŤ NA ZAČIATKU ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    lang = st.selectbox("Language / Jazyk", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    # Domov tlačidlo
    if st.button(t["home"], use_container_width=True):
        # Tvoj link z Frameru
        hlavna_adresa = "https://silent-terms-318372.framer.app/"
        js = f"window.parent.location.href = '{hlavna_adresa}';"
        components.html(f"<script>{js}</script>", height=0)
        st.query_params.clear()
        st.rerun()

    st.divider()
    
    # Navigačné tlačidlá - Tieto tu budú VŽDY
    if st.button(t["chat_title"], use_container_width=True):
        st.query_params.p = "chat"
        st.rerun()
    if st.button(t["forum_title"], use_container_width=True):
        st.query_params.p = "forum"
        st.rerun()
    if st.button(t["groups_title"], use_container_width=True):
        st.query_params.p = "groups"
        st.rerun()

# --- 4. LOGIKA ZOBRAZOVANIA OBSAHU ---
query_params = st.query_params
selected_page = query_params.get("p", None)

if selected_page is None:
    # Ak nie je nič vybraté, zobrazíme len prázdne miesto (aby to nekazilo úvod webu)
    st.write("") 
    st.stop()

if selected_page == "chat":
    st.title(t["chat_title"])
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input(t["input_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = f"Simulovaná odpoveď ({lang}): {prompt}"
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

elif selected_page == "forum":
    st.title(t["forum_title"])
    uploaded_file = st.file_uploader(t["upload_label"], type=['pdf', 'png', 'jpg'])
    if uploaded_file:
        st.success(t["success_upload"])

elif selected_page == "groups":
    st.title(t["groups_title"])
    nazov_skupiny = st.text_input("Name")
    if st.button(t["create_group"]):
        st.balloons()
        st.success(f"Skupina '{nazov_skupiny}' vytvorená!")
