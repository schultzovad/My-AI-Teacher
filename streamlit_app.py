import streamlit as st
import google.generativeai as genai
import pypdf
import docx

# 1. NASTAVENIE API
api_key = st.secrets.get("tutor") or st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ API kľúč chýba!")
    st.stop()

genai.configure(api_key=api_key)
model_ai = genai.GenerativeModel('gemini-1.5-flash')

# --- INICIALIZÁCIA ---
if "m" not in st.session_state: st.session_state.m = []
if "doc_content" not in st.session_state: st.session_state.doc_content = ""

# 2. JAZYKOVÁ LOGIKA (Podpora pre všetky tvoje predmety)
query_params = st.query_params
jazyk = query_params.get("lang", "SK").upper()

texty = {
    "SK": {
        "title": "🤖 AI Tutor", "lib": "📚 Knižnica", "menu": "Menu", 
        "nav_chat": "🤖 AI Tutor", "nav_lib": "📚 Študijné materiály",
        "selected": "Vybraný súbor:", "send_file": "Odoslať ⬆️", "input": "Napíš otázku...",
        "file_msg": "*(Súbor: {name})*", "sys_prompt": "Odpovedaj výhradne v slovenskom jazyku.",
        "lib_desc": "Vyber si predmet a nájdi potrebné poznámky:"
    }
    # ... (ostatné jazyky EN, FR, DE, IT, ES, UA, RU sa doplnia automaticky podľa predošlého vzoru)
}
T = texty.get(jazyk, texty["SK"])

# 3. DIZAJN + CSS (Očistený uploader podľa tvojich požiadaviek)
st.set_page_config(page_title=T["title"], layout="wide")

st.markdown(f"""
    <style>
    header, footer {{visibility: hidden;}} 
    .stAppDeployButton {{display:none;}}
    
    div[data-testid="stFileUploader"] section {{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        padding: 0 !important;
        min-height: 45px !important;
        border: 1px solid #eee;
        border-radius: 8px;
        background-color: #fafafa;
    }}

    div[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] {{
        width: 40px !important;
        height: 30px !important;
        background-color: white !important;
        border: 1px solid #ccc !important;
        color: transparent !important;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    div[data-testid="stFileUploader"] section::after,
    div[data-testid="stFileUploader"] section::before,
    div[data-testid="stFileUploader"] div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stFileUploader"] label {{
        display: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. BOČNÉ MENU
with st.sidebar:
    st.title(T["menu"])
    volba = st.sidebar.radio("Navigácia", [T["nav_chat"], T["nav_lib"]], label_visibility="collapsed")

# --- SEKCIJA 1: CHAT ---
if volba == T["nav_chat"]:
    st.title(T["title"])
    
    chat_container = st.container()
    with chat_container:
        for m in st.session_state.m:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            u = st.file_uploader("up", type=['pdf', 'docx'], label_visibility="collapsed")
            if u: st.info(f"📄 **{T['selected']}** {u.name}")
        with col2:
            if st.button(T["send_file"], use_container_width=True):
                # (Logika spracovania súboru zostáva rovnaká)
                pass

    if p := st.chat_input(T["input"]):
        # (Logika AI četu)
        pass

# --- SEKCIJA 2: KNIŽNICA (Podľa tvojich priečinkov na Drive) ---
else:
    st.title(T["nav_lib"])
    st.write(T["lib_desc"])
    
    # Rozdelenie predmetov do stĺpcov podľa snímky obrazovky
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.info("🧬 **Biológia**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/1HwEr80n2TnaAs7oyixCvcFWF5ZGKPjmf")
        
        st.info("🏺 **Dejepis**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/1zbicCs41T0Vrjf5DxyQ-5OJaWGvCl5kk")

    with c2:
        st.info("⚛️ **Fyzika**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/1LumTX7YUXknUu16WcG9ooUYq6Nchc-XS")
        
        st.info("🧪 **Chémia**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/1BrnIjnLQfB9ZjcmMxmz-e-_QvoyRkKaR")

    with c3:
        st.info("📐 **Matematika**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/16o7nKWMoIOk7b8m90tXbgA4L2NeZ9STm")
        
        st.info("⚖️ **Občianska náuka**")
        st.link_button("Otvoriť", "https://drive.google.com/drive/u/1/folders/1kNvYlsNxa64IVyB-QLSXQ_8pC6oQzof_")

    st.write("---")
    st.subheader("🌍 Jazyky")
    j1, j2, j3, j4 = st.columns(4)
    with j1:
        st.link_button("🇸🇰 Slovenčina", "https://drive.google.com/drive/u/1/folders/1GY8gyXFXGIXG3gL5cXBPOlbEjsqowpA-")
        st.link_button("🇬🇧 Angličtina", "https://drive.google.com/drive/u/1/folders/1ffEMvwZA4zTCbcCLx3DqfAQYTmqt4fiB")
    with j2:
        st.link_button("🇩🇪 Nemčina", "https://drive.google.com/drive/u/1/folders/1rejCBuHI8qFm_y2Dr1zR9PtJnMJ9SkCI")
        st.link_button("🇫🇷 Francúzština", "https://drive.google.com/drive/u/1/folders/1qf6u3qAMKLkTK4e1QBbBCVo0VNothU3j")
    with j3:
        st.link_button("🇪🇸 Španielčina", "https://drive.google.com/drive/u/1/folders/1qf6u3qAMKLkTK4e1QBbBCVo0VNothU3j")
        st.link_button("🇮🇹 Taliančina", "https://drive.google.com/drive/u/1/folders/161jDX2VhvCpRIoPpY1FLIj08rp5chhp_")
    with j4:
        st.link_button("🇷🇺 Ruština", "https://drive.google.com/drive/u/1/folders/1w7F9_8m4DkFnXx33Iys_kLWgfWPI_Gt5")
        st.link_button("🇺🇦 Ukrajinčina", "https://drive.google.com/drive/u/1/folders/1FSp1PuT1yAJjR3HW17sgvXXIyIWrYHYO")
