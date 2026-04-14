import streamlit as st
import streamlit.components.v1 as components

# --- 1. ZÁKLADNÉ NASTAVENIA ---
st.set_page_config(page_title="EduHub AI Tutor", layout="wide", page_icon="🎓")

# --- 2. KOMPLETNÝ SLOVNÍK (8 JAZYKOV) ---
lang_data = {
    "SK": {"h": "🏠 Domov", "c": "🤖 AI Tutor", "f": "📚 Študijné materiály", "g": "👥 Študijné skupiny", "i": "S čím ti dnes pomôžem?", "u": "Nahraj svoje poznámky", "s": "Súbor bol úspešne nahraný!", "n": "Vytvoriť novú skupinu"},
    "EN": {"h": "🏠 Home", "c": "🤖 AI Tutor", "f": "📚 Study Materials", "g": "👥 Study Groups", "i": "How can I help you today?", "u": "Upload your notes", "s": "File uploaded successfully!", "n": "Create new group"},
    "DE": {"h": "🏠 Startseite", "c": "🤖 AI Tutor", "f": "📚 Lernmaterialien", "g": "👥 Studiengruppen", "i": "Wie kann ich dir helfen?", "u": "Notizen hochladen", "s": "Datei erfolgreich hochgeladen!", "n": "Neue Gruppe erstellen"},
    "ES": {"h": "🏠 Inicio", "c": "🤖 Tutor AI", "f": "📚 Materiales de estudio", "g": "👥 Grupos de estudio", "i": "¿Cómo te puedo ayudar?", "u": "Subir notas", "s": "¡Archivo subido con éxito!", "n": "Crear nuevo grupo"},
    "FR": {"h": "🏠 Accueil", "c": "🤖 Tuteur IA", "f": "📚 Matériels d'étude", "g": "👥 Groupes d'étude", "i": "Comment puis-je vous aider ?", "u": "Télécharger vos notes", "s": "Fichier téléchargé avec succès !", "n": "Créez un nouveau groupe"},
    "IT": {"h": "🏠 Home", "c": "🤖 Tutor IA", "f": "📚 Materiali di studio", "g": "👥 Gruppi di studio", "i": "Come posso aiutarti?", "u": "Carica le tue note", "s": "File caricato con successo!", "n": "Crea nuovo gruppo"},
    "UA": {"h": "🏠 Головна", "c": "🤖 AI Тьютор", "f": "📚 Навчальні матеріали", "g": "👥 Навчальні групи", "i": "Чим я можу вам допомогти?", "u": "Завантажте свої нотатки", "s": "Файл успішно завантажено!", "n": "Створити нову групу"},
    "RU": {"h": "🏠 Главная", "c": "🤖 AI Тьютор", "f": "📚 Учебные материалы", "g": "👥 Учебные группы", "i": "Чем я могу вам помочь?", "u": "Загрузите свои заметки", "s": "Файл успешно загружен!", "n": "Создать новую группу"}
}

# --- 3. BOČNÁ LIŠTA (SIDEBAR) ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    
    # Výber jazyka
    lang = st.selectbox("Language / Jazyk", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    # Tlačidlo DOMOV (Návrat na hlavnú stránku Frameru)
    if st.button(t["h"], use_container_width=True):
        hlavna_adresa = "https://silent-terms-318372.framer.app/"
        js = f"window.parent.location.href = '{hlavna_adresa}';"
        components.html(f"<script>{js}</script>", height=0)
        st.stop()

    st.divider()
    
    # Navigačné tlačidlá v bočnom menu
    if st.button(t["c"], use_container_width=True):
        st.query_params.p = "chat"
        st.rerun()
    if st.button(t["f"], use_container_width=True):
        st.query_params.p = "forum"
        st.rerun()
    if st.button(t["g"], use_container_width=True):
        st.query_params.p = "groups"
        st.rerun()

# --- 4. LOGIKA STRÁNOK ---
query_params = st.query_params
selected_page = query_params.get("p", "chat")

if selected_page == "chat":
    st.title(t["c"])
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input(t["i"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = f"Simulovaná odpoveď ({lang}): Rozumiem, analyzujem vaše poznámky."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

elif selected_page == "forum":
    st.title(t["f"])
    uploaded_file = st.file_uploader(t["u"], type=['pdf', 'png', 'jpg'])
    if uploaded_file:
        st.success(t["s"])

elif selected_page == "groups":
    st.title(t["g"])
    nazov_skupiny = st.text_input("Názov skupiny / Group Name")
    if st.button(t["n"]):
        st.balloons()
        st.success(f"Skupina '{nazov_skupiny}' vytvorená!")
