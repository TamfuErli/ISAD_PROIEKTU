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
    
    def gehituAlokairuKop(posta):
        db.update("UPDATE Erabiltzailea SET alokairuKop = alokairuKop + 1 WHERE posta = ?", (posta,))
    
    def getErabiltzaileKodea(posta):
        return db.select("SELECT kodePers FROM Erabiltzailea WHERE posta = ?", (posta,))[0][0]

    def getPasahitza(posta):
        onartua = db.select("SELECT Onartua FROM Erabiltzailea WHERE posta = ?", (posta,))[0][0]
        if onartua:
            return db.select("SELECT pasahitza FROM Erabiltzailea WHERE posta = ?", (posta,))[0][0]
        else:
            return 0

    
    def getPosta(posta):
        return db.select("SELECT posta FROM Erabiltzailea WHERE posta = ?", (posta,))
    
    def bereAlokairua(self):
        # Implement the logic for proposamenak
        pass

    def proposamenak(self):
        # Implement the logic for proposamenak
        pass
     
    def adminDa(pPosta):
        adminDa=db.select("SELECT adminDa FROM Erabiltzailea WHERE posta = ?", (pPosta,))
        return adminDa[0][0]
    
    def setOnartua(pPosta):
        db.update("UPDATE Erabiltzailea SET Onartua = True WHERE posta = ?", (pPosta,))
        
    def getOnartua(pPosta):
        onartua=db.select("SELECT Onartua FROM Erabiltzailea WHERE posta = ?", (pPosta,))
        return onartua
    
