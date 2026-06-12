
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

def db():
    conn = sqlite3.connect('db.db')
    conn.row_factory = sqlite3.Row
    return conn

def init():
    con = db()
    con.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, user TEXT, pass TEXT)')
    con.execute('CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY, client TEXT, product TEXT, qty INT, status TEXT)')
    if not con.execute('SELECT * FROM users').fetchone():
        con.execute("INSERT INTO users(user, pass) VALUES('admin','1234')")
    con.commit()

@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=request.form['user']
        p=request.form['pass']
        user=db().execute('SELECT * FROM users WHERE user=? AND pass=?',(u,p)).fetchone()
        if user:
            session['user']=u
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dash():
    if 'user' not in session: return redirect('/')
    d=db()
    orders=d.execute('SELECT * FROM orders').fetchall()
    return render_template('dash.html',orders=orders)

@app.route('/add', methods=['POST'])
def add():
    d=db()
    d.execute('INSERT INTO orders(client,product,qty,status) VALUES(?,?,?,?)',
              (request.form['client'],request.form['product'],request.form['qty'],'Pendiente'))
    d.commit()
    return redirect('/dashboard')

if __name__=='__main__':
    init()
