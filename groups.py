import streamlit as st
import sqlite3
import hashlib

# --- NASTAVENIE STRÁNKY ---
st.set_page_config(layout="wide")

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
    "SK": {"title": "👥 Študijné skupiny", "label": "Názov skupiny", "btn": "Vytvoriť", "login": "Prihlásenie", "register": "Registrácia", "logout": "Odhlásiť sa"},
    "EN": {"title": "👥 Study Groups", "label": "Group name", "btn": "Create", "login": "Login", "register": "Registration", "logout": "Log out"},
    "DE": {"title": "👥 Studiengruppen", "label": "Name", "btn": "Erstellen", "login": "Login", "register": "Registrierung", "logout": "Abmelden"},
    "ES": {"title": "👥 Grupos", "label": "Nombre", "btn": "Crear", "login": "Iniciar sesión", "register": "Registrarse", "logout": "Cerrar sesión"},
    "FR": {"title": "👥 Groupes", "label": "Nom", "btn": "Créer", "login": "Connexion", "register": "Inscription", "logout": "Déconnexion"},
    "IT": {"title": "👥 Gruppi", "label": "Nome", "btn": "Crea", "login": "Accesso", "register": "Registrazione", "logout": "Disconnetti"},
    "UA": {"title": "👥 Групи", "label": "Назва", "btn": "Створити", "login": "Вхід", "register": "Реєстрація", "logout": "Вийти"},
    "RU": {"title": "👥 Группы", "label": "Название", "btn": "Создать", "login": "Вход", "register": "Регистрация", "logout": "Выйти"}
}

L = st.query_params.get("lang", "SK")
t = lang_data.get(L, lang_data["SK"])

st.title(t["title"])

# --- SESSION STATE ---
if "teacher_logged_in" not in st.session_state:
    st.session_state.teacher_logged_in = False
    st.session_state.teacher_id = None
    st.session_state.teacher_name = ""

# --- HLAVNÁ LOGIKA BEZ SIDEBARU ---
if not st.session_state.teacher_logged_in:
    # Vytvoríme pekné záložky (Tabs) priamo v strede stránky
    tab1, tab2 = st.tabs([t["login"], t["register"]])
    
    with tab1:
        st.subheader(t["login"])
        login_email = st.text_input("Email", key="l_email")
        login_pwd = st.text_input("Heslo / Password", type="password", key="l_pwd")
        
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
                    st.success("✅ Úspešne zaregistrované! Teraz sa môžete v prvej záložke prihlásiť.")
                except sqlite3.IntegrityError:
                    st.error("❌ Tento email sa už používa.")
                conn.close()
            else:
                st.warning("⚠️ Vyplňte všetky polia.")

else:
    # Učiteľ je úspešne prihlásený - vidí správu skupín
    st.write(f"👋 **Ahoj, {st.session_state.teacher_name}**")
    if st.button(t["logout"]):
        st.session_state.teacher_logged_in = False
        st.session_state.teacher_id = None
        st.session_state.teacher_name = ""
        st.rerun()
        
    st.write("---")
    
    # Formulár na vytvorenie skupiny
    n = st.text_input(t["label"])
    if st.button(t["btn"]):
        if n.strip() != "":
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO groups (group_name, teacher_id) VALUES (?, ?)", (n, st.session_state.teacher_id))
            conn.commit()
            conn.close()
            
            st.balloons()
            st.success(f"Skupina '{n}' úspešne vytvorená!")
        else:
            st.warning("⚠️ Názov skupiny nemôže byť prázdny.")
            
    # Zobrazenie skupín
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
