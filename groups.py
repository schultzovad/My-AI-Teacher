import streamlit as st
import hashlib
import random
import string
import unicodedata
from db_utils import supabase

# --- POMOCNÉ FUNKCIE ---
def hash_pwd(p): return hashlib.sha256(p.encode()).hexdigest()
def gen_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# --- CSS DIZAJN ---
st.set_page_config(layout="wide", page_title="Školský portál")
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    div.stButton > button { border-radius: 12px; border: 2px solid #4a90e2; background-color: #ffffff; color: #4a90e2; font-weight: bold; }
    div.stButton > button:hover { background-color: #4a90e2; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Školský portál")
role = st.radio("Zvoľ si rolu:", ["Žiak", "Učiteľ"], horizontal=True)

# --- LOGIKA ŽIAK ---
if role == "Žiak":
    if "st_id" not in st.session_state: st.session_state.st_id = None
    if not st.session_state.st_id:
        tab1, tab2 = st.tabs(["Prihlásiť", "Registrovať"])
        with tab1:
            name = st.text_input("Meno", key="st_login")
            pwd = st.text_input("Heslo", type="password", key="st_pwd")
            if st.button("Prihlásiť"):
                res = supabase.table("students").select("*").eq("name", name).eq("password", hash_pwd(pwd)).execute()
                if res.data:
                    st.session_state.st_id, st.session_state.st_name = res.data[0]['id'], res.data[0]['name']
                    st.rerun()
        with tab2:
            name = st.text_input("Meno", key="reg_n")
            em = st.text_input("Email", key="reg_e")
            pw = st.text_input("Heslo", type="password", key="reg_p")
            if st.button("Registrovať"):
                supabase.table("students").insert({"name": name, "email": em, "password": hash_pwd(pw)}).execute()
                st.success("Registrované!")
    else:
        st.subheader(f"Vitaj, {st.session_state.st_name}")
        if st.button("Odhlásiť"): st.session_state.st_id = None; st.rerun()
        
        # Zobrazenie skupín
        skupiny = supabase.table("groups").select("*").execute().data
        for s in skupiny:
            with st.expander(f"📁 {s['group_name']}"):
                mats = supabase.table("materials").select("*").eq("group_id", s['id']).execute().data
                for m in mats:
                    st.markdown(f"• [{m['title']}]({m['link']})")
                
                up_file = st.file_uploader(f"Nahrať do {s['group_name']}", key=f"f_{s['id']}")
                if up_file and st.button("Nahrať", key=f"up_{s['id']}"):
                    # Sem by išla funkcia na upload do Supabase Storage
                    st.info("Súbor bol nahraný (nutné doplniť storage logiku)")

# --- LOGIKA UČITEĽ ---
else:
    if "tch_id" not in st.session_state: st.session_state.tch_id = None
    if not st.session_state.tch_id:
        name = st.text_input("Meno učiteľa")
        pwd = st.text_input("Heslo", type="password")
        if st.button("Prihlásiť"):
            res = supabase.table("teachers").select("*").eq("name", name).eq("password", hash_pwd(pwd)).execute()
            if res.data:
                st.session_state.tch_id, st.session_state.tch_name = res.data[0]['id'], res.data[0]['name']
                st.rerun()
    else:
        st.subheader(f"Učiteľ: {st.session_state.tch_name}")
        n = st.text_input("Názov novej skupiny")
        if st.button("Vytvoriť skupinu"):
            supabase.table("groups").insert({"group_name": n, "group_code": gen_code(), "teacher_id": st.session_state.tch_id}).execute()
            st.rerun()
