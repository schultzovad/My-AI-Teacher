import streamlit as st
import streamlit.components.v1 as components

# --- 1. NASTAVENIA (Tvoj základ) ---
st.set_page_config(page_title="EduHub AI Tutor", layout="wide", page_icon="🎓")

# --- CSS (DÔLEŽITÉ: Toto zabezpečí plynulý posun vnútri Streamlitu) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    html { scroll-behavior: smooth; } 
    </style>
    """, unsafe_allow_html=True)

# --- 2. SLOVNÍK (Tvojich 8 jazykov - nezmenené) ---
lang_data = {
    "SK": {"nav_title": "Navigácia", "home": " Domov", "chat_title": " AI Tutor", "forum_title": " Študijné materiály", "groups_title": " Študijné skupiny", "input_placeholder": "S čím ti dnes pomôžem?", "upload_label": "Nahraj svoje poznámky", "success_upload": "Súbor bol úspešne nahraný!", "create_group": "Vytvoriť novú skupinu"},
    "EN": {"nav_title": "Navigation", "home": " Home", "chat_title": " AI Tutor", "forum_title": " Study Materials", "groups_title": " Study Groups", "input_placeholder": "How can I help you today?", "upload_label": "Upload your notes", "success_upload": "File uploaded successfully!", "create_group": "Create new group"},
    "DE": {"nav_title": "Navigation", "home": " Startseite", "chat_title": " AI Tutor", "forum_title": " Lernmaterialien", "groups_title": " Studiengruppen", "input_placeholder": "Wie kann ich dir helfen?", "upload_label": "Notizen hochladen", "success_upload": "Datei erfolgreich hochgeladen!", "create_group": "Neue Gruppe erstellen"},
    "ES": {"nav_title": "Navegación", "home": " Inicio", "chat_title": " Tutor AI", "forum_title": " Materiales de estudio", "groups_title": " Grupos de estudio", "input_placeholder": "¿Cómo te puedo ayudar?", "upload_label": "Subir notas", "success_upload": "¡Archivo subido con éxito!", "create_group": "Crear nuevo grupo"},
    "FR": {"nav_title": "Navigation", "home": " Accueil", "chat_title": " Tuteur IA", "forum_title": " Matériels d'étude", "groups_title": " Groupes d'étude", "input_placeholder": "Comment puis-je vous aider ?", "upload_label": "Télécharger vos notes", "success_upload": "Fichier téléchargé avec succès !", "create_group": "Crear un nouveau groupe"},
    "IT": {"nav_title": "Navigazione", "home": " Home", "chat_title": " Tutor IA", "forum_title": " Materiali di studio", "groups_title": " Gruppi di studio", "input_placeholder": "Come posso aiutarti?", "upload_label": "Carica le tue note", "success_upload": "File caricato con successo!", "create_group": "Crea nuovo gruppo"},
    "UA": {"nav_title": "Навігація", "home": " Головна", "chat_title": " AI Тьютор", "forum_title": " Навчальні матеріали", "groups_title": " Навчальні групи", "input_placeholder": "Чим я можу вам допомогти?", "upload_label": "Завантажте свої нотатки", "success_upload": "Файл успішно завантажено!", "create_group": "Створити нову групу"},
    "RU": {"nav_title": "Навигация", "home": " Главная", "chat_title": " AI Тьютор", "forum_title": " Учебные материалы", "groups_title": " Учебные группы", "input_placeholder": "Чем я могу вам помочь?", "upload_label": "Загрузите свои заметки", "success_upload": "Файл успешно загружен!", "create_group": "Создать новую группу"}
}

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title(" EduHub Menu")
    lang = st.selectbox("Language / Jazyk", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    if st.button(t["home"], use_container_width=True):
        hlavna_adresa = "https://silent-terms-318372.framer.app/"
        js = f"window.parent.location.href = '{hlavna_adresa}';"
        components.html(f"<script>{js}</script>", height=0)
        st.stop()

    st.divider()
    
    # Tlačidlá v sidebare teraz fungujú ako "skoky" na sekciu
    if st.button(t["chat_title"], use_container_width=True):
        js = "window.location.hash = 'ai-tutor';"
        components.html(f"<script>{js}</script>", height=0)
    if st.button(t["forum_title"], use_container_width=True):
        js = "window.location.hash = 'forum';"
        components.html(f"<script>{js}</script>", height=0)
    if st.button(t["groups_title"], use_container_width=True):
        js = "window.location.hash = 'groups';"
        components.html(f"<script>{js}</script>", height=0)

# --- 4. OBSAH (Všetko pod sebou, aby to Framer Scroll našiel) ---

# --- SEKCIA: AI TUTOR ---
st.markdown('<div id="ai-tutor"></div>', unsafe_allow_html=True)
st.title(t["chat_title"])
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input(t["input_placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        response = f"Simulovaná odpoveď: {prompt}"
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()

# --- SEKCIA: FÓRUM ---
st.markdown('<div id="forum" style="padding-top: 20px;"></div>', unsafe_allow_html=True)
st.title(t["forum_title"])
uploaded_file = st.file_uploader(t["upload_label"], type=['pdf', 'png', 'jpg'])
if uploaded_file:
    st.success(t["success_upload"])

st.divider()

# --- SEKCIA: SKUPINY ---
st.markdown('<div id="groups" style="padding-top: 20px;"></div>', unsafe_allow_html=True)
st.title(t["groups_title"])
nazov_skupiny = st.text_input("Name")
if st.button(t["create_group"]):
    st.balloons()
    st.success(f"Skupina '{nazov_skupiny}' vytvorená!")
