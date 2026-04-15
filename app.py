import streamlit as st

# --- NASTAVENIA STRÁNKY ---
st.set_page_config(page_title="EduHub AI", layout="wide", page_icon="🎓")

# --- KOMPLETNÝ PREKLADOVÝ SLOVNÍK ---
lang_data = {
    "SK": {
        "chat_title": "🤖 AI Tutor",
        "forum_title": "📚 Študijné materiály",
        "groups_title": "👥 Študijné skupiny",
        "input_placeholder": "S čím ti dnes pomôžem?",
        "upload_label": "Nahraj svoje poznámky",
        "success_upload": "Súbor bol úspešne nahraný!",
        "create_group": "Vytvoriť novú skupinu",
        "lang_label": "Vyber si jazyk"
    },
    "EN": {
        "chat_title": "🤖 AI Tutor",
        "forum_title": "📚 Study Materials",
        "groups_title": "👥 Study Groups",
        "input_placeholder": "How can I help you today?",
        "upload_label": "Upload your notes",
        "success_upload": "File uploaded successfully!",
        "create_group": "Create new group",
        "lang_label": "Choose language"
    },
    "DE": {
        "chat_title": "🤖 AI Tutor",
        "forum_title": "📚 Lernmaterialien",
        "groups_title": "👥 Studiengruppen",
        "input_placeholder": "Wie kann ich dir heute helfen?",
        "upload_label": "Notizen hochladen",
        "success_upload": "Datei erfolgreich hochgeladen!",
        "create_group": "Neue Gruppe erstellen",
        "lang_label": "Sprache wählen"
    },
    "ES": {
        "chat_title": "🤖 AI Tutor",
        "forum_title": "📚 Materiales de estudio",
        "groups_title": "👥 Grupos de estudio",
        "input_placeholder": "¿Cómo te puedo ayudar hoy?",
        "upload_label": "Subir notas",
        "success_upload": "¡Archivo subido con éxito!",
        "create_group": "Crear nuevo grupo",
        "lang_label": "Elegir idioma"
    }
}

# --- SIDEBAR (Bočná lišta pre výber jazyka) ---
with st.sidebar:
    lang = st.selectbox("Language / Jazyk", ["SK", "EN", "DE", "ES"])
    st.divider()
    st.write(lang_data[lang]["lang_label"])

texts = lang_data[lang]

# --- LOGIKA NAVIGÁCIE ---
query_params = st.query_params
selected_page = query_params.get("p", "chat")

# --- 1. SEKCIA: AI TUTOR ---
if selected_page == "chat":
    st.title(texts["chat_title"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(texts["input_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Tu je tvoja AI odpoveď
            response = f"Simulovaná odpoveď ({lang}): Rozumiem, tvoja otázka je: '{prompt}'."
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- 2. SEKCIA: FÓRUM ---
elif selected_page == "forum":
    st.title(texts["forum_title"])
    uploaded_file = st.file_uploader(texts["upload_label"], type=['pdf', 'png', 'jpg'])
    if uploaded_file:
        st.success(texts["success_upload"])

# --- 3. SEKCIA: SKUPINY ---
elif selected_page == "groups":
    st.title(texts["groups_title"])
    st.subheader(texts["create_group"])
    nazov = st.text_input("Názov / Name")
    if st.button("Vytvoriť / Create"):
        st.balloons()

# --- OŠETRENIE CHYBY ---
else:
    st.error(f"Sekcia '{selected_page}' sa nenašla. Skontroluj link vo Frameri!")
    
