import hmac

import bcrypt
import streamlit as st
from supabase import create_client

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="NEXORA | Digital Identity",
    page_icon="✨",
    layout="centered",
)

# -------------------- SUPABASE CONNECTION --------------------
@st.cache_resource
def get_supabase_client():
    """Create one server-side Supabase client for this Streamlit app."""
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )


try:
    supabase = get_supabase_client()
except Exception as exc:
    st.error(
        "Supabase connection is not configured. Check SUPABASE_URL "
        "and SUPABASE_KEY in Streamlit Secrets."
    )
    st.stop()


# -------------------- CUSTOM DESIGN --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101d50, #392078, #087eaa);
    color: white;
}
.main .block-container {
    max-width: 650px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    text-align: center;
    padding: 20px 5px;
}
.hero h1 {
    font-size: 46px;
    font-weight: 900;
    background: linear-gradient(90deg, #55e6ff, #d69cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: #d6e5ff;
    font-size: 15px;
}
h1, h2, h3, p, label {
    color: white;
}
[data-testid="stForm"] {
    background: rgba(255,255,255,0.09);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}
.stTextInput input {
    border-radius: 10px;
    color: #1e293b !important;
    background-color: #ffffff !important;
}
.stTextInput input::placeholder {
    color: #64748b !important;
    opacity: 1;
}
.stAlert, .stAlert p, .stAlert div {
    color: #1e293b !important;
}
.stButton > button, .stFormSubmitButton > button {
    width: 100%;
    min-height: 45px;
    border: 0;
    border-radius: 12px;
    background: linear-gradient(90deg, #00c6ff, #8e54e9);
    color: white;
    font-weight: bold;
    font-size: 15px;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    color: white;
    border: 0;
    box-shadow: 0 6px 20px rgba(0,198,255,0.4);
}
.footer {
    text-align: center;
    color: #c5d8ff;
    font-size: 12px;
    margin-top: 35px;
}
</style>
""", unsafe_allow_html=True)


# -------------------- USER FUNCTIONS --------------------
def register_user(username, password):
    password_bytes = password.encode("utf-8")

    # bcrypt supports a maximum password input length of 72 bytes.
    if len(password_bytes) > 72:
        return "long_password"

    password_hash = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    ).decode("utf-8")

    try:
        supabase.table("users").insert({
            "username": username,
            "password_hash": password_hash,
        }).execute()
        return "success"
    except Exception as exc:
        # PostgreSQL unique-constraint violation means username is taken.
        message = str(exc).lower()
        if "duplicate" in message or "unique" in message or "23505" in message:
            return "exists"
        st.error("Could not create the account. Please try again.")
        return "error"


def login_user(username, password):
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        return False

    try:
        response = (
            supabase.table("users")
            .select("password_hash")
            .eq("username", username)
            .limit(1)
            .execute()
        )
        if not response.data:
            return False

        saved_hash = response.data[0]["password_hash"].encode("utf-8")
        return bcrypt.checkpw(password_bytes, saved_hash)
    except Exception:
        st.error("Login could not be completed. Please try again.")
        return False


def admin_credentials_match(username, password):
    configured_username = st.secrets.get("ADMIN_USERNAME", "")
    configured_password = st.secrets.get("ADMIN_PASSWORD", "")

    if not configured_username or not configured_password:
        return False

    return (
        hmac.compare_digest(username, str(configured_username))
        and hmac.compare_digest(password, str(configured_password))
    )


# -------------------- SESSION STATE --------------------
defaults = {
    "page": "login",
    "logged_in": False,
    "username": "",
    "is_admin": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -------------------- HEADER --------------------
st.markdown("""
<div class="hero">
    <h1>✦ NEXORA</h1>
    <p>Your Digital Identity, Protected.</p>
</div>
""", unsafe_allow_html=True)


# -------------------- LOGGED-IN USER --------------------
if st.session_state.logged_in and not st.session_state.is_admin:
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


# -------------------- ADMIN DASHBOARD --------------------
elif st.session_state.logged_in and st.session_state.is_admin:
    st.success("Admin login successful.")
    st.markdown("## NEXORA Admin Dashboard")
    st.write("Registered user security records")

    try:
        response = (
            supabase.table("users")
            .select("username, password_hash, created_at")
            .order("created_at", desc=True)
            .execute()
        )

        records = []
        for user in response.data:
            stored_hash = user["password_hash"]
            records.append({
                "Username": user["username"],
                # bcrypt hash contains its salt in the first 29 characters.
                "Salt": stored_hash[:29],
                "Password Hash": stored_hash,
                "Created At": user.get("created_at", ""),
            })

        st.write(f"Total registered users: {len(records)}")
        if records:
            st.dataframe(records, use_container_width=True, hide_index=True)
        else:
            st.info("No registered users yet.")
    except Exception:
        st.error("Could not load user records.")

    st.warning(
        "Security note: These are password hashes, not original passwords. "
        "Keep this dashboard private."
    )

    if st.button("ADMIN LOGOUT"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.is_admin = False
        st.session_state.page = "login"
        st.rerun()


# -------------------- LOGIN PAGE --------------------
elif st.session_state.page == "login":
    st.markdown("## Welcome Back! 👋")
    st.write("Login to access your account.")
    show_password = st.checkbox("Show Password", key="login_show_password")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input(
            "Password",
            type="default" if show_password else "password",
            placeholder="Enter your password",
        )
        submit = st.form_submit_button("LOGIN")

    if submit:
        username = username.strip()
        if not username or not password:
            st.error("Please enter all fields.")
        elif login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.is_admin = False
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.write("")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            '<p style="padding-top:8px;">Don\'t have an account?</p>',
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("Register Here →"):
            st.session_state.page = "register"
            st.rerun()

    if st.button("Admin Login →"):
        st.session_state.page = "admin_login"
        st.rerun()


# -------------------- REGISTRATION PAGE --------------------
elif st.session_state.page == "register":
    st.markdown("## Create Your Account ✨")
    st.write("Join NEXORA and create your account.")
    show_password = st.checkbox("Show Password", key="register_show_password")

    with st.form("register_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        password = st.text_input(
            "Password",
            type="default" if show_password else "password",
            placeholder="Create a password",
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="default" if show_password else "password",
            placeholder="Enter password again",
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
        st.markdown(
            '<p style="padding-top:8px;">Already have an account?</p>',
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("Back to Login →"):
            st.session_state.page = "login"
            st.rerun()


# -------------------- ADMIN LOGIN PAGE --------------------
elif st.session_state.page == "admin_login":
    st.markdown("## Admin Login 🔐")
    st.write("Authorized administrator access only.")

    with st.form("admin_login_form"):
        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input("Admin Password", type="password")
        submit = st.form_submit_button("ADMIN LOGIN")

    if submit:
        if admin_credentials_match(admin_username.strip(), admin_password):
            st.session_state.logged_in = True
            st.session_state.is_admin = True
            st.session_state.username = admin_username.strip()
            st.rerun()
        else:
            st.error("Invalid admin credentials.")

    if st.button("Back to Login →"):
        st.session_state.page = "login"
        st.rerun()


# -------------------- FOOTER --------------------
st.markdown("""
<div class="footer">
    Protected with bcrypt password hashing
    <br><br>
    NEXORA | A Modern Authentication Experience
</div>
""", unsafe_allow_html=True)
