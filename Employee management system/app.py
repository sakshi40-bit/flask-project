from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "mini_commerce_secret"  

# -------- DATABASE CONNECTION --------
try:
    db = mysql.connector.connect(
        host="localhost",       
        user="root",            
        password="sakshi2006",  
        database="mini_commerce"  
    )
    cursor = db.cursor(dictionary=True)
except mysql.connector.Error as err:
    print("DB Connection Error:", err)
    exit(1)

# -------- LOGIN ROUTE --------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )
        admin = cursor.fetchone()

        if admin:
            session['admin'] = username
            return redirect('/add_product')
        else:
            return

    return render_template("login.html")

# -------- ADD PRODUCT --------
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'admin' not in session:
        return redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']

        cursor.execute(
            "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
            (name, price, stock)
        )
        db.commit()
        return redirect('/view_products')

    return render_template("add_product.html")

# -------- VIEW PRODUCTS --------
@app.route('/view_products')
def view_products():
    if 'admin' not in session:
        return redirect('/')

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template("view_product.html", products=products)

# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# -------- RUN SERVER --------
if __name__ == '__main__':
    app.run(debug=True)
