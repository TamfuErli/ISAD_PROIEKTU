from flask import render_template, Flask, session, url_for, redirect, request, make_response
from controller import erabiltzaile_kudeaketa
import sqlite3 

app = Flask(__name__, static_url_path='', template_folder='../templates/')
app.secret_key = 'super secret key'

@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit_login', methods=['POST'])
def submit_login():
    posta = request.form['posta']
    pasahitza = request.form['password']
    pashitza_egokia=erabiltzaile_kudeaketa.erabiltzailea_logeatu(posta, pasahitza)
    
    if pashitza_egokia:
        session['loged'] = pashitza_egokia
        session['sPosta'] = posta
        return redirect(url_for('home_loged'))
    else:
        return redirect(url_for('login'))

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

@app.route('/home_loged')
def home_loged():
    return render_template('home_loged.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
