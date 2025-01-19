from modeloa import Erabiltzailea, Pelikula, Alokairua
import sqlite3
from modeloa.Connection import Connection

db = Connection()

def gehituFilma(kodeFilma, izena, poster_path, deskripzioa, balorazioa, data, onartua):
    existing_film=Pelikula.getPelikula(kodeFilma)
    if not existing_film:
        kodeFilma = kodeFilma
        izena = izena
        poster_path = poster_path
        deskripzioa = deskripzioa
        balorazioa = balorazioa
        data = data
        onartua = onartua
        db.insert('''
        INSERT INTO Filma (kodeFilm, izena, poster_path, deskripzioa, balorazioa, data, onartua)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (kodeFilma, izena, poster_path, deskripzioa, balorazioa, data, onartua))
        
def gehituEskaera(kodeFilm, kodePers):
    existing_eskaera=Pelikula.getEskaera(kodeFilm, kodePers)
    onartua=Pelikula.getPelikulaOnartua(kodeFilm)[0][0]
    if onartua == 0:
        if not existing_eskaera:
            kodeFilm = kodeFilm
            kodePers = kodePers
            db.insert('''
            INSERT INTO Proposamenak (kodeFilm, kodePers)
            VALUES (?, ?)
        ''', (kodeFilm, kodePers))
            return True
        return False
    else:
        return False

def onartutakoFilmak():
    onartutakoPelikulak = db.select("SELECT * FROM Filma WHERE onartua = 1")
    return [Pelikula(*onartutakoPelikula) for onartutakoPelikula in onartutakoPelikulak]

def alokatutakoFilmak(pPosta):
    pKodePers = Erabiltzailea.getErabiltzaileKodea(pPosta)
    alokatutakoPelikulak = db.select("SELECT * FROM Alokairua WHERE kodePers = ?", (pKodePers,))
    return [Alokairua.Alokairua(*alokatutakoPelikula) for alokatutakoPelikula in alokatutakoPelikulak]

def billatuPelikula(kodeFilm):
    pPelikula = Pelikula.getPelikula(kodeFilm)
    return pPelikula

def ezOnartutakoFilmak():
    ezOnartutakoPelikulak = db.select("SELECT * FROM Filma WHERE onartua = 0")
    film_json = [
        {
            "kodeFilm": ezOnartutakoPelikula[0],
            "izena": ezOnartutakoPelikula[1],
            "poster_path": ezOnartutakoPelikula[2],
            "deskripzioa": ezOnartutakoPelikula[3],
            "balorazioa": ezOnartutakoPelikula[4],
            "data": ezOnartutakoPelikula[5],
            "onartua": ezOnartutakoPelikula[6]
        }
        for ezOnartutakoPelikula in ezOnartutakoPelikulak
    ]
    return film_json
def filmaOnartu(pkodeFilm):
    kodeFilm = pkodeFilm
    Pelikula.setOnartua(kodeFilm)