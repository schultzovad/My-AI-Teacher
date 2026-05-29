import streamlit as st
import sqlite3
import hashlib
import random
import string
import unicodedata
from supabase import create_client

# --- NASTAVENIE STRÁNKY ---
st.set_page_config(layout="wide")

# Načítanie Supabase údajov zo Secrets
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = str(st.secrets.get("SUPABASE_KEY", "")).strip()
BUCKET_NAME = "materials"

# INICIALIZÁCIA OFICIÁLNEHO SUPABASE KLIENTA
supabase_client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        pass

# --- INICIALIZÁCIA DATABÁZY ---
DB_NAME = "tutor_platform.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            group_code TEXT UNIQUE NOT NULL,
            teacher_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            group_id INTEGER,
            file_path_on_cloud TEXT,
            uploaded_by TEXT DEFAULT 'Učiteľ',
            FOREIGN KEY (group_id) REFERENCES groups (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_group_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def remove_diacritics(text):
    """Odstráni slovenské dĺžne a mäkčene z názvu súboru pre Supabase."""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def upload_to_supabase(file_bytes, file_name, mime_type):
    """Odošle súbor a v prípade zlyhania vráti skutočnú textovú chybu."""
    if not supabase_client:
        return None, "Chyba: Supabase klient nie je inicializovaný. Skontroluj Secrets."
        
    # Odstránenie diakritiky a nepovolených znakov
    base_name = remove_diacritics(file_name)
    clean_name = "".join(c for c in base_name if c.isalnum() or c in "._-").strip()
    unique_name = f"{generate_group_code()}_{clean_name}"
    
    try:
        response = supabase_client.storage.from_(BUCKET_NAME).upload(
            path=unique_name,
            file=file_bytes,
            file_options={"content-type": mime_type}
        )
        if response:
            public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{unique_name}"
            return public_url, unique_name
    except Exception as e:
        return None, str(e)
        
    return None, "Neznáma chyba pri nahrávaní."

def delete_from_supabase(file_path):
    if not supabase_client:
        return False
    try:
        response = supabase_client.storage.from_(BUCKET_NAME).remove([file_path])
        return response is not None
    except Exception:
        return False

# --- JAZYKOVÉ DATA ---
lang_data = {
    "SK": {
        "title": "👥 Študijné skupiny", "label": "Názov skupiny", "btn": "Vytvoriť", 
        "login": "Prihlásenie", "register": "Registrácia", "logout": "Odhlásiť sa", 
        "role_teacher": "Som Učiteľ", "role_student": "Som Žiak", "code_label": "Zadaj kód skupiny", 
        "join_btn": "Vstúpiť do skupiny", "name_input": "Meno", "pwd_input": "Heslo",
        "type_cloud": "Nahrať súbor (Uloží sa do Supabase cloudu)", "type_link": "Vložiť obyčajný internetový odkaz"
    }
}

L = st.query_params.get("lang", "SK")
t = lang_data.get(L, lang_data["SK"])

st.title(t["title"])

user_role = st.radio("Vyberte svoju rolu:", [t["role_student"], t["role_teacher"]], horizontal=True)

# --- REŽIM ŽIAK ---
if user_role == t["role_student"]:
    st.write("---")
    student_name = st.text_input(f"Tvoje {t['name_input'].lower()}:", key="st_name").strip()
    group_code_input = st.text_input(t["code_label"], key="g_code").strip().upper()
    
    if student_name and group_code_input:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, group_name FROM groups WHERE group_code = ?", (group_code_input,))
        group = cursor.fetchone()
        
        if group:
            st.success(f"🎉 Vitaj v skupine: **{group[1]}**")
            
            st.write("---")
            st.subheader("📤 Odovzdať môj súbor do skupiny")
            student_file = st.file_uploader("Vyber svoj súbor:", key="file_uploader_student")
            if st.button("Poslať súbor spolužiakom a učiteľovi"):
                if student_file is not None:
                    with st.spinner("Nahrávam tvoju prácu..."):
                        file_bytes = student_file.getvalue()
                        public_link, error_msg = upload_to_supabase(file_bytes, student_file.name, student_file.type)
                        if public_link:
                            cursor.execute("INSERT INTO materials (title, link, group_id, file_path_on_cloud, uploaded_by) VALUES (?, ?, ?, ?, ?)", 
                                           (student_file.name, public_link, group[0], error_msg, student_name))
                            conn.commit()
                            st.success(f"🚀 Tvoj súbor bol úspešne nahraný!")
                            st.rerun()
                        else:
                            st.error(f"❌ Detail chyby zo Supabase: {error_msg}")
            
            st.write("---")
            cursor.execute("SELECT id, title, link, file_path_on_cloud, uploaded_by FROM materials WHERE group_id = ?", (group[0],))
            materials = cursor.fetchall()
            if materials:
                st.subheader("📚 Spoločné materiály:")
                for m in materials:
                    col1, col2 = st.columns([8, 2])
                    with col1:
                        st.markdown(f"📁 [{m[1]}]({m[2]}) *(Pridal/a: {m[4]})*")
                    with col2:
                        if m[4] == student_name:
                            if st.button("🗑️ Odstrániť", key=f"del_st_{m[0]}"):
                                if m[3]: delete_from_supabase(m[3])
                                cursor.execute("DELETE FROM materials WHERE id = ?", (m[0],))
                                conn.commit()
                                st.rerun()
        conn.close()

# --- REŽIM UČITEĽ ---
else:
    if "teacher_logged_in" not in st.session_state:
        st.session_state.teacher_logged_in = False
        st.session_state.teacher_id = None
        st.session_state.teacher_name = ""

    if not st.session_state.teacher_logged_in:
        tab1, tab2 = st.tabs([t["login"], t["register"]])
        with tab1:
            st.subheader(t["login"])
            login_email = st.text_input("Email", key="l_email")
            login_pwd = st.text_input(t["pwd_input"], type="password", key="l_pwd")
            if st.button(t["login"]):
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM teachers WHERE email = ? AND password = ?", (login_email, hash_password(login_pwd)))
                user = cursor.fetchone()
                conn.close()
                if user:
                    st.session_state.teacher_logged_in = True
                    st.session_state.teacher_id = user[0]
                    st.session_state.teacher_name = user[1]
                    st.rerun()
                else:
                    st.error("❌ Nesprávny email alebo heslo.")
        with tab2:
            st.subheader(t["register"])
            reg_name = st.text_input(t["name_input"])
            reg_email = st.text_input("Email")
            reg_pwd = st.text_input(t["pwd_input"], type="password")
            if st.button(t["register"]):
                if reg_name and reg_email and reg_pwd:
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO teachers (name, email, password) VALUES (?, ?, ?)", (reg_name, reg_email, hash_password(reg_pwd)))
                        conn.commit()
                        
                        cursor.execute("SELECT id, name FROM teachers WHERE email = ?", (reg_email,))
                        new_user = cursor.fetchone()
                        if new_user:
                            st.session_state.teacher_logged_in = True
                            st.session_state.teacher_id = new_user[0]
                            st.session_state.teacher_name = new_user[1]
                        conn.close()
                        st.success("✅ Úspešne zaregistrované!")
                        st.rerun()
                    except sqlite3.IntegrityError: 
                        st.error("❌ Email sa používa.")
                        conn.close()
    else:
        st.write(f"👋 **Ahoj, profesor {st.session_state.teacher_name}**")
        if st.button(t["logout"]):
            st.session_state.teacher_logged_in = False
            st.rerun()
            
        st.write("---")
        st.subheader("🆕 Vytvoriť novú skupinu")
        n = st.text_input(t["label"])
        if st.button(t["btn"]):
            if n.strip() != "":
                code = generate_group_code()
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO groups (group_name, group_code, teacher_id) VALUES (?, ?, ?)", (n, code, st.session_state.teacher_id))
                conn.commit()
                conn.close()
                st.rerun()
        
        st.write("---")
        st.subheader("⚙️ Správa vašich skupín a materiálov")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, group_name, group_code FROM groups WHERE teacher_id = ?", (st.session_state.teacher_id,))
        moje_skupiny = cursor.fetchall()
        
        if moje_skupiny:
            skupiny_dict = {f"📁 {g[1]} (Kód: {g[2]})": g[0] for g in moje_skupiny}
            vybrana_skupina_text = st.selectbox("Vyberte skupinu:", list(skupiny_dict.keys()))
            vybrana_skupina_id = skupiny_dict[vybrana_skupina_text]
            
            typ_materialu = st.radio("Typ materiálu:", [t["type_cloud"], t["type_link"]], horizontal=True)
            if typ_materialu == t["type_cloud"]:
                uploaded_file = st.file_uploader("Vyberte súbor:")
                if st.button("Zdieľať súbor cez Cloud"):
                    if uploaded_file is not None:
                        with st.spinner("Zdieľam súbor..."):
                            file_bytes = uploaded_file.getvalue()
                            public_link, error_msg = upload_to_supabase(file_bytes, uploaded_file.name, uploaded_file.type)
                            if public_link:
                                cursor.execute("INSERT INTO materials (title, link, group_id, file_path_on_cloud, uploaded_by) VALUES (?, ?, ?, ?, 'Učiteľ')", (uploaded_file.name, public_link, vybrana_skupina_id, error_msg))
                                conn.commit()
                                st.rerun()
                            else:
                                st.error(f"❌ Detail chyby zo Supabase: {error_msg}")
            else:
                mat_title = st.text_input("Názov odkazu:")
                mat_link = st.text_input("Odkaz (URL):")
                if st.button("Zdieľať odkaz"):
                    if mat_title and mat_link:
                        cursor.execute("INSERT INTO materials (title, link, group_id, file_path_on_cloud, uploaded_by) VALUES (?, ?, ?, NULL, 'Učiteľ')", (mat_title, mat_link, vybrana_skupina_id))
                        conn.commit()
                        st.rerun()
            
            cursor.execute("SELECT id, title, link, file_path_on_cloud, uploaded_by FROM materials WHERE group_id = ?", (vybrana_skupina_id,))
            skupina_materialy = cursor.fetchall()
            if skupina_materialy:
                for m in skupina_materialy:
                    c1, c2 = st.columns([8, 2])
                    with c1:
                        st.markdown(f"🔗 [{m[1]}]({m[2]}) *(Pridal/a: {m[4]})*")
                    with c2:
                        if st.button("❌ Zmazať", key=f"del_tch_{m[0]}"):
                            if m[3]: delete_from_supabase(m[3])
                            cursor.execute("DELETE FROM materials WHERE id = ?", (m[0],))
                            conn.commit()
                            st.rerun()
        conn.close()
