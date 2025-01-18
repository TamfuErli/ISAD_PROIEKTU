from modeloa import Erabiltzailea, Pelikula
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
    else:
        return False
       