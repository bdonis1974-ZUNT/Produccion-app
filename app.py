from flask import Flask, render_template, request, redirect, session

app = Flask(_name_)
app.secret_key = 'secret123'

# datos en memoria
orders = []

@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = request.form['user']
        password = request.form['pass']

        if user == 'admin' and password == '1234':
            session['user'] = user
            return redirect('/dashboard')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dash.html', orders=orders)

@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session:
        return redirect('/')

    client = request.form['client']
    product = request.form['product']
    qty = request.form['qty']

    orders.append({
        'client': client,
        'product': product,
        'qty': qty,
        'status': 'Pendiente'
    })

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
