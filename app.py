import streamlit as st
import streamlit.components.v1 as components

# --- 1. NASTAVENIA STRÁNKY ---
st.set_page_config(
    page_title="EduHub", 
    layout="wide", 
    page_icon="🎓"
)

# --- 2. CSS OPRAVY (ODSTRÁNENIE BIELYCH MIEST) ---
st.markdown("""
    <style>
    /* Posunie celú aplikáciu vyššie, aby nebola pod textom diera */
    .stApp {
        margin-top: -80px;
    }
    /* Skryje nepotrebné lišty a logá Streamlitu */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Zruší vnútorné okraje boxu */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SLOVNÍK JAZYKOV (VŠETKÝCH 8) ---
lang_data = {
    "SK": {"h": "🏠 Domov", "c": "🤖 AI Tutor", "f": "📚 Študijné materiály", "g": "👥 Študijné skupiny", "i": "S čím ti dnes pomôžem?", "u": "Nahraj svoje poznámky", "n": "Vytvoriť novú skupinu"},
    "EN": {"h": "🏠 Home", "c": "🤖 AI Tutor", "f": "📚 Study Materials", "g": "👥 Study Groups", "i": "How can I help you today?", "u": "Upload your notes", "n": "Create new group"},
    "DE": {"h": "🏠 Startseite", "c": "🤖 AI Tutor", "f": "📚 Lernmaterialien", "g": "👥 Studiengruppen", "i": "Wie kann ich dir helfen?", "u": "Notizen hochladen", "n": "Neue Gruppe erstellen"},
    "ES": {"h": "🏠 Inicio", "c": "🤖 Tutor AI", "f": "📚 Materiales de estudio", "g": "👥 Grupos de estudio", "i": "¿Cómo te puedo ayudar?", "u": "Subir notas", "n": "Crear nuevo grupo"},
    "FR": {"h": "🏠 Accueil", "c": "🤖 Tuteur IA", "f": "📚 Matériels d'étude", "g": "👥 Groupes d'étude", "i": "Comment puis-je vous aider ?", "u": "Télécharger vos notes", "s": "Fichier téléchargé!", "n": "Créer un nouveau groupe"},
    "IT": {"h": "🏠 Home", "c": "🤖 Tutor IA", "f": "📚 Materiali di studio", "g": "👥 Gruppi di studio", "i": "Come posso aiutarti?", "u": "Carica le tue note", "n": "Crea nuovo gruppo"},
    "UA": {"h": "🏠 Головна", "c": "🤖 AI Тьютор", "f": "📚 Навчальні матеріали", "g": "👥 Навчальні групи", "i": "Чим я можу вам допомогти?", "u": "Завантажте свої нотатки", "n": "Створити нову групу"},
    "RU": {"h": "🏠 Главная", "c": "🤖 AI Тьютор", "f": "📚 Учебные материалы", "g": "👥 Учебные группы", "i": "Чем я могу вам помочь?", "u": "Загрузите свои заметки", "n": "Создать новую группу"}
}

# --- 4. BOČNÁ LIŠTA (NAVIGÁCIA) ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    lang = st.selectbox("Language / Jazyk", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    # Tlačidlo Domov - Tu si prepíš adresu ak sa tvoj web zmení
    if st.button(t["h"], use_container_width=True):
        moj_framer_web = "https://silent-terms-318372.framer.app/"
        components.html(f"<script>window.top.location.href = '{moj_framer_web}';</script>", height=0)
        st.stop()

    st.divider()
    # Výber sekcie
    page_selection = st.radio("Sekcia", [t["c"], t["f"], t["g"]])

# --- 5. ZOBRAZENIE OBSAHU ---
if page_selection == t["c"]:
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
            response = "Analyzujem vaše zadanie..."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

elif page_selection == t["f"]:
    st.title(t["f"])
    st.write(t["u"])
    st.file_uploader("", type=['pdf', 'png', 'jpg'])

elif page_selection == t["g"]:
    st.title(t["g"])
    nazov_skupiny = st.text_input("Názov skupiny")
    if st.button(t["n"]):
        st.balloons()
        st.success(f"Skupina '{nazov_skupiny}' vytvorená!")
