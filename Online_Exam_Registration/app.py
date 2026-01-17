from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "examregsecret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sakshi2006",
    database="exam_reg"
)
cursor = db.cursor(dictionary=True)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        db.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

# ---------- Login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Email or Password"

    return render_template('login.html')

# ---------- Dashboard ----------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        exam = request.form.get('exam')
        subject = request.form.get('subject')

        cursor.execute(
            "INSERT INTO exam_registration (user_email, exam_name, subject) VALUES (%s, %s, %s)",
            (session['email'], exam, subject)
        )
        db.commit()
        return redirect(url_for('exam_details'))

    return render_template('dashboard.html')

# ---------- Exam Details ----------
@app.route('/exam_details')
def exam_details():
    if 'email' not in session:
        return redirect(url_for('login'))

    cursor.execute(
        "SELECT * FROM exam_registration WHERE user_email=%s",
        (session['email'],)
    )
    data = cursor.fetchall()

    return render_template('exam_details.html', exams=data)

# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------- Run App ----------
if __name__ == '__main__':
    app.run(debug=True)
