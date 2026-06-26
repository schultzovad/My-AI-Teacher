import streamlit as st
import hashlib
import random
import string
from db_utils import supabase

# --- PREKLADY ---
lang_data = {
    "SK": {"title": "🎓 Školský portál", "role": "Zvoľ si rolu:", "login": "Prihlásiť", "reg": "Registrovať"},
    "EN": {"title": "🎓 School Portal", "role": "Choose your role:", "login": "Login", "reg": "Register"},
    "DE": {"title": "🎓 Schulportal", "role": "Wähle deine Rolle:", "login": "Anmelden", "reg": "Registrieren"},
    "ES": {"title": "🎓 Portal Escolar", "role": "Elige tu rol:", "login": "Iniciar sesión", "reg": "Registrarse"},
    "FR": {"title": "🎓 Portail Scolaire", "role": "Choisissez votre rôle:", "login": "Connexion", "reg": "S'inscrire"},
    "IT": {"title": "🎓 Portale Scolastico", "role": "Scegli il tuo ruolo:", "login": "Accedi", "reg": "Registrati"},
    "UA": {"title": "🎓 Шкільний портал", "role": "Виберіть роль:", "login": "Увійти", "reg": "Зареєструватися"},
    "RU": {"title": "🎓 Школьный портал", "role": "Выберите роль:", "login": "Войти", "reg": "Зарегистрироваться"}
}

# Zistenie jazyka z URL (napr. ?lang=EN)
L = st.query_params.get("lang", "SK").upper()
t = lang_data.get(L, lang_data["SK"])

# --- FUNKCIE ---
def hash_pwd(p): return hashlib.sha256(p.encode()).hexdigest()
def gen_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

st.set_page_config(layout="wide", page_title="Školský portál")
st.title(t["title"])
role = st.radio(t["role"], ["Žiak", "Učiteľ"], horizontal=True, key="role_select")

# --- LOGIKA ŽIAK ---
if role == "Žiak":
    if "st_id" not in st.session_state: st.session_state.st_id = None
    if not st.session_state.st_id:
        tab1, tab2 = st.tabs([t["login"], t["reg"]])
        with tab1:
            name = st.text_input("Meno", key="st_login_name")
            pwd = st.text_input("Heslo", type="password", key="st_login_pwd")
            if st.button(t["login"], key="btn_login_st"):
                res = supabase.table("students").select("*").eq("name", name).eq("password", hash_pwd(pwd)).execute()
                if res.data:
                    st.session_state.st_id, st.session_state.st_name = res.data[0]['id'], res.data[0]['name']
                    st.rerun()
        with tab2:
            name = st.text_input("Meno", key="st_reg_name")
            em = st.text_input("Email", key="st_reg_em")
            pw = st.text_input("Heslo", type="password", key="st_reg_pwd")
            if st.button(t["reg"], key="btn_reg_st"):
                supabase.table("students").insert({"name": name, "email": em, "password": hash_pwd(pw)}).execute()
                st.success("Registrácia úspešná!")
    else:
        st.subheader(f"Vitaj, {st.session_state.st_name}")
        if st.button("Odhlásiť", key="logout_st"): st.session_state.st_id = None; st.rerun()

# --- LOGIKA UČITEĽ ---
else: 
    if "tch_id" not in st.session_state: st.session_state.tch_id = None
    if not st.session_state.tch_id:
        tab1, tab2 = st.tabs([t["login"], t["reg"]])
        with tab1:
            name = st.text_input("Meno", key="tch_login_name")
            pwd = st.text_input("Heslo", type="password", key="tch_login_pwd")
            if st.button(t["login"], key="btn_login_tch"):
                res = supabase.table("teachers").select("*").eq("name", name).eq("password", hash_pwd(pwd)).execute()
                if res.data:
                    st.session_state.tch_id, st.session_state.tch_name = res.data[0]['id'], res.data[0]['name']
                    st.rerun()
        with tab2:
            name = st.text_input("Meno", key="tch_reg_name")
            em = st.text_input("Email", key="tch_reg_em")
            pw = st.text_input("Heslo", type="password", key="tch_reg_pwd")
            if st.button(t["reg"], key="btn_reg_tch"):
                supabase.table("teachers").insert({"name": name, "email": em, "password": hash_pwd(pw)}).execute()
                st.success("Registrácia úspešná!")
    else:
        st.subheader(f"Učiteľ: {st.session_state.tch_name}")
        n = st.text_input("Názov novej skupiny", key="new_group_name")
        if st.button("Vytvoriť skupinu", key="create_group_btn"):
            supabase.table("groups").insert({"group_name": n, "group_code": gen_code(), "teacher_id": st.session_state.tch_id}).execute()
            st.rerun()
