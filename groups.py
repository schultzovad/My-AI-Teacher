import streamlit as st
import sqlite3
import hashlib
import random
import string
import requests

# --- NASTAVENIE STRÁNKY ---
st.set_page_config(layout="wide")

# Načítanie Supabase údajov zo Secrets
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
BUCKET_NAME = "materials"

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

def upload_to_supabase(file_bytes, file_name, mime_type):
    """Odošle súbor priamo do Supabase Storage a vráti naň verejný odkaz."""
    clean_name = "".join(c for c in file_name if c.isalnum() or c in "._-").strip()
    unique_name = f"{generate_group_code()}_{clean_name}"
    
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{unique_name}"
    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "API-KEY": SUPABASE_KEY,
        "Content-Type": mime_type
    }
    
    response = requests.post(url, headers=headers, data=file_bytes)
    
    if response.status_code == 200:
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{unique_name}"
        return public_url
    return None

# --- JAZYKOVÉ DATA (VRÁTENÉ VŠETKY JAZYKY + TVOJE ÚPRAWY) ---
lang_data = {
    "SK": {
        "title": "👥 Študijné skupiny", "label": "Názov skupiny", "btn": "Vytvoriť", 
        "login": "Prihlásenie", "register": "Registrácia", "logout": "Odhlásiť sa", 
        "role_teacher": "Som Učiteľ", "role_student": "Som Žiak", "code_label": "Zadaj kód skupiny", 
        "join_btn": "Vstúpiť do skupiny", "name_input": "Meno", "pwd_input": "Heslo",
        "type_cloud": "Nahrať súbor (Uloží sa do Supabase cloudu)", "type_link": "Vložiť obyčajný internetový odkaz"
    },
    "EN": {
        "title": "👥 Study Groups", "label": "Group name", "btn": "Create", 
        "login": "Login", "register": "Registration", "logout": "Log out", 
        "role_teacher": "I am a Teacher", "role_student": "I am a Student", "code_label": "Enter group code", 
        "join_btn": "Join Group", "name_input": "Name", "pwd_input": "Password",
        "type_cloud": "Upload file to Cloud", "type_link": "Insert web link (URL)"
    },
    "DE": {
        "title": "👥 Studiengruppen", "label": "Name", "btn": "Erstellen", 
        "login": "Login", "register": "Registrierung", "logout": "Abmelden", 
        "role_teacher": "Ich bin Lehrer", "role_student": "Ich bin Schüler", "code_label": "Gruppencode eingeben", 
        "join_btn": "Gruppe beitreten", "name_input": "Name", "pwd_input": "Passwort",
        "type_cloud": "Datei in die Cloud hochladen", "type_link": "Internetlink einfügen"
    },
    "ES": {
        "title": "👥 Grupos", "label": "Nombre", "btn": "Crear", 
        "login": "Iniciar sesión", "register": "Registrarse", "logout": "Cerrar sesión", 
        "role_teacher": "Soy Profesor", "role_student": "Soy Estudiante", "code_label": "Código de grupo", 
        "join_btn": "Unirse al grupo", "name_input": "Nombre", "pwd_input": "Contraseña",
        "type_cloud": "Subir archivo a la nube", "type_link": "Insertar enlace de internet"
    },
    "FR": {
        "title": "👥 Groupes", "label": "Nom", "btn": "Créer", 
        "login": "Connexion", "register": "Inscription", "logout": "Déconnexion", 
        "role_teacher": "Je suis Enseignant", "role_student": "Je suis Étudiant", "code_label": "Code du groupe", 
        "join_btn": "Rejoindre le groupe", "name_input": "Nom", "pwd_input": "Mot de passe",
        "type_cloud": "Téléverser sur le Cloud", "type_link": "Insérer un lien internet"
    },
    "IT": {
        "title": "👥 Gruppi", "label": "Nome", "btn": "Crea", 
        "login": "Accesso", "register": "Registrazione", "logout": "Disconnetti", 
        "role_teacher": "Sono un Insegnante", "role_student": "Sono uno Studente", "code_label": "Codice gruppo", 
        "join_btn": "Entra nel gruppo", "name_input": "Nome", "pwd_input": "Password",
        "type_cloud": "Carica file sul Cloud", "type_link": "Inserisci collegamento internet"
    },
    "UA": {
        "title": "👥 Групи", "label": "Назва", "btn": "Створити", 
        "login": "Вхід", "register": "Реєстрація", "logout": "Вийти", 
        "role_teacher": "Я вчитель", "role_student": "Я учень", "code_label": "Введіть код групи", 
        "join_btn": "Увійти в групу", "name_input": "Ім'я", "pwd_input": "Пароль",
        "type_cloud": "Завантажити файл у хмару", "type_link": "Вставити інтернет-посилання"
    },
    "RU": {
        "title": "👥 Группы", "label": "Название", "btn": "Создать", 
        "login": "Вход", "register": "Регистрация", "logout": "Выйти", 
        "role_teacher": "Я учитель", "role_student": "Я ученик", "code_label": "Введите код группы", 
        "join_btn": "Войти в группу", "name_input": "Имя", "pwd_input": "Пароль",
        "type_cloud": "Загрузить файл в облако", "type_link": "Вставить интернет-ссылку"
    }
}

L = st.query_params.get("lang", "SK")
t = lang_data.get(L, lang_data["SK"])

