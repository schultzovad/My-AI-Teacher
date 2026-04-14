import streamlit as st
from streamlit_option_menu 
import option_menu # Ak toto nemáš, napíšem ti nižšie ako to spraviť cez HTML

# --- KONFIGURÁCIA STRÁNKY ---
st.set_page_config(page_title="EduHub", layout="wide", page_icon="🎓", initial_sidebar_state="expanded")

# --- CSS PRE MODERNEJŠÍ VZHĽAD A SKRYTIE LIŠIEX ---
st.markdown("""
    <style>
    /* Skrytie default líšt */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Sivé pozadie pre bočnú lištu */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #dee2e6;
    }
    
    /* Vlastný štýl pre prepínač jazyka */
    .stSelectbox label {
        color: #6c757d;
        font-weight: normal;
        margin-bottom: 5px;
    }
    
    /* Vlastný štýl pre nadpis AI Tutor a ikonky */
    .sidebar-header {
        display: flex;
        align-items: center;
        font-size: 20px;
        font-weight: bold;
        color: #31333F;
        margin-bottom: 15px;
    }
    
    /* Vlastný štýl pre ČERVENÉ TLAČIDLO "Nový čet" */
    div.stButton > button:first-child {
        background-color: #ff4d4d;
        color: white;
        border: none;
        font-weight: bold;
        width: 100%;
        border-radius: 8px;
        padding: 10px 0;
    }
    
    /* Vlastný štýl pre VYHĽADÁVACIE POLE */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #dee2e6;
        background-color: white;
    }
    
    /* Prázdny priestor pre hlavný obsah */
    .block-container {
        padding-top: 5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BOČNÁ LIŠTA (SIDEBAR) - TVOJ MODERNY VZHĽAD ---
with st.sidebar:
    # 1. Jazyk
    st.markdown('<p style="color: #6c757d; margin-bottom: 2px; font-size: 14px;">🌐 Jazyk</p>', unsafe_allow_html=True)
    lang = st.selectbox("", ["SK", "EN"], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Nadpis a ikonky (Súbor, Bublina)
    st.markdown("""
        <div class="sidebar-header">
            📁 &nbsp; 💬 &nbsp; AI Tutor
        </div>
        """, unsafe_allow_html=True)
        
    # 3. Červené tlačidlo "Nový čet"
    if st.button("＋ Nový čet"):
        st.success("Nový čet bol vytvorený!") # Zatiaľ len simulácia
        
    # 4. Vyhľadávacie pole "Hľadaj..."
    search = st.text_input("", placeholder="Hľadaj...", label_visibility="collapsed")

# --- HLAVNÝ OBSAH (Prázdny podla tvojich fotiek) ---
# Tuto zatiaľ nie je nič, len prázdna biela plocha s deliacou čiarou
st.divider()
