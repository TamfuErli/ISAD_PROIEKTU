import sqlite3
from .Connection import Connection

db = Connection()

class Pelikula:
    """def __init__(self, pizenburua, pzuzendaria, purtea, pmota):
        self.izenburua = pizenburua
        self.zuzendaria = pzuzendaria
        self.urtea = purtea
        self.mota = pmota"""

    def __init__(self, kodeFilma, izena, poster_path, deskripzioa, balorazioa, data, onartua):
        self.kodeFilma = kodeFilma
        self.izena = izena
        self.poster_path = poster_path
        self.deskripzioa = deskripzioa
        self.balorazioa = balorazioa
        self.data = data
        self.onartua = onartua

    def getPelikula(kodeFilm):
        return db.select("SELECT * FROM Filma WHERE kodeFilm = ?", (kodeFilm,))
    
    def getPelikulaKodea(izena): 
        return db.select("SELECT kodeFilm FROM Filma WHERE izena = ?", (izena,))
    
    def getEskaera(kodeFilm, kodePers):
        return db.select("SELECT * FROM Proposamenak WHERE kodeFilm = ? AND kodePers = ?", (kodeFilm, kodePers, ))
    
    def getPelikulaKodeGuztiak():
        return db.select("SELECT kodeFilm FROM Filma WHERE onartua = 1")
    
    def getPelikulaOnartua(kodeFilm):
        return db.select("SELECT onartua FROM Filma WHERE kodeFilm = ?", (kodeFilm,))
    def setOnartua(kodeFilm):
        db.update("UPDATE Filma SET onartua = 1 WHERE kodeFilm = ?", (kodeFilm,))