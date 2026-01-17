from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "banksecret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sakshi2006",
    database="banking"
)
cursor = db.cursor(dictionary=True)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s",(email,password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
                       (name,email,password))
        db.commit()
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT * FROM users WHERE id=%s",(session['user_id'],))
    user = cursor.fetchone()
    cursor.execute("SELECT * FROM transactions WHERE user_id=%s",(session['user_id'],))
    trans = cursor.fetchall()
    return render_template('dashboard.html', user=user, trans=trans)

@app.route('/deposit', methods=['GET','POST'])
def deposit():
    if request.method == 'POST':
        amount = int(request.form['amount'])
        cursor.execute("UPDATE users SET balance=balance+%s WHERE id=%s",
                       (amount,session['user_id']))
        cursor.execute("INSERT INTO transactions (user_id,type,amount) VALUES (%s,'Deposit',%s)",
                       (session['user_id'],amount))
        db.commit()
        return redirect('/dashboard')
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET','POST'])
def withdraw():
    if request.method == 'POST':
        amount = int(request.form['amount'])
        cursor.execute("UPDATE users SET balance=balance-%s WHERE id=%s",
                       (amount,session['user_id']))
        cursor.execute("INSERT INTO transactions (user_id,type,amount) VALUES (%s,'Withdraw',%s)",
                       (session['user_id'],amount))
        db.commit()
        return redirect('/dashboard')
    return render_template('withdraw.html')

app.run(debug=True)
