from flask import render_template, Flask, url_for, redirect, request, make_response
from modeloa import Erabiltzailea
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
    password = request.form.get('password')
    izena = request.form.get('erabiltzailea')
    posta = request.form.get('posta')
    Erabiltzailea.gehituErabiltzailea(izena,password,posta)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
