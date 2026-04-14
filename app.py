import streamlit as st
import streamlit.components.v1 as components

# --- 1. ZÁKLADNÉ NASTAVENIA ---
st.set_page_config(
    page_title="EduHub", 
    layout="wide", 
    page_icon="🎓"
)

# --- 2. SLOVNÍK (JAZYKY) ---
lang_data = {
    "SK": {"h": "🏠 Domov", "c": "🤖 AI Tutor", "f": "📚 Študijné materiály", "g": "👥 Študijné skupiny", "i": "S čím ti dnes pomôžem?"},
    "EN": {"h": "🏠 Home", "c": "🤖 AI Tutor", "f": "📚 Study Materials", "g": "👥 Study Groups", "i": "How can I help you today?"},
    "UA": {"h": "🏠 Головна", "c": "🤖 AI Тьютор", "f": "📚 Навчальні матеріали", "g": "👥 Навчальні групи", "i": "Чим я можу вам допомогти?"}
}

# --- 3. BOČNÁ LIŠTA (SIDEBAR) ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    lang = st.selectbox("Language", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    # TLAČIDLO DOMOV - TU SI UPRAV SVOJU URL
    if st.button(t["h"], use_container_width=True):
        # SEM VLOŽ SVOJU PRESNÚ ADRESU WEBU
        moj_web = "https://silent-terms-318372.framer.app/"
        
        components.html(f"""
            <script>
                window.top.location.href = "{moj_web}";
            </script>
        """, height=0)
        st.stop()

    st.divider()
    # Výber sekcie
    page_selection = st.radio("Menu", [t["c"], t["f"], t["g"]])

# --- 4. LOGIKA SKRÝVANIA (DÔLEŽITÉ!) ---
# Ak nie je v URL parameter "p", Streamlit nebude vidno (nezakryje ti Home)
if not st.query_params.get("p"):
    st.stop()

# --- 5. ZOBRAZENIE OBSAHU ---
if page_selection == t["c"]:
    st.title(t["c"])
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if prompt := st.chat_input(t["i"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        res = "Analyzujem vaše poznámky..."
        with st.chat_message("assistant"): st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

elif page_selection == t["f"]:
    st.title(t["f"])
    st.file_uploader("Nahraj súbor", type=['pdf', 'png', 'jpg'])

elif page_selection == t["g"]:
    st.title(t["g"])
    st.text_input("Názov novej skupiny")
    if st.button("Vytvoriť skupinu"): st.balloons()
