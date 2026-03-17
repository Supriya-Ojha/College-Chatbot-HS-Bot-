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

# ---------- ROUTES ---------- #

@app.route("/")
def login():
    return render_template("login.html")

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

# ---------- MAIN ---------- #

if __name__ == "__main__":
    init_db()   # ✅ VERY IMPORTANT
    app.run(host="0.0.0.0", port=10000)