from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sakshi2006",
    database="mini_ecom"
)
cursor = db.cursor(dictionary=True)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print("LOGIN BUTTON CLICKED")   

        e = request.form['email']
        p = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (e, p)
        )
        user = cursor.fetchone()

        if user:
            session['email'] = e
            return redirect('/products')

    return render_template('login.html')


@app.route('/products')
def products():
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    return render_template('products.html', products=data)

@app.route('/add/<int:id>')
def add(id):
    cursor.execute("SELECT * FROM products WHERE id=%s",(id,))
    p = cursor.fetchone()
    cursor.execute(
        "INSERT INTO cart(email,product,price) VALUES(%s,%s,%s)",
        (session['email'], p['name'], p['price'])
    )
    db.commit()
    return redirect('/cart')

@app.route('/cart')
def cart():
    cursor.execute(
        "SELECT * FROM cart WHERE email=%s",(session['email'],)
    )
    items = cursor.fetchall()
    total = sum(i['price'] for i in items)
    return render_template('cart.html', items=items, total=total)

@app.route('/order')
def order():
    cursor.execute(
        "SELECT SUM(price) total FROM cart WHERE email=%s",(session['email'],)
    )
    total = cursor.fetchone()['total']
    cursor.execute(
        "INSERT INTO orders(email,total) VALUES(%s,%s)",
        (session['email'], total)
    )
    cursor.execute("DELETE FROM cart WHERE email=%s",(session['email'],))
    db.commit()
    return redirect('/orders')

@app.route('/orders')
def orders():
    cursor.execute(
        "SELECT * FROM orders WHERE email=%s",(session['email'],)
    )
    data = cursor.fetchall()
    return render_template('orders.html', orders=data)

if __name__ == '__main__':
    app.run(debug=True)
