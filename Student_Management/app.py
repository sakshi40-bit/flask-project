from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "student_secret_key"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sakshi2006",   
    database="student_mgmt"
)

cursor = db.cursor(dictionary=True)

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
            return redirect('/add_student')
        else:
            return 

    return render_template('login.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'admin' not in session:
        return redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        year = request.form['year']

        cursor.execute(
            "INSERT INTO students (name, course, year) VALUES (%s, %s, %s)",
            (name, course, year)
        )
        db.commit()

        return redirect('/view_student')

    return render_template('add_student.html')

@app.route('/view_student')
def view_student():
    if 'admin' not in session:
        return redirect('/')

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    return render_template('view_student.html', students=students)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
