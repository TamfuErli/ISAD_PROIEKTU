import sqlite3
from .Connection import Connection

db = Connection()

class Erabiltzailea:
    def __init__(self, kodePers, izena, pasahitza, posta, alokairuKop, adminDa, onartua):
        self.kodePers = kodePers
        self.izena = izena
        self.pasahitza = pasahitza
        self.posta = posta
        self.alokairuKop = alokairuKop
        self.adminDa = adminDa
        self.onartua = onartua

    def getErabiltzailea(posta):
        return db.select("SELECT * FROM Erabiltzailea WHERE posta = ?", (posta,))

    def bereAlokairua(self):
        # Implement the logic for proposamenak
        pass

    def proposamenak(self):
        # Implement the logic for proposamenak
        pass
    

    def adminDa(self):
        # Implement the logic for adminDa
        pass