from flask import Flask, render_template, request, redirect, flash, session
import sqlite3
from chatbot import chatbot_response

app = Flask(__name__)
app.secret_key = "secret"

# ---------- DATABASE ---------- #

def get_db_connection():
    conn = sqlite3.connect('college.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS enquiries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT
    )
    ''')

    conn.commit()
    conn.close()

# ---------- USER ROUTES ---------- #

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = get_db_connection()

    try:
        conn.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )
        conn.commit()

    except Exception:
        conn.close()
        flash("User already exists!")
        return redirect("/register")

    conn.close()
    flash("Registration Successful! Please login.")
    return redirect("/")


@app.route("/login_validation", methods=["POST"])
def login_validation():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    ).fetchone()
    conn.close()

    if user:
        session["user"] = email
        return redirect("/index")
    else:
        flash("Invalid Email or Password")
        return redirect("/")


@app.route("/index")
def index():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    if "user" not in session:
        return "Please login first"

    msg = request.args.get("msg")

    if msg:
        conn = get_db_connection()
        conn.execute("INSERT INTO enquiries(message) VALUES(?)", (msg,))
        conn.commit()
        conn.close()

        return chatbot_response(msg)

    return "No message received"


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ---------- FORGOT PASSWORD ---------- #

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")


@app.route("/forgot_password", methods=["POST"])
def forgot_password():
    email = request.form.get("email")

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()
    conn.close()

    if user:
        flash(f"Your password is: {user['password']}")
    else:
        flash("Email not found")

    return redirect("/")

# ---------- ADMIN ROUTES ---------- #

@app.route("/admin")
def admin():
    return render_template("admin_login.html")


@app.route("/admin_login_validation", methods=["POST"])
def admin_login_validation():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin123":
        session["admin"] = username
        return redirect("/admin_dashboard")
    else:
        flash("Invalid Admin Credentials")
        return redirect("/admin")


@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin")

    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    enquiries = conn.execute("SELECT * FROM enquiries").fetchall()
    conn.close()

    return render_template("admin.html", users=users, enquiries=enquiries)


@app.route("/admin_logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/admin")

# ---------- MAIN ---------- #

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
