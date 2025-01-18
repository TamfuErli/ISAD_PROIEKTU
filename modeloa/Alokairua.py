import sqlite3
from .Connection import Connection

db = Connection()

class Alokairua:
    def __init__(self, data, kodeFilm, kodePers):
        self.data = data
        self.kodeFilm = kodeFilm
        self.kodePers = kodePers

    def getKodeFilm(self):
        return self.kodeFilm
    
    def getAlokairua(kodeFilm, kodePers):
        return db.select("SELECT * FROM Alokairua WHERE kodeFilm = ? AND kodePers = ?", (kodeFilm, kodePers,))