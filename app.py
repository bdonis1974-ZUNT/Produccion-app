from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "clave123"

orders = []

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
    return render_template("dash.html", orders=orders)


@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        return redirect("/")
    
    orders.append({
        "client": request.form["client"],
        "product": request.form["product"],
        "qty": request.form["qty"],
        "status": "Pendiente"
    })

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# IMPORTANTE: esto hace que funcione en Render
if __name__ != "__main__":
    pass
