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
    onartua=erabiltzaile_kudeaketa.erabiltzaileaOnartua("")
    if pashitza_egokia:
        if onartua==0:
            return redirect(url_for('login', error="Erabiltzailea ez dago onartuta"))
        else:
            session['adminDa'] = erabiltzaile_kudeaketa.Erabiltzailea.adminDa(posta)
            session['loged'] = pashitza_egokia
            session['sPosta'] = posta
            if session['adminDa']:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home_loged'))
    else:
        return redirect(url_for('login', error="Pasahitza okerra"))

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

@app.route('/datuak_aldatu')
def datuak_aldatu():
    return render_template('datuak_aldatu.html')

@app.route('/submit_datuak', methods=['POST'])
def submit_datuak():
    izena = request.form['izenBerria']
    email = request.form['emailBerria']
    sPosta = session['sPosta']
    erabiltzaile_kudeaketa.aldatuErabiltzailea(izena, email, sPosta)
    return redirect(url_for('home_loged'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/eskaerak')
def eskaerak():
    Erabiltzaileak=erabiltzaile_kudeaketa.listaErabiltzaileak()
    return render_template('eskaera_lista.html', Erabiltzaileak=Erabiltzaileak)

@app.route('/submit_onarpen', methods=['POST'])
def submit_onarpen():
    posta = request.form.get('posta')
    erabiltzaile_kudeaketa.erabiltzaileaOnartu(posta)
    return redirect(url_for('eskaerak'))

@app.route("/ezabatu_erabiltzailea")
def ezabatu_erabiltzailea():
    Erabiltzaileak=erabiltzaile_kudeaketa.listaErabiltzaileakOnartuta()
    return render_template('ezabatu_erabiltzailea.html', Erabiltzaileak=Erabiltzaileak)

@app.route('/submit_ezabatu', methods=['POST'])
def submit_ezabatu():
    posta = request.form.get('posta')
    erabiltzaile_kudeaketa.erabiltzaileaEzabatu(posta)
    return redirect(url_for('ezabatu_erabiltzailea'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