st.title(t["title"])

user_role = st.radio("Vyberte svoju rolu:", [t["role_student"], t["role_teacher"]], horizontal=True)

# --- REŽIM ŽIAK ---
if user_role == t["role_student"]:
    st.write("---")
    student_name = st.text_input(f"Tvoje {t['name_input'].lower()}:", key="st_name")
    group_code_input = st.text_input(t["code_label"], key="g_code").strip().upper()
    
    if st.button(t["join_btn"]):
        if student_name and group_code_input:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT id, group_name FROM groups WHERE group_code = ?", (group_code_input,))
            group = cursor.fetchone()
            
            if group:
                st.success(f"🎉 Vitaj v skupine: **{group[1]}**")
                
                cursor.execute("SELECT title, link FROM materials WHERE group_id = ?", (group[0],))
                materials = cursor.fetchall()
                conn.close()
                
                if materials:
                    st.subheader("📚 Spoločné materiály na štúdium:")
                    for m in materials:
                        st.markdown(f"📁 [{m[0]}]({m[1]})")
                else:
                    st.info("Učiteľ zatiaľ do tejto skupiny nepridal žiadne materiály.")
            else:
                st.error("❌ Nesprávny kód skupiny.")
                conn.close()
        else:
            st.warning("⚠️ Vyplň svoje meno aj kód skupiny.")

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
            if st.button(t["login"], key="btn_login_main"):
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
                else: st.error("❌ Nesprávny email alebo heslo.")
        with tab2:
            st.subheader(t["register"])
            reg_name = st.text_input(t["name_input"], key="r_name")
            reg_email = st.text_input("Email", key="r_email")
            reg_pwd = st.text_input(t["pwd_input"], type="password", key="r_pwd")
            if st.button(t["register"], key="btn_reg_main"):
                if reg_name and reg_email and reg_pwd:
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO teachers (name, email, password) VALUES (?, ?, ?)", (reg_name, reg_email, hash_password(reg_pwd)))
                        conn.commit()
                        st.success("✅ Úspešne zaregistrované!")
                    except sqlite3.IntegrityError: st.error("❌ Email sa používa.")
                    conn.close()
                else: st.warning("⚠️ Vyplňte polia.")
    else:
        st.write(f"👋 **Ahoj, profesor {st.session_state.teacher_name}**")
        if st.button(t["logout"]):
            st.session_state.teacher_logged_in = False
            st.session_state.teacher_id = None
            st.session_state.teacher_name = ""
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
                st.balloons()
                st.success(f"Skupina vytvorená s kódom: **{code}**")
                st.rerun()
        
        st.write("---")
        st.subheader("⚙️ Správa vašich skupín a materiálov")
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, group_name, group_code FROM groups WHERE teacher_id = ?", (st.session_state.teacher_id,))
        moje_skupiny = cursor.fetchall()
        
        if moje_skupiny:
            skupiny_dict = {f"📁 {g[1]} (Kód: {g[2]})": g[0] for g in moje_skupiny}
            vybrana_skupina_text = st.selectbox("Vyberte skupinu pre pridanie materiálu:", list(skupiny_dict.keys()))
            vybrana_skupina_id = skupiny_dict[vybrana_skupina_text]
            
            typ_materialu = st.radio("Typ materiálu:", [t["type_cloud"], t["type_link"]], horizontal=True)
            
            if typ_materialu == t["type_cloud"]:
                uploaded_file = st.file_uploader("Vyberte súbor (PDF, Word, Obrázok...):")
                if st.button("Zdieľať súbor cez Cloud"):
                    if uploaded_file is not None and SUPABASE_URL and SUPABASE_KEY:
                        with st.spinner("Nahrávam súbor do zabezpečeného cloudu..."):
                            file_bytes = uploaded_file.getvalue()
                            public_link = upload_to_supabase(file_bytes, uploaded_file.name, uploaded_file.type)
                            
                            if public_link:
                                cursor.execute("INSERT INTO materials (title, link, group_id) VALUES (?, ?, ?)", (uploaded_file.name, public_link, vybrana_skupina_id))
                                conn.commit()
                                st.success(f"🚀 Súbor úspešne nahraný do cloudu!")
                                st.rerun()
                            else:
                                st.error("❌ Nepodarilo sa odoslať súbor do Supabase. Skontroluj Secrets.")
                    else:
                        st.warning("⚠️ Vyber súbor a over nastavenie kľúčov v Secrets.")
            else:
                mat_title = st.text_input("Názov odkazu:")
                mat_link = st.text_input("Odkaz (URL):")
                if st.button("Zdieľať odkaz"):
                    if mat_title and mat_link:
                        cursor.execute("INSERT INTO materials (title, link, group_id) VALUES (?, ?, ?)", (mat_title, mat_link, vybrana_skupina_id))
                        conn.commit()
                        st.success("✅ Odkaz úspešne pridaný!")
                        st.rerun()
            
            st.write("Doterajšie materiály v tejto skupine:")
            cursor.execute("SELECT title, link FROM materials WHERE group_id = ?", (vybrana_skupina_id,))
            skupina_materialy = cursor.fetchall()
            if skupina_materialy:
                for m in skupina_materialy:
                    st.markdown(f"🔗 [{m[0]}]({m[1]})")
            else: st.caption("Zatiaľ žiadne materiály.")
        conn.close()
