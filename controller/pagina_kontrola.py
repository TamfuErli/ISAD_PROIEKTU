from flask import render_template, Flask, session, url_for, redirect, request, make_response, request, jsonify
from controller import erabiltzaile_kudeaketa, film_kudeaketa
import sqlite3 
import requests
from modeloa import Erabiltzailea, Pelikula, PelikulaList, Connection

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
    onartuFilmak = film_kudeaketa.onartutakoFilmak()  # Fetch approved films from the database
    return render_template('home_loged.html', Pelikulak=onartuFilmak)

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

@app.route('/alokairu')
def alokairu():
    posta = request.form.get('posta')
    alokatutakoFilmak = film_kudeaketa.alokatutakoFilmak(posta)  # Fetch approved films from the database
    return render_template('alokairu.html', Pelikulak=alokatutakoFilmak)

@app.route('/submit_alokairu', methods=['POST'])
def submit_alokairu():
    kodeFilm = request.form.get('kodeFilm')
    erabiltzaile_kudeaketa.gehituAlokairua(2,kodeFilm)
    return redirect(url_for('alokairu'))

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

@app.route('/aldatu_datuak')
def aldatu_datuak():
    return render_template('datu_erabiltzaile_aldatu.html')
@app.route('/lortu_datuak')
def lortu_datuak():
    return jsonify(erabiltzaile_kudeaketa.listaErabiltzaileakOnartuta())


@app.route('/update_user', methods=['POST']) 
def update_user():
    posta = request.form.get('posta')
    izena = request.form.get('izena')
    erabiltzaile_kudeaketa.aldatuErabiltzailea(izena, posta, posta)
    return redirect(url_for('aldatu_datuak'))


@app.route('/logout')
def logout():
    session.clear()
    currentUser = None
    return redirect(url_for('home'))

@app.route('/propose', methods=['GET', 'POST'])
def propose():
    api_key = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNWUwYjAwZjFjZGRiZDMxZDQ0ODdkMWI1NGI3NzdlOSIsIm5iZiI6MTcyODY3OTU5Mi4wMzY4ODUsInN1YiI6IjY3MDdhYjM1ZDA2MTZjN2IxOWZiNTUwNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VM6BTKuWFqgaYTCqphxpAzRMPNZ1nmIBIVXOTF7tpC0"
    url_base = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=popularity.desc&page="
    search_url = "https://api.themoviedb.org/3/search/movie?query={query}&language=en-US&page={page}&include_adult=false"

    page = request.args.get('page', default=1, type=int)
    query = request.args.get('query', default="", type=str)

    if query:
        url = search_url.format(query=query, page=page)
    else:
        url = f"{url_base}{page}"

    response = requests.get(url, headers={"Authorization": api_key})

    movies = response.json()
    total_pages = movies.get('total_pages', 1)
    movies_results = movies.get('results', [])

    return render_template('propose.html', movies=movies_results, current_page=page, total_pages=total_pages, valid_page=True, query=query)


@app.route('/save_movie', methods=['POST'])
def save_movie():
    data = request.json
    kodeFilma = data['id']
    izena = data['title']
    poster_path = data['poster_path']
    deskripzioa = data['overview']
    balorazioa = data['vote_average']
    data = data['release_date']
    onartua = 0
    film_kudeaketa.gehituFilma(kodeFilma, izena, poster_path, deskripzioa, balorazioa, data, onartua)
    emaitza = film_kudeaketa.gehituEskaera(kodeFilma, Erabiltzailea.getErabiltzaileKodea(session['sPosta']))

    return {'success': emaitza}

@app.route('/get_saved_movies', methods=['GET'])
def get_saved_movies():
    saved_movies=Pelikula.getPelikulaKodeGuztiak()
    print(saved_movies)
    return jsonify([x[0] for x in saved_movies])
