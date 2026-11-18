import sqlite3
import bcrypt
import streamlit as st

DB_NAME = "users.db"

st.set_page_config(page_title="NEXORA | Digital Identity", page_icon="✨", layout="centered")

st.markdown("""
<style>
/* Your existing CSS */
.stApp {
    background: linear-gradient(...);
}

/* New CSS — paste here */
.stTextInput input {
    color: #1e293b !important;
    background-color: #ffffff !important;
}

.stAlert,
.stAlert p,
.stAlert div {
    color: #1e293b !important;
}

.stTextInput input::placeholder {
    color: #64748b !important;
    opacity: 1;
}
</style>
.stApp { background: linear-gradient(135deg, #101d50, #392078, #087eaa); color: white; }
.main .block-container { max-width: 650px; padding-top: 2rem; padding-bottom: 3rem; }
.hero { text-align: center; padding: 20px 5px; }
.hero h1 { font-size: 46px; font-weight: 900; background: linear-gradient(90deg,#55e6ff,#d69cff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { color: #d6e5ff; font-size: 15px; }
h1,h2,h3,p,label { color: white; }
[data-testid="stForm"] { background: rgba(255,255,255,0.09); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); }
.stTextInput input { border-radius: 10px; }
.stButton > button, .stFormSubmitButton > button { width:100%; min-height:45px; border:0; border-radius:12px; background:linear-gradient(90deg,#00c6ff,#8e54e9); color:white; font-weight:bold; font-size:15px; }
.stButton > button:hover, .stFormSubmitButton > button:hover { color:white; border:0; box-shadow:0 6px 20px rgba(0,198,255,0.4); }
.footer { text-align:center; color:#c5d8ff; font-size:12px; margin-top:35px; }
</style>
""", unsafe_allow_html=True)


def create_table():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        """)


def register_user(username, password):
    password_bytes = password.encode("utf-8")

    # bcrypt accepts a maximum input length of 72 bytes
    if len(password_bytes) > 72:
        return "long_password"

    # bcrypt automatically generates a random salt
    password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash.decode("utf-8"))
            )
        return "success"
    except sqlite3.IntegrityError:
        return "exists"


def login_user(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        row = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()

    if row is None:
        return False

    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        return False

    saved_hash = row[0].encode("utf-8")
    return bcrypt.checkpw(password_bytes, saved_hash)


if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

create_table()

st.markdown("""
<div class="hero">
    <h1>✦ NEXORA</h1>
    <p>Your Digital Identity, Protected.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.logged_in:
    st.success("Login Successful! 🎉")
    st.markdown(f"## Welcome, {st.session_state.username}!")
    st.markdown("### Your account is now active.")
    st.write("You have successfully accessed your NEXORA dashboard.")
    st.info("Your password is protected using bcrypt hashing.")

    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "login"
        st.rerun()

elif st.session_state.page == "login":
    st.markdown("## Welcome Back! 👋")
    st.write("Login to access your account.")
    show_password = st.checkbox("Show Password", key="login_show_password")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input(
            "Password",
            type="default" if show_password else "password",
            placeholder="Enter your password"
        )
        submit = st.form_submit_button("LOGIN")

    if submit:
        username = username.strip()
        if not username or not password:
            st.error("Please enter all fields.")
        elif login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.write("")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<p style="padding-top:8px;">Don\'t have an account?</p>', unsafe_allow_html=True)
    with col2:
        if st.button("Register Here →"):
            st.session_state.page = "register"
            st.rerun()

elif st.session_state.page == "register":
    st.markdown("## Create Your Account ✨")
    st.write("Join NEXORA and create your account.")
    show_password = st.checkbox("Show Password", key="register_show_password")

    with st.form("register_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        password = st.text_input(
            "Password",
            type="default" if show_password else "password",
            placeholder="Create a password"
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="default" if show_password else "password",
            placeholder="Enter password again"
        )
        submit = st.form_submit_button("CREATE ACCOUNT")

    if submit:
        username = username.strip()
        if not username or not password or not confirm_password:
            st.error("Please fill in all fields.")
        elif len(username) < 3:
            st.error("Username must have at least 3 characters.")
        elif len(password) < 8:
            st.error("Password must have at least 8 characters.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif len(password.encode("utf-8")) > 72:
            st.error("Password must not exceed 72 bytes when encoded.")
        else:
            result = register_user(username, password)
            if result == "success":
                st.success("Account created successfully! 🎉")
                st.session_state.page = "login"
                st.rerun()
            elif result == "exists":
                st.error("Username already exists.")

    st.write("")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<p style="padding-top:8px;">Already have an account?</p>', unsafe_allow_html=True)
    with col2:
        if st.button("Back to Login →"):
            st.session_state.page = "login"
            st.rerun()

st.markdown("""
<div class="footer">
    Protected with bcrypt password hashing
    <br><br>
    NEXORA | A Modern Authentication Experience
</div>
""", unsafe_allow_html=True)
