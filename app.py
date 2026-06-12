from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave123"

procesos = ["CORTE", "COSTURA", "INSPECCION", "EMPAQUE", "COMPLETO"]

# Crear base de datos
def init_db():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS produccion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        estado TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["user"] == "admin" and request.form["pass"] == "1234":
            session["user"] = "admin"
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM produccion")
    data = c.fetchall()
    conn.close()

    return render_template("dash.html", data=data, procesos=procesos)

@app.route("/add", methods=["POST"])
def add():
    codigo = request.form["codigo"]

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("INSERT INTO produccion (codigo, estado) VALUES (?, ?)", (codigo, "CORTE"))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/next/<int:id>")
def next_step(id):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    c.execute("SELECT estado FROM produccion WHERE id=?", (id,))
    estado = c.fetchone()[0]

    idx = procesos.index(estado)

    if idx < len(procesos) - 1:
        nuevo = procesos[idx + 1]
        c.execute("UPDATE produccion SET estado=? WHERE id=?", (nuevo, id))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
