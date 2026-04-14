import streamlit as st
import streamlit.components.v1 as components

# --- 1. NASTAVENIA ---
st.set_page_config(page_title="EduHub AI Tutor", layout="wide", page_icon="🎓")

# --- 2. SLOVNÍK ---
lang_data = {
    "SK": {"h": "🏠 Domov", "c": "🤖 AI Tutor", "f": "📚 Študijné materiály", "g": "👥 Študijné skupiny", "i": "S čím ti dnes pomôžem?", "u": "Nahraj svoje poznámky", "s": "Súbor bol úspešne nahraný!", "n": "Vytvoriť novú skupinu"},
    "EN": {"h": "🏠 Home", "c": "🤖 AI Tutor", "f": "📚 Study Materials", "g": "👥 Study Groups", "i": "How can I help you today?", "u": "Upload your notes", "s": "File uploaded successfully!", "n": "Create new group"},
    "UA": {"h": "🏠 Головна", "c": "🤖 AI Тьютор", "f": "📚 Навчальні матеріали", "g": "👥 Навчальні групи", "i": "Чим я можу вам допомогти?", "u": "Завантажте свої нотатки", "s": "Файл успішно завантажено!", "n": "Створити нову групу"}
}

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎓 EduHub Menu")
    lang = st.selectbox("Jazyk", list(lang_data.keys()))
    t = lang_data[lang]
    st.divider()
    
    # Tlačidlo Domov - vráti ťa na čistú URL bez parametrov
    if st.button(t["h"], use_container_width=True):
        hlavna_adresa = "https://silent-terms-318372.framer.app/"
        components.html(f"<script>window.parent.location.href = '{hlavna_adresa}';</script>", height=0)
        st.stop()

    if st.button(t["c"], use_container_width=True):
        st.query_params.p = "chat"; st.rerun()
    if st.button(t["f"], use_container_width=True):
        st.query_params.p = "forum"; st.rerun()
    if st.button(t["g"], use_container_width=True):
        st.query_params.p = "groups"; st.rerun()

# --- 4. LOGIKA "NEVIDITEĽNOSTI" ---
query_params = st.query_params
selected_page = query_params.get("p", None)

# AK JE STRÁNKA PRÁZDNA (užívateľ práve prišiel na web)
if selected_page is None:
    # Tu sa nezobrazí vôbec nič, takže vo Frameri nebude biela plocha
    st.stop()

# AK JE VYBRANÝ CHAT
elif selected_page == "chat":
    st.title(t["c"])
    if "m" not in st.session_state: st.session_state.m = []
    for m in st.session_state.m:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if p := st.chat_input(t["i"]):
        st.session_state.m.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        r = f"Analyzujem: {p}"
        with st.chat_message("assistant"): st.markdown(r)
        st.session_state.m.append({"role": "assistant", "content": r})

# AK JE VYBRANÉ FÓRUM
elif selected_page == "forum":
    st.title(t["f"])
    st.file_uploader(t["u"])

# AK SÚ VYBRANÉ SKUPINY
elif selected_page == "groups":
    st.title(t["g"])
    st.text_input("Názov skupiny")
    if st.button(t["n"]): st.balloons()
