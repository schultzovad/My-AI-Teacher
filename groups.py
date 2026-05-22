import streamlit as st
import sqlite3
import hashlib
import random
import string

# --- NASTAVENIE STRÁNKY ---
st.set_page_config(layout="wide")

# --- INICIALIZÁCIA DATABÁZY ---
DB_NAME = "tutor_platform.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabuľka pre učiteľov
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Tabuľka pre skupiny (pridaný unikátny kód skupiny)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            group_code TEXT UNIQUE NOT NULL,
            teacher_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    ''')
    # Tabuľka pre materiály zdieľané v skupinách
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
    """Vygeneruje náhodný 5-miestny kód z veľkých písmen a čísel."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# --- JAZYKOVÉ DATA ---
lang_data = {
    "SK": {"title": "👥 Študijné skupiny", "label": "Názov skupiny", "btn": "Vytvoriť", "login": "Prihlásenie", "register": "Registrácia", "logout": "Odhlásiť sa", "role_teacher": "Som Učiteľ", "role_student": "Som Žiak", "code_label": "Zadaj kód skupiny", "join_btn": "Vstúpiť do skupiny"},
    "EN": {"title": "👥 Study Groups", "label": "Group name", "btn": "Create", "login": "Login", "register": "Registration", "logout": "Log out", "role_teacher": "I am a Teacher", "role_student": "I am a Student", "code_label": "Enter group code", "join_btn": "Join Group"},
    "DE": {"title": "👥 Studiengruppen", "label": "Name", "btn": "Erstellen", "login": "Login", "register": "Registrierung", "logout": "Abmelden", "role_teacher": "Ich bin Lehrer", "role_student": "Ich bin Schüler", "code_label": "Gruppencode eingeben", "join_btn": "Gruppe beitreten"},
    "ES": {"title": "👥 Grupos", "label": "Nombre", "btn": "Crear", "login": "Iniciar sesión", "register": "Registrarse", "logout": "Cerrar sesión", "role_teacher": "Soy Profesor", "role_student": "Soy Estudiante", "code_label": "Código de grupo", "join_btn": "Unirse al grupo"},
    "FR": {"title": "👥 Groupes", "label": "Nom", "btn": "Créer", "login": "Connexion", "register": "Inscription", "logout": "Déconnexion", "role_teacher": "Je suis Enseignant", "role_student": "Je suis Étudiant", "code_label": "Code du groupe", "join_btn": "Rejoindre le groupe"},
    "IT": {"title": "👥 Gruppi", "label": "Nome", "btn": "Crea", "login": "Accesso", "register": "Registrazione", "logout": "Disconnetti", "role_teacher": "Sono un Insegnante", "role_student": "Sono uno Studente", "code_label": "Codice gruppo", "join_btn": "Entra nel gruppo"},
    "UA": {"title": "👥 Групи", "label": "Назва", "btn": "Створити", "login": "Вхід", "register": "Реєстрація", "logout": "Вийти", "role_teacher": "Я вчитель", "role_student": "Я учень", "code_label": "Введіть код групи", "join_btn": "Увійти в групу"},
    "RU": {"title": "👥 Группы", "label": "Название", "btn": "Создать", "login": "Вход", "register": "Регистрация", "logout": "Выйти", "role_teacher": "Я учитель", "role_student": "Я ученик", "code_label": "Введите код группы", "join_btn": "Войти в группу"}
}

L = st.query_params.get("lang", "SK")
t = lang_data.get(L, lang_data["SK"])

st.title(t["title"])

# Rozcestník na začiatku: Vyber si, kto si
user_role = st.radio("Vyberte svoju rolu / Select your role:", [t["role_student"], t["role_teacher"]], horizontal=True)

# --- REŽIM ŽIAK ---
if user_role == t["role_student"]:
    st.write("---")
    student_name = st.text_input("Tvoje meno / Your name:", key="st_name")
    group_code_input = st.text_input(t["code_label"], key="g_code").strip().upper()
    
    if st.button(t["join_btn"]):
        if student_name and group_code_input:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT id, group_name FROM groups WHERE group_code = ?", (group_code_input,))
            group = cursor.fetchone()
            
            if group:
                st.success(f"🎉 Vitaj v skupine: **{group[1]}**")
                
                # Načítanie materiálov pre túto skupinu
                cursor.execute("SELECT title, link FROM materials WHERE group_id = ?", (group[0],))
                materials = cursor.fetchall()
                conn.close()
                
                if materials:
                    st.subheader("📚 Spoločné materiály na štúdium:")
                    for m in materials:
                        st.markdown(f"🔗 [{m[0]}]({m[1]})")
                else:
                    st.info("Učiteľ zatiaľ do tejto skupiny nepridal žiadne materiály.")
            else:
                st.error("❌ Nesprávny kód skupiny. Skontroluj preklepy.")
                conn.close()
        else:
            st.warning("⚠️ Vyplň svoje meno aj kód skupiny.")

# --- REŽIM UČITEĽ ---
else:
    # SESSION STATE pre učiteľa
    if "teacher_logged_in" not in st.session_state:
        st.session_state.teacher_logged_in = False
        st.session_state.teacher_id = None
        st.session_state.teacher_name = ""

    if not st.session_state.teacher_logged_in:
        tab1, tab2 = st.tabs([t["login"], t["register"]])
        
        with tab1:
            st.subheader(t["login"])
            login_email = st.text_input("Email", key="l_email")
            login_pwd = st.text_input("Heslo", type="password", key="l_pwd")
            
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
                else:
                    st.error("❌ Nesprávny email alebo heslo.")
                    
        with tab2:
            st.subheader(t["register"])
            reg_name = st.text_input("Meno", key="r_name")
            reg_email = st.text_input("Email", key="r_email")
            reg_pwd = st.text_input("Heslo", type="password", key="r_pwd")
            
            if st.button(t["register"], key="btn_reg_main"):
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
                    st.warning("⚠️ Vyplňte všetky polia.")

    else:
        # Učiteľ je prihlásený
        st.write(f"👋 **Ahoj, profesor {st.session_state.teacher_name}**")
        if st.button(t["logout"]):
            st.session_state.teacher_logged_in = False
            st.session_state.teacher_id = None
            st.session_state.teacher_name = ""
            st.rerun()
            
        st.write("---")
        
        # 1. FORMULÁR NA VYTVORENIE SKUPINY
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
                st.success(f"Skupina '{n}' úspešne vytvorená s kódom: **{code}**")
                st.rerun()
            else:
                st.warning("⚠️ Názov skupiny nemôže byť prázdny.")
                
        st.write("---")
        
        # 2. SPRÁVA EXISTUJÚCICH SKUPÍN A PRIDÁVANIE MATERIÁLOV
        st.subheader("⚙️ Správa vašich skupín a materiálov")
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, group_name, group_code FROM groups WHERE teacher_id = ?", (st.session_state.teacher_id,))
        moje_skupiny = cursor.fetchall()
        
        if moje_skupiny:
            # Učiteľ si z roletky vyberie, do ktorej svojej skupiny ide pridať materiál
            skupiny_dict = {f"📁 {g[1]} (Kód: {g[2]})": g[0] for g in moje_skupiny}
            vybrana_skupina_text = st.selectbox("Vyberte skupinu pre pridanie materiálu:", list(skupiny_dict.keys()))
            vybrana_skupina_id = skupiny_dict[vybrana_skupina_text]
            
            # Formulár na pridanie linku
            mat_title = st.text_input("Názov materiálu (napr. Úloha na piatok, Prezentácia):")
            mat_link = st.text_input("Webový odkaz na materiál (Google Drive link, atď.):")
            
            if st.button("Zdieľať materiál v skupine"):
                if mat_title and mat_link:
                    cursor.execute("INSERT INTO materials (title, link, group_id) VALUES (?, ?, ?)", (mat_title, mat_link, vybrana_skupina_id))
                    conn.commit()
                    st.success(f"✅ Materiál '{mat_title}' bol úspešne pridaný!")
                else:
                    st.warning("⚠️ Vyplňte názov aj odkaz.")
            
            # Ukážka doterajších materiálov v tejto vybranej skupine
            st.write("Current materiály v tejto skupine:")
            cursor.execute("SELECT title, link FROM materials WHERE group_id = ?", (vybrana_skupina_id,))
            skupina_materialy = cursor.fetchall()
            if skupina_materialy:
                for m in skupina_materialy:
                    st.markdown(f"📄 [{m[0]}]({m[1]})")
            else:
                st.caption("V tejto skupine zatiaľ nie sú žiadne odkazy.")
                
        else:
            st.info("Zatiaľ ste nevytvorili žiadnu skupinu. Vytvorte ju vyššie.")
            
        conn.close()
