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
