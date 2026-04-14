import streamlit as st

# --- 1. NASTAVENIA STRÁNKY (Natívne správanie) ---
st.set_page_config(
    page_title="EduHub AI", 
    layout="wide", 
    page_icon="🎓",
    initial_sidebar_state="expanded" # Toto zabezpečí, že lišta je na začiatku vonku
)

# --- 2. CSS OPRAVA (Skrytie hlavičky a úprava medzier) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Toto zabezpečí, že šípka bude mať štandardnú farbu a pozíciu */
    [data-testid="collapsedControl"] {
        color: #31333F;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KOMPLETNÝ PREKLADOVÝ SLOVNÍK (8 jazykov) ---
lang_data = {
    "SK": {"chat_title": "🤖 AI Tutor", "forum_title": "📚 Študijné materiály", "groups_title": "👥 Študijné skupiny", "input_placeholder": "S čím ti dnes pomôžem?", "upload_label": "Nahraj svoje poznámky", "success_upload": "Súbor úspešne nahraný!", "create_group": "Vytvoriť novú skupinu"},
    "EN": {"chat_title": "🤖 AI Tutor", "forum_title": "📚 Study Materials", "groups_title": "👥 Study Groups", "input_placeholder": "How can I help you?", "upload_label": "Upload notes", "success_upload": "File uploaded!", "create_group": "Create group"},
    "DE": {"chat_title": "🤖 AI Tutor", "forum_title": "📚 Lernmaterialien", "groups_title": "👥 Studiengruppen", "input_placeholder": "Wie kann ich helfen?", "upload_label": "Notizen hochladen", "success_upload": "Erfolgreich!", "create_group": "Gruppe erstellen"},
    "ES": {"chat_title": "🤖 AI Tutor", "forum_title": "📚 Materiales de estudio", "groups_title": "👥 Grupos de estudio", "input_placeholder": "¿Cómo te ayudo?", "upload_label": "Subir notas", "success_upload": "¡Éxito!", "create_group": "Crear grupo"},
    "FR": {"chat_title": "🤖 Tuteur IA", "forum_title": "📚 Matériels d'étude", "groups_title": "👥 Groupes d'étude", "input_placeholder": "Comment puis-je aider?", "upload_label": "Télécharger notes", "success_upload": "Succès!", "create_group": "Créer un groupe"},
    "IT": {"chat_title": "🤖 Tutor IA", "forum_title": "📚 Materiali di studio", "groups_title": "👥 Gruppi di studio", "input_placeholder": "Come posso aiutarti?", "upload_label": "Carica note", "success_upload": "Caricato!", "create_group": "Crea gruppo"},
    "UA": {"chat_title": "🤖 AI Тьютор", "forum_title": "📚 Навчальні матеріаli", "groups_title": "👥 Навчальні групи", "input_placeholder": "Чim я можу допомогти?", "upload_label": "Завантажити нотатки", "success_upload": "Успішно!", "create_group": "Створити групу"},
    "RU": {"chat_title": "🤖 AI Тьютор", "forum_title": "📚 Учебные материалы", "groups_title": "👥 Учебные группы", "input_placeholder": "Чем я могу помочь?", "upload_label": "Загрузить заметки", "success_upload": "Успешно!", "create_group": "Создать группу"}
}

# --- 4. SIDEBAR (Výber jazyka a navigácia) ---
with st.sidebar:
    st.title("🎓 EduHub")
    lang = st.selectbox("Language / Jazyk", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    # Pridáme prepínač stránok priamo do lišty (istota, ak by URL nefungovala)
    choice = st.radio("Menu", [t["chat_title"], t["forum_title"], t["groups_title"]])

# --- 5. LOGIKA NAVIGÁCIE (Podľa tvojho vzoru) ---
# Skontrolujeme parametre v URL, ak nie sú, použijeme výber z lišty
query_params = st.query_params
url_page = query_params.get("p", "")

if url_page == "forum" or choice == t["forum_title"]:
    st.title(t["forum_title"])
    uploaded_file = st.file_uploader(t["upload_label"], type=['pdf', 'png', 'jpg'])
    if uploaded_file: st.success(t["success_upload"])

elif url_page == "groups" or choice == t["groups_title"]:
    st.title(t["groups_title"])
    st.subheader(t["create_group"])
    st.text_input("Názov / Name")
    if st.button("Vytvoriť / Create"): st.balloons()

else: # Default je AI Chat
    st.title(t["chat_title"])
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if prompt := st.chat_input(t["input_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        response = f"Simulovaná odpoveď ({lang}): Rozumiem."
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
