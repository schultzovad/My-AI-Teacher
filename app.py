import streamlit as st
import streamlit.components.v1 as components

# --- 1. NASTAVENIA ---
st.set_page_config(page_title="EduHub AI Tutor", layout="wide", page_icon="🎓")

# --- 2. KOMPLETNÝ SLOVNÍK ---
lang_data = {
    "SK": {"h": "🏠 Domov", "c": "🤖 AI Tutor", "f": "📚 Študijné materiály", "g": "👥 Študijné skupiny", "i": "S čím ti dnes pomôžem?", "u": "Nahraj svoje poznámky", "s": "Súbor bol úspešne nahraný!", "n": "Vytvoriť novú skupinu"},
    "EN": {"h": "🏠 Home", "c": "🤖 AI Tutor", "f": "📚 Study Materials", "g": "👥 Study Groups", "i": "How can I help you today?", "u": "Upload your notes", "s": "File uploaded successfully!", "n": "Create new group"},
    "UA": {"h": "🏠 Головна", "c": "🤖 AI Тьютор", "f": "📚 Навчальні матеріали", "g": "👥 Навчальні групи", "i": "Чим я можу вам допомогти?", "u": "Завантажте свої нотатки", "s": "Файл успішно завантажено!", "n": "Створити нову групу"}
}

# --- JS POISTKA (TOTO OPRAVÍ TO PREPÍNANIE) ---
# Tento kúsok kódu sleduje, či sa zmenila URL v prehliadači a povie Streamlitu, aby sa prebral
components.html("""
<script>
    var lastUrl = window.parent.location.href;
    setInterval(function() {
        var currentUrl = window.parent.location.href;
        if (currentUrl !== lastUrl) {
            lastUrl = currentUrl;
            window.location.reload();
        }
    }, 500);
</script>
""", height=0)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    lang = st.selectbox("Language / Jazyk", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    if st.button(t["h"], use_container_width=True):
        components.html(f"<script>window.parent.location.href = 'https://silent-terms-318372.framer.app/';</script>", height=0)
        st.stop()

    if st.button(t["c"], use_container_width=True):
        st.query_params.p = "chat"; st.rerun()
    if st.button(t["f"], use_container_width=True):
        st.query_params.p = "forum"; st.rerun()
    if st.button(t["g"], use_container_width=True):
        st.query_params.p = "groups"; st.rerun()

# --- 4. LOGIKA STRÁNOK ---
query_params = st.query_params
selected_page = query_params.get("p", None)

if selected_page is None:
    st.stop()

if selected_page == "chat":
    st.title(t["c"])
    if "messages" not in st.session_state: st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])
    if prompt := st.chat_input(t["i"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        response = f"Simulovaná odpoveď: Analyzujem vaše zadanie."
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

elif selected_page == "forum":
    st.title(t["f"])
    st.file_uploader(t["u"], type=['pdf', 'png', 'jpg'])

elif selected_page == "groups":
    st.title(t["g"])
    st.text_input("Name")
    if st.button(t["n"]): st.balloons()
