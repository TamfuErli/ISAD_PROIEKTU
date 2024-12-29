from flask import render_template, Flask, url_for, redirect, request, make_response
from controller import erabiltzaile_kudeaketa
import sqlite3 

app = Flask(__name__, static_url_path='', template_folder='../templates/')
conexion=sqlite3.connect('datuBasea.db')
@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    izena = request.form['erabiltzailea']
    email = request.form['posta']
    pasahitza = request.form['password']
    erabiltzaile_kudeaketa.sortuErabiltzailea(izena,pasahitza, email)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
