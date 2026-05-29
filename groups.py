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

# ... (init_db, hash_pwd, gen_code, upload/delete functions ostávajú rovnaké ako doteraz) ...
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

st.title("🎓 Školský portál")
role = st.radio("Rola:", ["Žiak", "Učiteľ"], horizontal=True)

if role == "Žiak":
    if "st_id" not in st.session_state: st.session_state.st_id = None
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
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", (name, em, hash_pwd(pw)))
                    new_id = cursor.lastrowid
                    conn.commit(); conn.close()
                    # AUTOMATICKÉ PRIHLÁSENIE:
                    st.session_state.st_id = new_id
                    st.session_state.st_name = name
                    st.rerun() # Toto vymaže všetky hlášky a hodí ho do účtu
                except: st.error("Meno alebo email už existuje.")
    else:
        st.write(f"### {st.session_state.st_name}")
        c1, c2 = st.columns([1, 1])
        if c1.button("Odhlásiť"): st.session_state.st_id = None; st.rerun()
        if c2.button("❌ Zmazať môj účet", type="primary"):
            conn = sqlite3.connect(DB_NAME)
            conn.execute("DELETE FROM group_members WHERE student_id=?", (st.session_state.st_id,))
            conn.execute("DELETE FROM students WHERE id=?", (st.session_state.st_id,))
            conn.commit(); conn.close(); st.session_state.st_id = None; st.rerun()
        # ... zvyšok kódu pre žiaka ...
        kod = st.text_input("Zadaj kód skupiny:")
        if st.button("Vstúpiť do skupiny"):
            conn = sqlite3.connect(DB_NAME)
            g = conn.execute("SELECT id FROM groups WHERE group_code=?", (kod.upper(),)).fetchone()
            if g:
                try: conn.execute("INSERT INTO group_members (group_id, student_id) VALUES (?, ?)", (g[0], st.session_state.st_id)); conn.commit()
                except: pass
                st.session_state.open_group = g[0]; conn.close(); st.rerun()
            else: st.error("Kód neexistuje."); conn.close()
        
        conn = sqlite3.connect(DB_NAME)
        skupiny = conn.execute("SELECT g.id, g.group_name FROM groups g JOIN group_members gm ON g.id=gm.group_id WHERE gm.student_id=?", (st.session_state.st_id,)).fetchall()
        for s in skupiny:
            with st.expander(f"📁 {s[1]}"):
                mats = conn.execute("SELECT id, title, link, file_path_on_cloud, uploaded_by FROM materials WHERE group_id=?", (s[0],)).fetchall()
                for m in mats:
                    c1, c2 = st.columns([8, 2])
                    c1.markdown(f"• [{m[1]}]({m[2]})")
                    if m[4] == st.session_state.st_name:
                        if c2.button("❌ Zmazať", key=f"del_{m[0]}"): delete_from_supabase(m[3]); conn.execute("DELETE FROM materials WHERE id=?", (m[0],)); conn.commit(); st.rerun()
                up = st.file_uploader(f"Nahrať do {s[1]}", key=f"up_{s[0]}")
                if up and st.button(f"Nahrať", key=f"b_{s[0]}"):
                    url, path = upload_to_supabase(up.getvalue(), up.name, up.type)
                    conn.execute("INSERT INTO materials (title, link, group_id, file_path_on_cloud, uploaded_by) VALUES (?, ?, ?, ?, ?)", (up.name, url, s[0], path, st.session_state.st_name))
                    conn.commit(); st.rerun()
        conn.close()

else: # Učiteľ (tu sprav to isté - pridaj session nastavenie po registrácii)
    if "tch_id" not in st.session_state: st.session_state.tch_id = None
    if not st.session_state.tch_id:
        tab1, tab2 = st.tabs(["Prihlásiť", "Registrovať"])
        with tab1:
            name = st.text_input("Meno", key="tch_login_name")
            pw = st.text_input("Heslo", type="password", key="tch_login_pwd")
            if st.button("Prihlásiť"):
                conn = sqlite3.connect(DB_NAME)
                user = conn.execute("SELECT id, name FROM teachers WHERE name=? AND password=?", (name, hash_pwd(pw))).fetchone()
                if user: st.session_state.tch_id, st.session_state.tch_name = user; st.rerun()
                conn.close()
        with tab2:
            name = st.text_input("Meno", key="tch_reg_name")
            em = st.text_input("Email", key="tch_reg_em")
            pw = st.text_input("Heslo", type="password", key="tch_reg_pw")
            if st.button("Registrovať"):
                try:
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO teachers (name, email, password) VALUES (?, ?, ?)", (name, em, hash_pwd(pw)))
                    new_id = cursor.lastrowid
                    conn.commit(); conn.close()
                    st.session_state.tch_id = new_id
                    st.session_state.tch_name = name
                    st.rerun()
                except: st.error("Meno alebo email už existuje.")
    else:
        st.write(f"### {st.session_state.tch_name}")
        if st.button("Odhlásiť"): st.session_state.tch_id = None; st.rerun()
        # ... zvyšok učiteľa ...
        n = st.text_input("Názov novej skupiny")
        if st.button("Vytvoriť skupinu"):
            conn = sqlite3.connect(DB_NAME)
            conn.execute("INSERT INTO groups (group_name, group_code, teacher_id) VALUES (?, ?, ?)", (n, gen_code(), st.session_state.tch_id))
            conn.commit(); conn.close(); st.rerun()
        # ... (zoznam skupín)
        conn = sqlite3.connect(DB_NAME)
        skupiny = conn.execute("SELECT id, group_name, group_code FROM groups WHERE teacher_id=?", (st.session_state.tch_id,)).fetchall()
        for s in skupiny:
            with st.expander(f"📁 {s[1]} (Kód: {s[2]})"):
                if st.button("Zmazať skupinu", key=f"del_{s[0]}"): conn.execute("DELETE FROM groups WHERE id=?", (s[0],)); conn.commit(); st.rerun()
        conn.close()
