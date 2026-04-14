import streamlit as st

# --- NASTAVENIA STRÁNKY ---
st.set_page_config(page_title="EduHub AI", layout="wide", page_icon="🎓")

# --- PREKLADOVÝ SLOVNÍK ---
lang_data = {
    "SK": {
        "chat_title": "🤖 AI Tutor",
        "forum_title": "📚 Študijné materiály",
        "groups_title": "👥 Študijné skupiny",
        "input_placeholder": "S čím ti dnes pomôžem?",
        "upload_label": "Nahraj svoje poznámky",
        "success_upload": "Súbor bol úspešne nahraný!",
        "create_group": "Vytvoriť novú skupinu"
    },
    "EN": {
        "chat_title": "🤖 AI Tutor",
        "forum_title": "📚 Study Materials",
        "groups_title": "👥 Study Groups",
        "input_placeholder": "How can I help you today?",
        "upload_label": "Upload your notes",
        "success_upload": "File uploaded successfully!",
        "create_group": "Create new group"
    }
}

# --- VÝBER JAZYKA (V SIDEBARE ALEBO NAVRHU) ---
lang = st.selectbox("Jazyk / Language", ["SK", "EN"])
texts = lang_data[lang]

# --- LOGIKA NAVIGÁCIE (PARAMETRE Z FRAMERU) ---
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
            response = f"Odpoveď na: {prompt}"
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
    if st.button("OK"):
        st.balloons()

else:
    st.error("Section not found.")
