from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # kosong karena default Laragon
    database="hidroponik_db"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('dashboard'))
        else:
            error = "Username atau password salah!"
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/registrasi', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Cek apakah username sudah ada
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            message = "Username sudah terdaftar!"
        else:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            db.commit()
            message = "Registrasi berhasil! Silakan login."
            return redirect(url_for('login'))

    return render_template('registrasi.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
