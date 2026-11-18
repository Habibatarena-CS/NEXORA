# ✨ NEXORA
### Your Digital Identity, Protected.

NEXORA is a cloud-based user authentication system built with **Python** and **Streamlit**. It provides secure user registration and login, bcrypt password protection, and persistent user records through a **Supabase PostgreSQL cloud database**.
## 🌐 Live Demo

**Try NEXORA:** ## 🌐 Live Demo

[Open NEXORA — Live Application](https://nexora-secure.streamlit.app/)

Explore the NEXORA interface, user registration, secure login, and authentication features.

## 🚀 Features

- **User Registration:** Create an account with a unique username and password. Duplicate usernames are not allowed.
- **Secure User Login:** Authenticate users by checking their entered password against the stored bcrypt hash.
- **Password Visibility:** Show or hide passwords during registration and login.
- **Logout:** End the current user or administrator session.
- **Admin Authentication:** Separate administrator login using credentials stored in Streamlit Secrets.
- **Admin Dashboard:** View registered users' usernames, bcrypt salts, and password hashes in a structured table.
- **Persistent Cloud Storage:** Keep user records in Supabase even after the application restarts.
- **Modern Interface:** Clean Streamlit interface with custom CSS styling.
- **Cloud Deployment:** Run the application online through Streamlit Community Cloud.

## 🔐 Password Security with bcrypt

NEXORA uses the **bcrypt** library to protect user passwords:

- Generates a unique salt for each password.
- Hashes passwords before saving them.
- Never stores original passwords in plain text.
- Uses `bcrypt.checkpw()` to verify login attempts.

**Note:** bcrypt is a one-way password-hashing algorithm. The original password is not displayed or stored.

## ☁️ Supabase Cloud Database

NEXORA uses **Supabase PostgreSQL** to store user records persistently in the cloud.

The `users` table contains:

| Column | Description |
|---|---|
| `id` | Unique user ID |
| `username` | Unique registered username |
| `password_hash` | bcrypt password hash |
| `salt` | Generated bcrypt salt |
| `created_at` | Account creation timestamp |

The Admin Dashboard displays the username, salt, and password hash. The `created_at` field remains in the database but is not displayed on the dashboard.

## 📊 How It Works

**Registration**
1. User enters a username and password.
2. The app checks that the username is not already registered.
3. bcrypt generates a salt and password hash.
4. The username, salt, and hash are saved in Supabase.

**Login**
1. User enters their credentials.
2. The app retrieves the stored password hash from Supabase.
3. bcrypt verifies the entered password using `bcrypt.checkpw()`.
4. Access is granted only if the password matches.

**Admin Dashboard**
1. The administrator signs in using separate admin credentials.
2. The app verifies those credentials using Streamlit Secrets.
3. The dashboard retrieves and displays registered users' security records from Supabase.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| bcrypt | Password hashing and verification |
| Supabase PostgreSQL | Cloud database |
| Git & GitHub | Version control and source code hosting |
| Streamlit Community Cloud | Application deployment |

## ⚙️ Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/Habibatarena-CS/NEXORA.git
cd NEXORA
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure Streamlit Secrets**

Create `.streamlit/secrets.toml` and add your own values:

```toml
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY = "YOUR_SUPABASE_SECRET_KEY"
ADMIN_USERNAME = "YOUR_ADMIN_USERNAME"
ADMIN_PASSWORD = "YOUR_ADMIN_PASSWORD"
```

**4. Start the application**

```bash
streamlit run app.py
```

## 📦 Requirements

```text
streamlit
bcrypt
supabase
```

## 🔒 Security Reminder

Keep your Supabase Secret key and administrator password private. Store them in Streamlit Secrets and never commit real credentials to GitHub.

The Admin Dashboard exposes password hashes and salts for this project's educational demonstration. In a production application, access to these records should be tightly restricted.

## 🎯 Project Objective

NEXORA demonstrates secure user authentication, bcrypt password hashing, salt generation, cloud database integration, and administrator access management in a deployed web application.

---

<p align="center">

**NEXORA — Your Digital Identity, Protected.** ✨

</p>
