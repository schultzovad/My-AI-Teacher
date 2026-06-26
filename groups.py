import streamlit as st
import hashlib
import random
import string
from db_utils import supabase

# --- PREKLADY ---
lang_data = {
    "SK": {"title": "🎓 Školský portál", "role": "Zvoľ si rolu:", "login": "Prihlásiť", "reg": "Registrovať", "kick": "Odobrať"},
    "EN": {"title": "🎓 School Portal", "role": "Choose your role:", "login": "Login", "reg": "Register", "kick": "Remove"},
    "DE": {"title": "🎓 Schulportal", "role": "Wähle deine Rolle:", "login": "Anmelden", "reg": "Registrieren", "kick": "Entfernen"},
    "ES": {"title": "🎓 Portal Escolar", "role": "Elige tu rol:", "login": "Iniciar sesión", "reg": "Registrarse", "kick": "Eliminar"},
    "FR": {"title": "🎓 Portail Scolaire", "role": "Choisissez votre rôle:", "login": "Connexion", "reg": "S'inscrire", "kick": "Supprimer"},
    "IT": {"title": "🎓 Portale Scolastico", "role": "Scegli il tuo ruolo:", "login": "Accedi", "reg": "Registrati", "kick": "Rimuovi"},
    "UA": {"title": "🎓 Шкільний портал", "role": "Виберіть роль:", "login": "Увійти", "reg": "Зареєструватися", "kick": "Видалити"},
    "RU": {"title": "🎓 Школьный портал", "role": "Выберите роль:", "login": "Войти", "reg": "Зарегистрироваться", "kick": "Удалить"}
}

# Zistenie jazyka
L = st.query_params.get("lang", "SK").upper()
t = lang_data.get(L, lang_data["SK"])

# --- FUNKCIE ---
def hash_pwd(p): return hashlib.sha256(p.encode()).hexdigest()
def gen_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

st.set_page_config(layout="wide", page_title="Školský portál")
st.title(t["title"])
role = st.radio(t["role"], ["Žiak", "Učiteľ"], horizontal=True)

# --- LOGIKA ---
if role == "Žiak":
    if "st_id" not in st.session_state: st.session_state.st_id = None
    if not st.session_state.st_id:
        tab1, tab2 = st.tabs([t["login"], t["reg"]])
        with tab1:
            name = st.text_input("Meno")
            pwd = st.text_input("Heslo", type="password")
            if st.button(t["login"]):
                res = supabase.table("students").select("*").eq("name", name).eq("password", hash_pwd(pwd)).execute()
                if res.data:
                    st.session_state.st_id, st.session_state.st_name = res.data[0]['id'], res.data[0]['name']
                    st.rerun()
        with tab2:
            name = st.text_input("Nové meno")
            em = st.text_input("Email")
            pw = st.text_input("Heslo", type="password")
            if st.button(t["reg"]):
                supabase.table("students").insert({"name": name, "email": em, "password": hash_pwd(pw)}).execute()
                st.success("Registrácia úspešná!")
    else:
        st.subheader(f"Vitaj, {st.session_state.st_name}")
        if st.button("Odhlásiť"): st.session_state.st_id = None; st.rerun()
        
        # Zobrazenie skupín
        skupiny = supabase.table("groups").select("id, group_name").execute().data
        for s in skupiny:
            with st.expander(f"📁 {s['group_name']}"):
                mats = supabase.table("materials").select("*").eq("group_id", s['id']).execute().data
                for m in mats:
                    st.markdown(f"• [{m['title']}]({m['link']})")

else: # Učiteľ
    if "tch_id" not in st.session_state: st.session_state.tch_id = None
    if not st.session_state.tch_id:
        name = st.text_input("Meno učiteľa")
        pwd = st.text_input("Heslo", type="password")
        if st.button(t["login"]):
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
