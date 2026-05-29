import streamlit as st
import sqlite3
import hashlib
import random
import string
import unicodedata
from supabase import create_client

st.set_page_config(layout="wide")

# Konfigurácia Supabase
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = str(st.secrets.get("SUPABASE_KEY", "")).strip()
BUCKET_NAME = "materials"
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

DB_NAME = "tutor_platform.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    # Meníme tabuľky tak, aby meno bolo INDEXOVANÉ pre rýchle hľadanie
    conn.execute('CREATE TABLE IF NOT EXISTS teachers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, email TEXT UNIQUE, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, email TEXT UNIQUE, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT, group_code TEXT UNIQUE, teacher_id INTEGER)')
    conn.execute('CREATE TABLE IF NOT EXISTS group_members (group_id INTEGER, student_id INTEGER, UNIQUE(group_id, student_id))')
    conn.execute('CREATE TABLE IF NOT EXISTS materials (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, link TEXT, group_id INTEGER, file_path_on_cloud TEXT, uploaded_by TEXT)')
    conn.commit(); conn.close()

init_db()

def hash_pwd(p): return hashlib.sha256(p.encode()).hexdigest()
def gen_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# --- UI LOGIKA ---
st.title("🎓 Školský portál")
role = st.radio("Prihlásenie:", ["Žiak", "Učiteľ"], horizontal=True)

# Pomocná funkcia na prihlásenie podľa mena
def login_user(table, name, pwd):
    conn = sqlite3.connect(DB_NAME)
    user = conn.execute(f"SELECT id, name FROM {table} WHERE name=? AND password=?", (name, hash_pwd(pwd))).fetchone()
    conn.close()
    return user

if role == "Žiak":
    if "st_id" not in st.session_state: st.session_state.st_id = None
    if not st.session_state.st_id:
        tab1, tab2 = st.tabs(["Prihlásiť", "Registrovať"])
        with tab1:
            name = st.text_input("Meno", key="st_login_name")
            pwd = st.text_input("Heslo", type="password", key="st_login_pwd")
            if st.button("Prihlásiť"):
                user = login_user("students", name, pwd)
                if user: st.session_state.st_id, st.session_state.st_name = user; st.rerun()
        with tab2:
            name = st.text_input("Meno", key="st_reg_name")
            em = st.text_input("Email", key="st_reg_em")
            pw = st.text_input("Heslo", type="password", key="st_reg_pw")
            if st.button("Registrovať"):
                try:
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", (name, em, hash_pwd(pw)))
                    conn.commit(); conn.close(); st.success("Registrácia úspešná!")
                except: st.error("Meno alebo email už existuje.")
    else:
        st.write(f"Ahoj {st.session_state.st_name}!")
        if st.button("Odhlásiť"): st.session_state.st_id = None; st.rerun()
        # ... (zvyšok logiky pre žiaka zostáva nezmenený) ...

else: # Učiteľ
    if "tch_id" not in st.session_state: st.session_state.tch_id = None
    if not st.session_state.tch_id:
        tab1, tab2 = st.tabs(["Prihlásiť", "Registrovať"])
        with tab1:
            name = st.text_input("Meno učiteľa", key="tch_login_name")
            pw = st.text_input("Heslo", type="password", key="tch_login_pwd")
            if st.button("Prihlásiť"):
                user = login_user("teachers", name, pw)
                if user: st.session_state.tch_id, st.session_state.tch_name = user; st.rerun()
        with tab2:
            name = st.text_input("Meno učiteľa", key="tch_reg_name")
            em = st.text_input("Email", key="tch_reg_em")
            pw = st.text_input("Heslo", type="password", key="tch_reg_pw")
            if st.button("Registrovať"):
                try:
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("INSERT INTO teachers (name, email, password) VALUES (?, ?, ?)", (name, em, hash_pwd(pw)))
                    conn.commit(); conn.close(); st.success("Registrácia úspešná!")
                except: st.error("Meno alebo email už existuje.")
    else:
        st.write(f"Profesor {st.session_state.tch_name}")
        # ... (zvyšok logiky pre učiteľa zostáva nezmenený) ...
