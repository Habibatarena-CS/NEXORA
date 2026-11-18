# ✨ NEXORA
### Your Digital Identity, Protected.

<p align="center">
  <strong>A Modern Authentication Web Application</strong><br>
  Built with Python, Streamlit, SQLite, and bcrypt
</p>

---

## 🌐 About NEXORA

**NEXORA** is a modern and user-friendly authentication web application developed using Python and Streamlit. It provides a simple way for users to create an account, log in securely, access a personal dashboard, and log out.

The project focuses on password security by using the **bcrypt hashing algorithm**. Instead of saving passwords as plain text, NEXORA hashes each password with a randomly generated salt before storing it in the SQLite database.

Its interface features a blue, purple, and cyan gradient design to create a clean and welcoming user experience.

## ✨ Key Features

- **User Registration** – Create a new account with a username and password.
- **User Login** – Sign in using registered account credentials.
- **bcrypt Password Hashing** – Protect passwords by storing their bcrypt hashes instead of plain-text passwords.
- **Automatic Random Salt** – Generate a unique random salt through bcrypt during password hashing.
- **Password Confirmation** – Confirm the password during registration.
- **Show/Hide Password** – Choose whether to display or hide password input.
- **Input Validation** – Check required fields, minimum username length, minimum password length, and matching passwords.
- **Duplicate Username Prevention** – Prevent registration with a username that already exists.
- **SQLite Database** – Store usernames and password hashes.
- **Personalized Dashboard** – Display a welcome message after successful login.
- **Logout Functionality** – End the active session and return to the login page.
- **Modern Gradient Interface** – Use a blue, purple, and cyan visual theme.

## 🔐 How NEXORA Works

NEXORA follows a straightforward registration and login process.

### 1. Registration Process

1. The user opens the registration page.
2. The user enters a username, password, and password confirmation.
3. The application validates the entered information.
4. bcrypt generates a random salt and creates a hash of the password.
5. The username and password hash are stored in the SQLite database.

### 2. Login Process

1. The user enters their registered username and password.
2. The application searches for the username in the database.
3. bcrypt checks the entered password against the stored password hash.
4. If the password is correct, the user is logged in and taken to the dashboard.
5. If the credentials are incorrect, an error message is displayed.

### 3. Logout Process

When the user clicks the **Logout** button, the active login session is cleared and the application returns to the login page.

## 🛡️ Password Security with bcrypt

NEXORA uses **bcrypt** for password hashing.

- `bcrypt.gensalt()` generates a random salt.
- `bcrypt.hashpw()` hashes the password using the generated salt.
- The resulting hash, which includes the salt information, is stored in the database.
- `bcrypt.checkpw()` verifies a password during login.

Passwords are not stored as plain text. The application stores the bcrypt password hash in SQLite.

## 🧰 Technologies and Libraries

| Technology / Library | Purpose |
|---|---|
| **Python** | Main programming language used to develop the application |
| **Streamlit** | Creates the web interface and handles user interaction |
| **SQLite3** | Creates and manages the user database |
| **bcrypt** | Generates password hashes and verifies passwords |
| **HTML** | Structures the custom interface elements |
| **CSS** | Styles the application with colors, gradients, spacing, and buttons |

## 📁 Project Structure

```text
NEXORA/
│
├── app.py
├── requirements.txt
└── README.md
```

| File | Description |
|---|---|
| `app.py` | Main application code, including registration, login, password hashing, database operations, and dashboard |
| `requirements.txt` | Lists the Python libraries required to run the application |
| `README.md` | Project overview, features, technologies, and working process |

The `users.db` SQLite database is created automatically when the application runs.

## ⚙️ Installation and Setup

### Requirements

- Python installed on the system
- Internet connection for installing the required libraries

### Install the Libraries

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

The NEXORA application opens in a web browser.

## 🎯 Project Objective

The objective of NEXORA is to develop a simple and interactive authentication system while applying important concepts of password security and web application development.

Through this project, I have implemented user registration, login authentication, bcrypt password hashing, automatic salt generation, database connectivity, input validation, and session-based navigation in a Streamlit application.

---

<p align="center">
  <strong>✦ NEXORA</strong><br>
  <em>Your Digital Identity, Protected.</em>
</p>
