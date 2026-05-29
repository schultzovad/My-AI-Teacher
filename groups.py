import streamlit as st
import sqlite3
import hashlib
import random
import string
import unicodedata
from supabase import create_client

st.set_page_config(layout="wide")
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = str(st.secrets.get("SUPABASE_KEY", "")).strip()
BUCKET_NAME = "materials"
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
DB_NAME = "tutor_platform.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS teachers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, email TEXT UNIQUE, password TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, email TEXT UNIQUE, password TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT, group_code TEXT UNIQUE, teacher_id INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS group_members (group_id INTEGER, student_id INTEGER, UNIQUE(group_id, student_id))')
    cursor.execute('CREATE TABLE IF NOT EXISTS materials (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, link TEXT, group_id INTEGER, file_path_on_cloud TEXT, uploaded_by TEXT)')
    conn.commit(); conn.close()

init_db()

def hash_pwd(p): return hashlib.sha256(p.encode()).hexdigest()
def gen_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# --- UI LOGIKA ---
st.title("🎓 Školský portál")
role = st.radio("Rola:", ["Žiak", "Učiteľ"], horizontal=True)

if role == "Žiak":
    if "st_id" not in st.session_state: st.session_state.st_id = None
    if "st_name" not in st.session_state: st.session_state.st_name = ""
    
    if not st.session_state.st_id:
        tab1, tab2 = st.tabs(["Prihlásiť", "Registrovať"])
        with tab1:
            name = st.text_input("Meno", key="st_login_name")
            pwd = st.text_input("Heslo", type="password", key="st_login_pwd")
            if st.button("Prihlásiť"):
                conn = sqlite3.connect(DB_NAME)
                user = conn.execute("SELECT id, name FROM students WHERE name=? AND password=?", (name, hash_pwd(pwd))).fetchone()
                if user: st.session_state.st_id, st.session_state.st_name = user; st.rerun()
                conn.close()
        with tab2:
            name = st.text_input("Meno", key="st_reg_name")
            em = st.text_input("Email", key="st_reg_em")
            pw = st.text_input("Heslo", type="password", key="st_reg_pw")
            if st.button("Registrovať"):
                try:
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", (name, em, hash_pwd(pw)))
                    conn.commit(); conn.close(); st.success("Registrácia OK!")
                except: st.error("Meno alebo email už existuje.")
    else:
        st.write(f"### Ahoj, {st.session_state.st_name}!")
        if st.button("Odhlásiť"): st.session_state.st_id = None; st.session_state.st_name = ""; st.rerun()
        
        kod = st.text_input("Zadaj kód skupiny:")
        if st.button("Vstúpiť do skupiny"):
            conn = sqlite3.connect(DB_NAME)
            g = conn.execute("SELECT id FROM groups WHERE group_code=?", (kod.upper(),)).fetchone()
            if g:
                try: conn.execute("INSERT INTO group_members VALUES (?, ?)", (g[0], st.session_state.st_id)); conn.commit(); st.rerun()
                except: st.info("Už v nej si.")
            else: st.error("Kód neexistuje.")
            conn.close()
        
        conn = sqlite3.connect(DB_NAME)
        skupiny = conn.execute("SELECT g.id, g.group_name FROM groups g JOIN group_members gm ON g.id=gm.group_id WHERE gm.student_id=?", (st.session_state.st_id,)).fetchall()
        for s in skupiny:
            with st.expander(f"📁 {s[1]}"):
                mats = conn.execute("SELECT title, link FROM materials WHERE group_id=?", (s[0],)).fetchall()
                for m in mats: st.markdown(f"• [{m[0]}]({m[1]})")
        conn.close()

else: # Učiteľ
    if "tch_id" not in st.session_state: st.session_state.tch_id = None
    if "tch_name" not in st.session_state: st.session_state.tch_name = ""
    if not st.session_state.tch_id:
        tab1, tab2 = st.tabs(["Prihlásiť", "Registrovať"])
        with tab1:
            name = st.text_input("Meno učiteľa", key="tch_login_name")
            pw = st.text_input("Heslo", type="password", key="tch_login_pwd")
            if st.button("Prihlásiť"):
                conn = sqlite3.connect(DB_NAME)
                user = conn.execute("SELECT id, name FROM teachers WHERE name=? AND password=?", (name, hash_pwd(pw))).fetchone()
                if user: st.session_state.tch_id, st.session_state.tch_name = user; st.rerun()
                conn.close()
        with tab2:
            name = st.text_input("Meno učiteľa", key="tch_reg_name")
            em = st.text_input("Email", key="tch_reg_em")
            pw = st.text_input("Heslo", type="password", key="tch_reg_pw")
            if st.button("Registrovať"):
                try:
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("INSERT INTO teachers (name, email, password) VALUES (?, ?, ?)", (name, em, hash_pwd(pw)))
                    conn.commit(); conn.close(); st.success("Registrácia OK!")
                except: st.error("Meno alebo email už existuje.")
    else:
        st.write(f"### Profesor {st.session_state.tch_name}")
        if st.button("Odhlásiť"): st.session_state.tch_id = None; st.session_state.tch_name = ""; st.rerun()
        # ... zvyšok kódu pre učiteľa (skupiny atď.) ...
