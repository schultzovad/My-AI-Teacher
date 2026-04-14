import streamlit as st

# --- NASTAVENIA STRÁNKY ---
st.set_page_config(
    page_title="EduHub AI", 
    layout="wide", 
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

# --- CSS OPRAVA: TOTO VYTIAHNE ŠÍPKU VON ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* VYTIAHNUTIE ŠÍPKY VON Z OKRAJA */
    [data-testid="collapsedControl"] {
        left: 20px !important;    /* Posun od ľavého okraja, aby ju Framer neorezal */
        top: 20px !important;     /* Posun zhora */
        background-color: white !important;
        border-radius: 50% !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important; /* Tieň, aby bola vidieť */
        z-index: 999999 !important;
        display: flex !important;
        visibility: visible !important;
    }
    
    /* Zabezpečíme, aby obsah nebol nalepený pod šípkou */
    .block-container {
        padding-top: 3.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PREKLADOVÝ SLOVNÍK (Tvoj pôvodný) ---
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
    }
}

# --- SIDEBAR ---
with st.sidebar:
    lang = st.selectbox("Language / Jazyk", list(lang_data.keys()))
    st.divider()
    choice = st.radio("Menu", [lang_data[lang]["chat_title"], lang_data[lang]["forum_title"], lang_data[lang]["groups_title"]])

texts = lang_data[lang]

# --- LOGIKA NAVIGÁCIE ---
query_params = st.query_params
selected_page = query_params.get("p", "chat")

# --- ZOBRAZENIE OBSAHU ---
if selected_page == "forum" or choice == texts["forum_title"]:
    st.title(texts["forum_title"])
    uploaded_file = st.file_uploader(texts["upload_label"], type=['pdf', 'png', 'jpg'])
    if uploaded_file: st.success(texts["success_upload"])

elif selected_page == "groups" or choice == texts["groups_title"]:
    st.title(texts["groups_title"])
    st.subheader(texts["create_group"])
    st.text_input("Názov / Name")
    if st.button("Vytvoriť / Create"): st.balloons()

else:
    st.title(texts["chat_title"])
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if prompt := st.chat_input(texts["input_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        response = "Rozumiem."
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
