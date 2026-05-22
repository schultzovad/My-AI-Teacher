import streamlit as st
import sqlite3
import hashlib

# --- NASTAVENIE STRÁNKY A ŠTÝLU ---
st.set_page_config(layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>", unsafe_allow_html=True)

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
    # Tabuľka pre skupiny
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            teacher_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- JAZYKOVÉ DATA ---
lang_data = {
    "SK": {"title": "👥 Študijné skupiny", "label": "Názov skupiny", "btn": "Vytvoriť", "login": "Prihlásenie učiteľa", "register": "Registrácia nového učiteľa", "logout": "Odhlásiť sa", "no_acc": "Nemáte účet? Zaregistrujte sa", "have_acc": "Už máte účet? Prihláste sa"},
    "EN": {"title": "👥 Study Groups", "label": "Group name", "btn": "Create", "login": "Teacher Login", "register": "Teacher Registration", "logout": "Log out", "no_acc": "No account? Register", "have_acc": "Have an account? Log in"},
    "DE": {"title": "👥 Studiengruppen", "label": "Name", "btn": "Erstellen", "login": "Lehrer-Login", "register": "Lehrer-Registrierung", "logout": "Abmelden", "no_acc": "Kein Konto? Registrieren", "have_acc": "Konto vorhanden? Einloggen"},
    "ES": {"title": "👥 Grupos", "label": "Nombre", "btn": "Crear", "login": "Iniciar sesión", "register": "Registrarse", "logout": "Cerrar sesión", "no_acc": "¿No tienes cuenta?", "have_acc": "¿Ya tienes cuenta?"},
    "FR": {"title": "👥 Groupes", "label": "Nom", "btn": "Créer", "login": "Connexion", "register": "Inscription", "logout": "Déconnexion", "no_acc": "Pas de compte?", "have_acc": "Déjà inscrit?"},
    "IT": {"title": "👥 Gruppi", "label": "Nome", "btn": "Crea", "login": "Accesso", "register": "Registrazione", "logout": "Disconnetti", "no_acc": "Non hai un account?", "have_acc": "Hai già un account?"},
    "UA": {"title": "👥 Групи", "label": "Назва", "btn": "Створити", "login": "Вхід для вчителів", "register": "Реєстрація вчителя", "logout": "Вийти", "no_acc": "Немає акаунту?", "have_acc": "Вже є акаунт?"},
    "RU": {"title": "👥 Группы", "label": "Название", "btn": "Создать", "login": "Вход для учителей", "register": "Регистрация учителя", "logout": "Выйти", "no_acc": "Нет аккаунта?", "have_acc": "Уже есть аккаунт?"}
}

L = st.query_params.get("lang", "SK")
t = lang_data.get(L, lang_data["SK"])

st.title(t["title"])

# --- SPRÁVA PRIHLÁSENIA (SESSION STATE) ---
if "teacher_logged_in" not in st.session_state:
    st.session_state.teacher_logged_in = False
    st.session_state.teacher_id = None
    st.session_state.teacher_name = ""

# --- BOČNÝ PANEL: PRIHLÁSENIE / REGISTRÁCIA ---
with st.sidebar:
    if not st.session_state.teacher_logged_in:
        menu_mode = st.radio("Menu", [t["login"], t["register"]], label_visibility="collapsed")
        
        if menu_mode == t["login"]:
            st.subheader(t["login"])
            login_email = st.text_input("Email", key="l_email")
            login_pwd = st.text_input("Heslo / Password", type="password", key="l_pwd")
            
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
                    
        elif menu_mode == t["register"]:
            st.subheader(t["register"])
            reg_name = st.text_input("Meno / Name")
            reg_email = st.text_input("Email")
            reg_pwd = st.text_input("Heslo / Password", type="password")
            
            if st.button(t["register"]):
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
        st.write(f"👋 {st.session_state.teacher_name}")
        if st.button(t["logout"]):
            st.session_state.teacher_logged_in = False
            st.session_state.teacher_id = None
            st.session_state.teacher_name = ""
            st.rerun()

# --- HLAVNÁ ČASŤ STRÁNKY ---
if st.session_state.teacher_logged_in:
    # Učiteľ je prihlásený, môže vytvárať skupiny
    n = st.text_input(t["label"])
    if st.button(t["btn"]):
        if n.strip() != "":
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO groups (group_name, teacher_id) VALUES (?, ?)", (n, st.session_state.teacher_id))
            conn.commit()
            conn.close()
            
            st.balloons()
            st.success(f"{t['title']}: '{n}'")
        else:
            st.warning("⚠️ Názov skupiny nemôže byť prázdny.")
            
    # Zobrazenie existujúcich skupín daného učiteľa
    st.write("---")
    st.subheader("Vaše vytvorené skupiny:")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT group_name FROM groups WHERE teacher_id = ?", (st.session_state.teacher_id,))
    moje_skupiny = cursor.fetchall()
    conn.close()
    
    if moje_skupiny:
        for g in moje_skupiny:
            st.markdown(f"📁 **{g[0]}**")
    else:
        st.info("Zatiaľ ste nevytvorili žiadnu skupinu.")
else:
    # Ak učiteľ nie je prihlásený
    st.info("🔒 Pre vytváranie skupín a zdieľanie materiálov sa prosím prihláste v bočnom paneli vľavo.")
