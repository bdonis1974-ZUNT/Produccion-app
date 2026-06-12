from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "clave123"

procesos = ["CORTE", "COSTURA", "INSPECCION", "EMPAQUE", "COMPLETO"]
data = []

@app.route("/", methods=["GET","POST"])
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
    return render_template("dash.html", data=data)

@app.route("/add", methods=["POST"])
def add():
    codigo = request.form["codigo"]
    if codigo:
        data.append({
            "codigo": codigo,
            "estado": "CORTE",
            "historial": ["CORTE"]
        })
    return redirect("/dashboard")

@app.route("/next/<int:i>")
def next_step(i):
    if i < len(data):
        item = data[i]
        actual = item["estado"]
        idx = procesos.index(actual)

        if idx < len(procesos) - 1:
            nuevo = procesos[idx + 1]
            item["estado"] = nuevo
            item["historial"].append(nuevo)

    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
