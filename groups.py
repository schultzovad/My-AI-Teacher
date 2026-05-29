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
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS teachers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, password TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, password TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT, group_code TEXT UNIQUE, teacher_id INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS group_members (group_id INTEGER, student_id INTEGER, UNIQUE(group_id, student_id))')
    cursor.execute('CREATE TABLE IF NOT EXISTS materials (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, link TEXT, group_id INTEGER, file_path_on_cloud TEXT, uploaded_by TEXT)')
    conn.commit()
    conn.close()

init_db()

def hash_pwd(p): return hashlib.sha256(p.encode()).hexdigest()
def gen_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def upload_to_supabase(file_bytes, file_name, mime_type):
    base_name = "".join([c for c in unicodedata.normalize('NFKD', file_name) if not unicodedata.combining(c)])
    clean_name = "".join(c for c in base_name if c.isalnum() or c in "._-").strip()
    unique_name = f"{gen_code()}_{clean_name}"
    try:
        supabase_client.storage.from_(BUCKET_NAME).upload(unique_name, file_bytes, {"content-type": mime_type})
        return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{unique_name}", unique_name
    except: return None, None

def delete_from_supabase(path):
    try: supabase_client.storage.from_(BUCKET_NAME).remove([path])
    except: pass

# --- UI LOGIKA ---
st.title("🎓 Školský portál")
role = st.radio("Prihlásenie:", ["Žiak", "Učiteľ"], horizontal=True)

if role == "Žiak":
    if "st_id" not in st.session_state: st.session_state.st_id = None
    
    if not st.session_state.st_id:
        tab1, tab2 = st.tabs(["Prihlásiť", "Registrovať"])
        with tab1:
            email = st.text_input("Email", key="st_em")
            pwd = st.text_input("Heslo", type="password", key="st_pwd")
            if st.button("Prihlásiť"):
                conn = sqlite3.connect(DB_NAME)
                user = conn.execute("SELECT id, name FROM students WHERE email=? AND password=?", (email, hash_pwd(pwd))).fetchone()
                if user: st.session_state.st_id, st.session_state.st_name = user; st.rerun()
                conn.close()
        with tab2:
            name = st.text_input("Meno")
            em = st.text_input("Email", key="st_reg_em")
            pw = st.text_input("Heslo", type="password", key="st_reg_pw")
            if st.button("Registrovať"):
                try:
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", (name, em, hash_pwd(pw)))
                    conn.commit(); st.success("Hotovo!")
                except: st.error("Email už existuje.")
    else:
        st.write(f"Ahoj {st.session_state.st_name}!")
        if st.button("Odhlásiť"): st.session_state.st_id = None; st.rerun()
        
        # Pridanie do skupiny
        kod = st.text_input("Zadaj kód skupiny:")
        if st.button("Vstúpiť do skupiny"):
            conn = sqlite3.connect(DB_NAME)
            g = conn.execute("SELECT id FROM groups WHERE group_code=?", (kod.upper(),)).fetchone()
            if g:
                try: conn.execute("INSERT INTO group_members VALUES (?, ?)", (g[0], st.session_state.st_id)); conn.commit()
                except: pass
            conn.close()
            
        # Zoznam skupín
        conn = sqlite3.connect(DB_NAME)
        skupiny = conn.execute("SELECT g.id, g.group_name FROM groups g JOIN group_members gm ON g.id=gm.group_id WHERE gm.student_id=?", (st.session_state.st_id,)).fetchall()
        for s in skupiny:
            with st.expander(f"📁 {s[1]}"):
                mats = conn.execute("SELECT title, link FROM materials WHERE group_id=?", (s[0],)).fetchall()
                for m in mats: st.markdown(f"• [{m[0]}]({m[1]})")
        conn.close()

else: # Učiteľ
    if "tch_id" not in st.session_state: st.session_state.tch_id = None
    if not st.session_state.tch_id:
        em = st.text_input("Email učiteľa")
        pw = st.text_input("Heslo", type="password")
        if st.button("Prihlásiť"):
            conn = sqlite3.connect(DB_NAME)
            user = conn.execute("SELECT id, name FROM teachers WHERE email=? AND password=?", (em, hash_pwd(pw))).fetchone()
            if user: st.session_state.tch_id, st.session_state.tch_name = user; st.rerun()
    else:
        st.write(f"Profesor {st.session_state.tch_name}")
        if st.button("Odhlásiť"): st.session_state.tch_id = None; st.rerun()
        
        n = st.text_input("Názov novej skupiny")
        if st.button("Vytvoriť skupinu"):
            conn = sqlite3.connect(DB_NAME)
            conn.execute("INSERT INTO groups (group_name, group_code, teacher_id) VALUES (?, ?, ?)", (n, gen_code(), st.session_state.tch_id))
            conn.commit(); conn.close(); st.rerun()
            
        conn = sqlite3.connect(DB_NAME)
        skupiny = conn.execute("SELECT id, group_name, group_code FROM groups WHERE teacher_id=?", (st.session_state.tch_id,)).fetchall()
        for s in skupiny:
            st.write(f"**{s[1]}** (Kód: {s[2]})")
            if st.button("Zmazať", key=f"del_{s[0]}"):
                conn.execute("DELETE FROM groups WHERE id=?", (s[0],)); conn.commit(); st.rerun()
        conn.close()
