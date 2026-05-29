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
    cursor.execute('CREATE TABLE IF NOT EXISTS teachers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, email TEXT, password TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, email TEXT, password TEXT)')
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

if 'input_group_name' not in st.session_state: st.session_state.input_group_name = ""
if 'input_join_code' not in st.session_state: st.session_state.input_join_code = ""

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
                else: st.error("Zlé meno alebo heslo.")
                conn.close()
        with tab2:
            name = st.text_input("Meno", key="st_reg_name")
            em = st.text_input("Email", key="st_reg_em")
            pw = st.text_input("Heslo", type="password", key="st_reg_pw")
            if st.button("Registrovať"):
                conn = sqlite3.connect(DB_NAME)
                try:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", (name, em, hash_pwd(pw)))
                    st.session_state.st_id = cursor.lastrowid
                    st.session_state.st_name = name
                    conn.commit(); conn.close(); st.rerun()
                except sqlite3.IntegrityError: 
                    conn.close(); st.error("Meno už existuje. Vyber si iné.")
    else:
        st.write(f"### {st.session_state.st_name}")
        c1, c2 = st.columns([1, 1])
        if c1.button("Odhlásiť"): st.session_state.st_id = None; st.rerun()
        
        # Zmazanie účtu s potvrdením
        if st.button("❌ Zmazať môj účet", type="primary"): st.session_state.confirm_del_acc = True
        if st.session_state.get("confirm_del_acc", False):
            st.error("Naozaj chceš ZMAZAŤ CELÝ ÚČET?")
            c_y, c_n = st.columns(2)
            if c_y.button("ÁNO, ZMAZAŤ"):
                conn = sqlite3.connect(DB_NAME)
                conn.execute("DELETE FROM group_members WHERE student_id=?", (st.session_state.st_id,))
                conn.execute("DELETE FROM students WHERE id=?", (st.session_state.st_id,))
                conn.commit(); conn.close(); st.session_state.st_id = None; st.session_state.confirm_del_acc = False; st.rerun()
            if c_n.button("Nie"): st.session_state.confirm_del_acc = False; st.rerun()
        
        kod = st.text_input("Zadaj kód skupiny:", value=st.session_state.input_join_code)
        if st.button("Vstúpiť do skupiny"):
            conn = sqlite3.connect(DB_NAME)
            g = conn.execute("SELECT id FROM groups WHERE group_code=?", (kod.upper(),)).fetchone()
            if g:
                try: conn.execute("INSERT INTO group_members (group_id, student_id) VALUES (?, ?)", (g[0], st.session_state.st_id)); conn.commit()
                except: pass
                st.session_state.open_group = g[0]; st.session_state.input_join_code = ""; conn.close(); st.rerun()
            else: st.error("Kód neexistuje."); conn.close()
        
        conn = sqlite3.connect(DB_NAME)
        skupiny = conn.execute("SELECT g.id, g.group_name FROM groups g JOIN group_members gm ON g.id=gm.group_id WHERE gm.student_id=?", (st.session_state.st_id,)).fetchall()
        for s in skupiny:
            is_expanded = st.session_state.get("open_group", None) == s[0]
            with st.expander(f"📁 {s[1]}", expanded=is_expanded):
                mats = conn.execute("SELECT id, title, link, file_path_on_cloud, uploaded_by FROM materials WHERE group_id=?", (s[0],)).fetchall()
                for m in mats:
                    c1, c2 = st.columns([8, 2])
                    c1.markdown(f"• [{m[1]}]({m[2]}) (nahral: {m[4]})")
                    if m[4] == st.session_state.st_name:
                        if c2.button("❌ Zmazať", key=f"del_st_{m[0]}"):
                            delete_from_supabase(m[3]); conn.execute("DELETE FROM materials WHERE id=?", (m[0],)); conn.commit(); st.rerun()
                up_file = st.file_uploader(f"Nahrať do {s[1]}", key=f"file_{s[0]}")
                if up_file and st.button(f"Nahrať", key=f"btn_{s[0]}"):
                    url, path = upload_to_supabase(up_file.getvalue(), up_file.name, up_file.type)
                    conn.execute("INSERT INTO materials (title, link, group_id, file_path_on_cloud, uploaded_by) VALUES (?, ?, ?, ?, ?)", (up_file.name, url, s[0], path, st.session_state.st_name))
                    conn.commit(); st.rerun()
        st.session_state.open_group = None; conn.close()

