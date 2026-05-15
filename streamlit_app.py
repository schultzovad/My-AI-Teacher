import streamlit as st
import google.generativeai as genai
import pypdf
import docx
from PIL import Image

# 1. NASTAVENIE API
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ API kľúč chýba v Secrets!")
    st.stop()

genai.configure(api_key=api_key)

# SKÚSME TENTO NÁZOV - je najuniverzálnejší
MODEL_NAME = 'gemini-1.5-flash'

try:
    model_ai = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"Chyba pri inicializácii: {e}")

# --- INICIALIZÁCIA ---
if "m" not in st.session_state: st.session_state.m = []
if "doc_content" not in st.session_state: st.session_state.doc_content = ""

# 2. JAZYKOVÁ LOGIKA
query_params = st.query_params
jazyk = query_params.get("lang", "SK").upper()

texty = {
    "SK": {"title": "🤖 AI Tutor", "selected": "Vybraný súbor:", "send_file": "Odoslať ⬆️", "input": "Napíš otázku...", "file_msg": "*(Súbor: {name})*", "sys_prompt": "Odpovedaj v jazyku používateľa. Ak píše slovensky, odpovedaj slovensky."},
    "FR": {"title": "🤖 Tuteur IA", "selected": "Fichier sélectionné:", "send_file": "Envoyer ⬆️", "input": "Question...", "file_msg": "*(Fichier: {name})*", "sys_prompt": "Répondez dans la langue de l'utilisateur. S'il écrit en slovaque, répondez en slovaque."},
    "EN": {"title": "🤖 AI Tutor", "selected": "Selected file:", "send_file": "Send ⬆️", "input": "Ask a question...", "file_msg": "*(File: {name})*", "sys_prompt": "Answer in the user's language."},
    "UA": {"title": "🤖 AI Тьютор", "selected": "Вибраний файл:", "send_file": "Надіслати ⬆️", "input": "Запитати...", "file_msg": "*(Файл: {name})*", "sys_prompt": "Відповідайте мовою користувача."},
    "RU": {"title": "🤖 AI Тьютор", "selected": "Выбранный файл:", "send_file": "Отправить ⬆️", "input": "Спросить...", "file_msg": "*(Файл: {name})*", "sys_prompt": "Отвечайте на языке пользователя."}
}
# Ostatné jazyky (DE, IT, ES) si doplň neskôr, keď toto rozbeháme
T = texty.get(jazyk, texty["SK"])

# 3. DIZAJN (Tvoj štýl)
st.set_page_config(page_title=T["title"], layout="wide")
st.markdown("""<style>header, footer {visibility: hidden;} .stAppDeployButton {display:none;}</style>""", unsafe_allow_html=True)

st.title(T["title"])

# 4. CHAT AREA
for m in st.session_state.m:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 5. SPODNÝ PANEL
u = st.file_uploader("uploader", type=['pdf', 'docx', 'jpg', 'jpeg', 'png'], label_visibility="collapsed")
if u: st.info(f"📄 {u.name}")

if p := st.chat_input(T["input"]):
    st.session_state.m.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)

    with st.chat_message("assistant"):
        try:
            # Príprava dát
            content = [f"{T['sys_prompt']}\n\nKontext: {st.session_state.doc_content}\n\nOtázka: {p}"]
            
            if u and u.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                content.append(Image.open(u))

            # Samotné volanie AI
            response = model_ai.generate_content(content)
            st.markdown(response.text)
            st.session_state.m.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"⚠️ CHYBA: {e}")
            # TENTO KÚSOK TI POMÔŽE: Vypíše zoznam modelov, ktoré tvoj kľúč reálne môže použiť
            if "404" in str(e):
                st.warning("Skúšam zistiť, aké modely máš povolené...")
                try:
                    available_models = [m.name for m in genai.list_models()]
                    st.write("Tvoj kľúč vidí tieto modely:", available_models)
                except:
                    st.write("Nepodarilo sa načítať ani zoznam modelov. Skontroluj API kľúč.")
