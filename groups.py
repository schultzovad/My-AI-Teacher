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
    # 1. Tabuľka učiteľov
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # 2. Tabuľka žiakov
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # 3. Tabuľka skupín
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            group_code TEXT UNIQUE NOT NULL,
            teacher_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    ''')
    # 4. Prepojovacia tabuľka (členovia skupín)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            student_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups (id),
            FOREIGN KEY (student_id) REFERENCES students (id),
            UNIQUE(group_id, student_id)
        )
    ''')
    # 5. Tabuľka materiálov
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
    if not supabase_client:
        return None, "Chyba: Supabase klient nie je inicializovaný."
    base_name = remove_diacritics(file_name)
    clean_name = "".join(c for c in base_name if c.isalnum() or c in "._-").strip()
    unique_name = f"{generate_group_code()}_{clean_name}"
    try:
        response = supabase_client.storage.from_(BUCKET_NAME).upload(
            path=unique_name, file=file_bytes, file_options={"content-type": mime_type}
        )
        if response:
            public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{unique_name}"
            return public_url, unique_name
    except Exception as e:
        return None, str(e)
    return None, "Neznáma chyba pri nahrávaní."

def delete_from_supabase(file_path):
    if not supabase_client: return False
    try:
        response = supabase_client.storage.from_(BUCKET_NAME).remove([file_path])
        return response is not None
    except Exception: return False

# --- ROZHRANIE STRÁNKY ---
st.title("👥 Školská platforma (Skupiny a Súbory)")

user_role = st.radio("Vyberte svoju rolu:", ["Som Žiak", "Som Učiteľ"], horizontal=True)

