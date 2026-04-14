import streamlit as st

# --- 1. NASTAVENIA STRÁNKY ---
st.set_page_config(page_title="EduHub AI Tutor", layout="wide", page_icon="🎓")

# --- 2. PREKLADOVÝ SLOVNÍK ---
lang_data = {
    "SK": {
        "nav_title": "Navigácia",
        "chat_title": "🤖 AI Tutor",
        "forum_title": "📚 Študijné materiály",
        "groups_title": "👥 Študijné skupiny",
        "input_placeholder": "S čím ti dnes pomôžem?",
        "upload_label": "Nahraj svoje poznámky",
        "success_upload": "Súbor bol úspešne nahraný!",
        "create_group": "Vytvoriť novú skupinu"
    },
    "EN": {
        "nav_title": "Navigation",
        "chat_title": "🤖 AI Tutor",
        "forum_title": "📚 Study Materials",
        "groups_title": "👥 Study Groups",
        "input_placeholder": "How can I help you today?",
        "upload_label": "Upload your notes",
        "success_upload": "File uploaded successfully!",
        "create_group": "Create new group"
    },
    "DE": {
        "nav_title": "Navigation",
        "chat_title": "🤖 AI Tutor",
        "forum_title": "📚 Lernmaterialien",
        "groups_title": "👥 Studiengruppen",
        "input_placeholder": "Wie kann ich dir helfen?",
        "upload_label": "Notizen hochladen",
        "success_upload": "Datei erfolgreich hochgeladen!",
        "create_group": "Neue Gruppe erstellen"
    },
    "ES": {
        "nav_title": "Navegación",
        "chat_title": "🤖 Tutor AI",
        "forum_title": "📚 Materiales de estudio",
        "groups_title": "👥 Grupos de estudio",
        "input_placeholder": "¿Cómo te puedo ayudar?",
        "upload_label": "Subir notas",
        "success_upload": "¡Archivo subido con éxito!",
        "create_group": "Crear nuevo grupo"
    }
}

# --- 3. BOČNÁ LIŠTA (SIDEBAR) PRE NAVIGÁCIU ---
# Toto vyrieši tvoj problém s preklikávaním!
with st.sidebar:
    st.title("🎓 EduHub Menu")
    
    # Výber jazyka
    lang = st.selectbox("Language / Jazyk", ["SK", "EN", "DE", "ES"])
    t = lang_data[lang]
    
    st.divider()
    st.subheader(t["nav_title"])
    
    # Tlačidlá, ktoré prepínajú sekcie priamo v okne
    if st.button(t["chat_title"], use_container_width=True):
        st.query_params.p = "chat"
        st.rerun()
    if st.button(t["forum_title"], use_container_width=True):
        st.query_params.p = "forum"
        st.rerun()
    if st.button(t["groups_title"], use_container_width=True):
        st.query_params.p = "groups"
        st.rerun()

# --- 4. LOGIKA STRÁNOK ---
query_params = st.query_params
selected_page = query_params.get("p", "chat")

# SEKCIA: CHAT
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
            response = f"Odpoveď v jazyku {lang}: Rozumiem vašej požiadavke '{prompt}'."
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# SEKCIA: FÓRUM
elif selected_page == "forum":
    st.title(t["forum_title"])
    uploaded_file = st.file_uploader(t["upload_label"], type=['pdf', 'png', 'jpg'])
    if uploaded_file:
        st.success(t["success_upload"])
    st.info("Tu sa čoskoro objavia príspevky od spolužiakov.")

# SEKCIA: SKUPINY
elif selected_page == "groups":
    st.title(t["groups_title"])
    st.subheader(t["create_group"])
    nazov = st.text_input("Názov skupiny")
    if st.button("Vytvoriť"):
        st.balloons()
        st.success(f"Skupina {nazov} vytvorená!")

# OŠETRENIE CHYBY
else:
    st.error("Sekcia sa nenašla. Použi menu vľavo.")
