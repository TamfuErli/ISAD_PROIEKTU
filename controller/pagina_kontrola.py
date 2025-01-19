from flask import flash, render_template, Flask, session, url_for, redirect, request, make_response, request, jsonify
from controller import erabiltzaile_kudeaketa, film_kudeaketa, puntuazio_kudeaketa
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
    erabilttzailea = erabiltzaile_kudeaketa.bilatuErabiltzailea(posta)
    if erabilttzailea:
        pashitza_egokia=erabiltzaile_kudeaketa.erabiltzailea_logeatu(posta, pasahitza)
        onartua=erabiltzaile_kudeaketa.erabiltzaileaOnartua(posta)
        erabilttzailea = erabiltzaile_kudeaketa.bilatuErabiltzailea(posta)
        if onartua==1:
            if pashitza_egokia:
                session['adminDa'] = erabiltzaile_kudeaketa.Erabiltzailea.adminDa(posta)
                session['loged'] = pashitza_egokia
                session['sPosta'] = posta
                if session['adminDa']:
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('home_loged'))
            else:
                session["error"]=0
                return redirect(url_for('error'))     
        else:
            session["error"]=1
            return redirect(url_for('error'))
    else:
        session["error"]=2
        return redirect(url_for('error'))

@app.route('/error')
def error():
    return render_template('error.html', error=session["error"])

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    izena = request.form['erabiltzailea']
    posta = request.form['posta']
    pasahitza = request.form['password']
    erabiltzailea=erabiltzaile_kudeaketa.bilatuErabiltzailea(posta)
    if erabiltzailea:
        session["error"]=3
        return redirect(url_for('error'))
    else:
        erabiltzaile_kudeaketa.sortuErabiltzailea(izena,pasahitza, posta)
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
    pPosta = session.get('sPosta')
    pertsonarenAlokairuak= film_kudeaketa.alokatutakoFilmak(pPosta) 
    alokatutakoFilmak = []
    for alokairu in pertsonarenAlokairuak:
        kodea = alokairu.getKodeFilm()
        film = film_kudeaketa.billatuPelikula(kodea)
        if film:
            alokatutakoFilmak.extend(film)
    return render_template('alokairu.html', Filmak=alokatutakoFilmak)

@app.route('/submit_alokairu', methods=['POST'])
def submit_alokairu():
    pPosta = session.get('sPosta')
    kodeFilma = request.form.get('kodeFilma')
    result = erabiltzaile_kudeaketa.gehituAlokairua(pPosta,kodeFilma)
    if not result['success']:
        flash(result['message'])
    return redirect(url_for('home_loged'))

@app.route('/eskaerak')
def eskaerak():
    return render_template('eskaera_lista.html')
@app.route('/lortu_erabiltzaileEZOnartu')
def lortu_erabiltzaileEZOnartu():
    return jsonify(erabiltzaile_kudeaketa.listaErabiltzaileakEzOnartuta())

@app.route('/submit_onarpen', methods=['POST'])
def submit_onarpen():
    posta = request.form.get('posta')
    erabiltzaile_kudeaketa.erabiltzaileaOnartu(posta)
    return redirect(url_for('eskaerak'))


@app.route("/ezabatu_erabiltzailea")
def ezabatu_erabiltzailea():
    return render_template('ezabatu_erabiltzailea.html')
@app.route('/lortu_erabiltzaileOnartua')
def lortu_erabiltzaileOnartua():
    return jsonify(erabiltzaile_kudeaketa.listaErabiltzaileakOnartuta())


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
    ePosta = request.form.get('original_posta')
    eIzena = request.form.get('original_izena')
    if not posta:
        posta = ePosta
    if not izena:
        izena = eIzena
    if erabiltzaile_kudeaketa.bilatuErabiltzailea(posta):
        session["error"]=4
        return redirect(url_for('error'))
    else:
        erabiltzaile_kudeaketa.aldatuErabiltzailea(izena, posta, ePosta)
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

@app.route('/filma_baloratu')
def filma_baloratu():
    pPosta = session.get('sPosta')
    kodeFilma = request.form.get('kodeFilma')
    return render_template('filma_baloratu.html')

@app.route('/eskaera_film')
def eskaera_film():
    return render_template('filma_eskaerak.html')

@app.route('/film_lista')
def film_lista():
    return jsonify(film_kudeaketa.ezOnartutakoFilmak())

@app.route('/filma_Onartu', methods=['POST'])
def filma_Onartu():
    kodeFilm = request.form.get('kodeFilm')
    film_kudeaketa.filmaOnartu(kodeFilm)
    return redirect(url_for('eskaera_film'))

@app.route('/filma_baloratu', methods=['POST'])
def filma_baloratu():
    session['kodeFilma'] = request.form.get('kodeFilma')
    return render_template('filma_baloratu.html')
@app.route('/get_balorazioak')
def get_balorazioak():
    balorazioak = puntuazio_kudeaketa.get_balorazioGuztiak(session['kodeFilma'])
    return jsonify(balorazioak)