# ==========================================
# --- REŽIM ŽIAK ---
# ==========================================
if user_role == "Som Žiak":
    if "student_logged_in" not in st.session_state:
        st.session_state.student_logged_in = False
        st.session_state.student_id = None
        st.session_state.student_name = ""

    if not st.session_state.student_logged_in:
        tab1, tab2 = st.tabs(["Prihlásenie Žiaka", "Registrácia Žiaka"])
        with tab1:
            st.subheader("Prihlásenie pre žiakov")
            st_email = st.text_input("Email", key="st_log_email")
            st_pwd = st.text_input("Heslo", type="password", key="st_log_pwd")
            if st.button("Prihlásiť sa ako Žiak"):
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM students WHERE email = ? AND password = ?", (st_email, hash_password(st_pwd)))
                user = cursor.fetchone()
                conn.close()
                if user:
                    st.session_state.student_logged_in = True
                    st.session_state.student_id = user[0]
                    st.session_state.student_name = user[1]
                    st.rerun()
                else:
                    st.error("❌ Nesprávny email alebo heslo žiaka.")
        with tab2:
            st.subheader("Registrácia nového žiaka")
            st_reg_name = st.text_input("Meno a Priezvisko", key="st_reg_name")
            st_reg_email = st.text_input("Email", key="st_reg_email")
            st_reg_pwd = st.text_input("Heslo", type="password", key="st_reg_pwd")
            if st.button("Zaregistrovať sa ako Žiak"):
                if st_reg_name and st_reg_email and st_reg_pwd:
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", (st_reg_name, st_reg_email, hash_password(st_reg_pwd)))
                        conn.commit()
                        st.success("✅ Žiak úspešne zaregistrovaný! Teraz sa môžeš prihlásiť.")
                    except sqlite3.IntegrityError:
                        st.error("❌ Tento email už žiak používa.")
                    conn.close()
    else:
        st.write(f"🎓 **Ahoj, žiak {st.session_state.student_name}**")
        if st.button("Odhlásiť sa", key="st_logout"):
            st.session_state.student_logged_in = False
            st.rerun()
            
        st.write("---")
        
        # Načítanie skupín, v ktorých je žiak pridaný učiteľom
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT groups.id, groups.group_name, groups.group_code, teachers.name 
            FROM group_members
            JOIN groups ON group_members.group_id = groups.id
            JOIN teachers ON groups.teacher_id = teachers.id
            WHERE group_members.student_id = ?
        ''', (st.session_state.student_id,))
        moje_skupiny = cursor.fetchall()
        
        if moje_skupiny:
            st.subheader("📚 Tvoje predmety a skupiny:")
            skupiny_dict = {f"📁 {g[1]} (Učiteľ: {g[3]})": g[0] for g in moje_skupiny}
            vybrana_skupina_text = st.selectbox("Vyber si predmet na zobrazenie:", list(skupiny_dict.keys()), key="st_sk_sel")
            vybrana_skupina_id = skupiny_dict[vybrana_skupina_text]
            
            # Nahrávanie súboru žiakom do vybranej skupiny
            st.write("---")
            st.subheader("📤 Odovzdať môj súbor do tejto skupiny")
            student_file = st.file_uploader("Vyber svoj súbor:", key="student_f_up")
            if st.button("Poslať súbor spolužiakom a učiteľovi"):
                if student_file is not None:
                    with st.spinner("Nahrávam tvoju prácu..."):
                        file_bytes = student_file.getvalue()
                        public_link, error_msg = upload_to_supabase(file_bytes, student_file.name, student_file.type)
                        if public_link:
                            cursor.execute("INSERT INTO materials (title, link, group_id, file_path_on_cloud, uploaded_by) VALUES (?, ?, ?, ?, ?)", 
                                           (student_file.name, public_link, vybrana_skupina_id, error_msg, st.session_state.student_name))
                            conn.commit()
                            st.success(f"🚀 Tvoj súbor bol úspešne nahraný!")
                            st.rerun()
                        else:
                            st.error(f"❌ Detail chyby: {error_msg}")
            
            # Zobrazenie materiálov skupiny žiakovi
            st.write("---")
            cursor.execute("SELECT id, title, link, file_path_on_cloud, uploaded_by FROM materials WHERE group_id = ?", (vybrana_skupina_id,))
            materials = cursor.fetchall()
            if materials:
                st.subheader("📚 Zdieľané materiály v tejto skupine:")
                for m in materials:
                    col1, col2 = st.columns([8, 2])
                    with col1:
                        st.markdown(f"📁 [{m[1]}]({m[2]}) *(Pridal/a: {m[4]})*")
                    with col2:
                        if m[4] == st.session_state.student_name:
                            if st.button("🗑️ Odstrániť", key=f"del_st_{m[0]}"):
                                if m[3]: delete_from_supabase(m[3])
                                cursor.execute("DELETE FROM materials WHERE id = ?", (m[0],))
                                conn.commit()
                                st.rerun()
        else:
            st.info("ℹ️ Zatiaľ nie si pridaný v žiadnej skupine. Požiadaj svojho učiteľa, aby ťa pridal.")
        conn.close()

# ==========================================
# --- REŽIM UČITEĽ ---
# ==========================================
else:
    if "teacher_logged_in" not in st.session_state:
        st.session_state.teacher_logged_in = False
        st.session_state.teacher_id = None
        st.session_state.teacher_name = ""

    if not st.session_state.teacher_logged_in:
        tab1, tab2 = st.tabs(["Prihlásenie Učiteľa", "Registrácia Učiteľa"])
        with tab1:
            st.subheader("Prihlásenie pre učiteľov")
            login_email = st.text_input("Email", key="l_email")
            login_pwd = st.text_input("Heslo", type="password", key="l_pwd")
            if st.button("Prihlásiť sa ako Učiteľ"):
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
            st.subheader("Registrácia nového učiteľa")
            reg_name = st.text_input("Meno a Priezvisko")
            reg_email = st.text_input("Email")
            reg_pwd = st.text_input("Heslo", type="password")
            if st.button("Zaregistrovať sa ako Učiteľ"):
                if reg_name and reg_email and reg_pwd:
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO teachers (name, email, password) VALUES (?, ?, ?)", (reg_name, reg_email, hash_password(reg_pwd)))
                        conn.commit()
                        st.success("✅ Úspešne zaregistrované! Teraz sa môžete prihlásiť.")
                    except sqlite3.IntegrityError: 
                        st.error("❌ Tento email sa už používa.")
                    conn.close()
    else:
        st.write(f"👋 **Ahoj, profesor {st.session_state.teacher_name}**")
        if st.button("Odhlásiť sa", key="tch_logout"):
            st.session_state.teacher_logged_in = False
            st.rerun()
            
        st.write("---")
        st.subheader("🆕 Vytvoriť novú skupinu")
        n = st.text_input("Názov skupiny (napr. 4.A Biológia):")
        if st.button("Vytvoriť skupinu"):
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
            vybrana_skupina_text = st.selectbox("Vyberte skupinu pre správu:", list(skupiny_dict.keys()))
            vybrana_skupina_id = skupiny_dict[vybrana_skupina_text]
            
            # NAČÍTANIE AKTUÁLNEHO NÁZVU PRE EDITÁCIU
            cursor.execute("SELECT group_name FROM groups WHERE id = ?", (vybrana_skupina_id,))
            aktualny_nazov = cursor.fetchone()[0]
            
            # --- 🌟 NOVÉ: PREMENOVANIE SKUPINY ---
            col_rename1, col_rename2 = st.columns([7, 3])
            with col_rename1:
                novy_nazov_input = st.text_input("Upraviť názov vybranej skupiny:", value=aktualny_nazov, key=f"ren_input_{vybrana_skupina_id}")
            with col_rename2:
                st.write(" ") # odsadenie kvôli zarovnaniu s textovým polom
                st.write(" ")
                if st.button("✏️ Premenovať skupinu", key=f"ren_btn_{vybrana_skupina_id}"):
                    if novy_nazov_input.strip() != "":
                        cursor.execute("UPDATE groups SET group_name = ? WHERE id = ?", (novy_nazov_input.strip(), vybrana_skupina_id))
                        conn.commit()
                        st.success("Názov skupiny bol úspešne zmenený!")
                        st.rerun()

            st.write(" ")
            if st.button("🗑️ Vymazať celú skupinu vrátane súborov", type="primary"):
                with st.spinner("Mažem skupinu..."):
                    cursor.execute("SELECT file_path_on_cloud FROM materials WHERE group_id = ?", (vybrana_skupina_id,))
                    subory = cursor.fetchall()
                    for s in subory:
                        if s[0]: delete_from_supabase(s[0])
                    cursor.execute("DELETE FROM materials WHERE group_id = ?", (vybrana_skupina_id,))
                    cursor.execute("DELETE FROM group_members WHERE group_id = ?", (vybrana_skupina_id,))
                    cursor.execute("DELETE FROM groups WHERE id = ?", (vybrana_skupina_id,))
                    conn.commit()
                st.success("Skupina bola vymazaná.")
                st.rerun()
            
            # --- SEKCIJA PRE PRIDÁVANIE ŽIAKOV DO SKUPINY ---
            st.write("---")
            st.subheader("👥 Správa študentov v tejto skupine")
            
            cursor.execute("SELECT id, name, email FROM students")
            vsetci_studenti = cursor.fetchall()
            
            cursor.execute('''
                SELECT students.id, students.name FROM group_members 
                JOIN students ON group_members.student_id = students.id 
                WHERE group_members.group_id = ?
            ''', (vybrana_skupina_id,))
            clenovia_skupiny = cursor.fetchall()
            clenovia_ids = [s[0] for s in clenovia_skupiny]
            
            col_add, col_list = st.columns(2)
            
            with col_add:
                st.write("**Pridať žiaka do skupiny:**")
                neclenovia = [s for s in vsetci_studenti if s[0] not in clenovia_ids]
                if neclenovia:
                    student_options = {f"{s[1]} ({s[2]})": s[0] for s in neclenovia}
                    vybrany_student_na_pridanie = st.selectbox("Vyberte žiaka:", list(student_options.keys()), key="sel_st_add")
                    if st.button("➕ Pridať žiaka do skupiny"):
                        st_id = student_options[vybrany_student_na_pridanie]
                        try:
                            cursor.execute("INSERT INTO group_members (group_id, student_id) VALUES (?, ?)", (vybrana_skupina_id, st_id))
                            conn.commit()
                            st.success("Žiak bol úspešne pridaný!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Chyba: {e}")
                else:
                    st.info("Všetci registrovaní žiaci sú už v tejto skupine.")
                    
            with col_list:
                st.write("**Žiaci aktuálne v skupine:**")
                if clenovia_skupiny:
                    for clen in clenovia_skupiny:
                        c_name, c_btn = st.columns([7, 3])
                        c_name.write(f"• {clen[1]}")
                        if c_btn.button("Odobrať", key=f"rem_st_{clen[0]}"):
                            cursor.execute("DELETE FROM group_members WHERE group_id = ? AND student_id = ?", (vybrana_skupina_id, clen[0]))
                            conn.commit()
                            st.rerun()
                else:
                    st.info("V tejto skupine zatiaľ nie sú žiadni žiaci.")

            # --- SPRÁVA MATERIÁLOV ---
            st.write("---")
            st.subheader("📁 Materiály skupiny")
            typ_materialu = st.radio("Typ materiálu:", ["Nahrať súbor (Uloží sa do Supabase cloudu)", "Vložiť obyčajný internetový odkaz"], horizontal=True)
            if typ_materialu == "Nahrať súbor (Uloží sa do Supabase cloudu)":
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
                            else: st.error(f"❌ Detail chyby: {error_msg}")
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
                    with c1: st.markdown(f"🔗 [{m[1]}]({m[2]}) *(Pridal/a: {m[4]})*")
                    with c2:
                        if st.button("❌ Zmazať", key=f"del_tch_{m[0]}"):
                            if m[3]: delete_from_supabase(m[3])
                            cursor.execute("DELETE FROM materials WHERE id = ?", (m[0],))
                            conn.commit()
                            st.rerun()
        conn.close()
