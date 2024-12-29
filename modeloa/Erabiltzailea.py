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



    def getPasahitza(self):
        return db.select("SELECT pasahitza FROM Erabiltzailea WHERE kodePers = ?", (self.kodePers,))[0][0]
     
    def getErabiltzailea(self):
        return db.select("SELECT * FROM Erabiltzailea WHERE kodePers = ?", (self.kodePers,))[0]






    def gehituErabiltzailea(pIzena, pPasahitza, pPosta):
        existing_user = db.select("SELECT * FROM Erabiltzailea WHERE posta = ?", (pPosta,))
        if existing_user:
            raise ValueError("Posta horrekin dagoeneko existitzen da")
        else:         
            izena = pIzena
            pasahitza = pPasahitza
            posta = pPosta   
            line_count = db.select("SELECT COUNT(*) FROM Erabiltzailea")[0][0]
            kodePers = line_count + 1
            alokairuKop = 0
            adminDa = False
            db.insert("INSERT INTO Erabiltzailea (kodePers,izena, pasahitza, posta,alokairuKop,adminDa) VALUES (?,?,?,?,?,?)", (kodePers,izena, pasahitza,posta,alokairuKop,adminDa))
        
        

    def bereAlokairua(self):
        # Implement the logic for proposamenak
        pass

    def proposamenak(self):
        # Implement the logic for proposamenak
        pass
    

    def adminDa(self):
        # Implement the logic for adminDa
        pass