else: # Učiteľ
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
                else: st.error("Zlé meno alebo heslo.")
                conn.close()
        with tab2:
            name = st.text_input("Meno", key="tch_reg_name")
            em = st.text_input("Email", key="tch_reg_em")
            pw = st.text_input("Heslo", type="password", key="tch_reg_pw")
            if st.button("Registrovať"):
                conn = sqlite3.connect(DB_NAME)
                try:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO teachers (name, email, password) VALUES (?, ?, ?)", (name, em, hash_pwd(pw)))
                    st.session_state.tch_id = cursor.lastrowid
                    st.session_state.tch_name = name
                    conn.commit(); conn.close(); st.rerun()
                except sqlite3.IntegrityError: 
                    conn.close(); st.error("Meno už existuje. Vyber si iné.")
    else:
        st.write(f"### {st.session_state.tch_name}")
        c1, c2 = st.columns([1, 1])
        if c1.button("Odhlásiť"): st.session_state.tch_id = None; st.rerun()
        
        # Zmazanie účtu s potvrdením
        if st.button("❌ Zmazať môj účet", type="primary"): st.session_state.confirm_del_tch = True
        if st.session_state.get("confirm_del_tch", False):
            st.error("Naozaj chceš ZMAZAŤ CELÝ ÚČET A VŠETKY SKUPINY?")
            c_y, c_n = st.columns(2)
            if c_y.button("ÁNO, ZMAZAŤ"):
                conn = sqlite3.connect(DB_NAME)
                groups = conn.execute("SELECT id FROM groups WHERE teacher_id=?", (st.session_state.tch_id,)).fetchall()
                for g in groups: conn.execute("DELETE FROM groups WHERE id=?", (g[0],))
                conn.execute("DELETE FROM teachers WHERE id=?", (st.session_state.tch_id,))
                conn.commit(); conn.close(); st.session_state.tch_id = None; st.session_state.confirm_del_tch = False; st.rerun()
            if c_n.button("Nie"): st.session_state.confirm_del_tch = False; st.rerun()

        n = st.text_input("Názov novej skupiny", value=st.session_state.input_group_name)
        if st.button("Vytvoriť skupinu"):
            conn = sqlite3.connect(DB_NAME)
            conn.execute("INSERT INTO groups (group_name, group_code, teacher_id) VALUES (?, ?, ?)", (n, gen_code(), st.session_state.tch_id))
            conn.commit(); conn.close(); st.session_state.input_group_name = ""; st.rerun()
            
        conn = sqlite3.connect(DB_NAME)
        skupiny = conn.execute("SELECT id, group_name, group_code FROM groups WHERE teacher_id=?", (st.session_state.tch_id,)).fetchall()
        for s in skupiny:
            with st.expander(f"📁 {s[1]} (Kód: {s[2]})"):
                # Zmazanie skupiny s potvrdením
                if st.button("Zmazať celú skupinu", key=f"del_{s[0]}"): st.session_state[f"confirm_del_g_{s[0]}"] = True
                if st.session_state.get(f"confirm_del_g_{s[0]}", False):
                    st.warning("Naozaj zmazať túto skupinu?")
                    c_y, c_n = st.columns(2)
                    if c_y.button("Áno", key=f"yes_{s[0]}"): conn.execute("DELETE FROM groups WHERE id=?", (s[0],)); conn.commit(); st.session_state[f"confirm_del_g_{s[0]}"] = False; st.rerun()
                    if c_n.button("Nie", key=f"no_{s[0]}"): st.session_state[f"confirm_del_g_{s[0]}"] = False; st.rerun()
                
                st.write("**Žiaci v skupine:**")
                ziaci = conn.execute("SELECT s.id, s.name FROM students s JOIN group_members gm ON s.id=gm.student_id WHERE gm.group_id=?", (s[0],)).fetchall()
                for z in ziaci:
                    c1, c2 = st.columns([8, 2])
                    c1.write(f"• {z[1]}")
                    if c2.button("Odobrať", key=f"rem_{s[0]}_{z[0]}"):
                        conn.execute("DELETE FROM group_members WHERE group_id=? AND student_id=?", (s[0], z[0])); conn.commit(); st.rerun()
                
                st.write("**Nahrať materiál:**")
                up_file = st.file_uploader(f"Nahrať do {s[1]}", key=f"file_{s[0]}")
                if up_file and st.button(f"Nahrať", key=f"btn_{s[0]}"):
                    url, path = upload_to_supabase(up_file.getvalue(), up_file.name, up_file.type)
                    conn.execute("INSERT INTO materials (title, link, group_id, file_path_on_cloud, uploaded_by) VALUES (?, ?, ?, ?, ?)", (up_file.name, url, s[0], path, st.session_state.tch_name))
                    conn.commit(); st.rerun()

                st.write("**Materiály:**")
                mats = conn.execute("SELECT id, title, link, file_path_on_cloud FROM materials WHERE group_id=?", (s[0],)).fetchall()
                for m in mats:
                    c1, c2 = st.columns([8, 2])
                    c1.markdown(f"• [{m[1]}]({m[2]})")
                    if c2.button("❌ Zmazať", key=f"del_m_{m[0]}"):
                        delete_from_supabase(m[3]); conn.execute("DELETE FROM materials WHERE id=?", (m[0],)); conn.commit(); st.rerun()
        conn.close()
