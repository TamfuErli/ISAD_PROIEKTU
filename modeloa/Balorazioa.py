import sqlite3
from .Connection import Connection

db = Connection()

class Balorazioa:
    def __init__(self, kodeBalorazioa, kodeFilm, kodePers, puntuazioa, iruzkina):
        self.kodeBalorazioa = kodeBalorazioa
        self.kodeFilm = kodeFilm
        self.kodePers = kodePers
        self.puntuazioa = puntuazioa
        self.iruzkina = iruzkina

    def getBalorazioa(kodeFilm, kodePers):
        return db.select("SELECT * FROM Puntuazioa WHERE kodeFilm = ? AND kodePers = ?", (kodeFilm, kodePers))

    def balorazioa_gorde(pelicula_id, usuario_id, puntuacion, comentario):
        """Guarda la valoración de un usuario en la base de datos."""
        db.insert("INSERT INTO Puntuazioa (kodeFilm, kodePers, puntuazioa, iruzkina) VALUES (?, ?, ?, ?)", (pelicula_id, usuario_id, puntuacion, comentario))

