from modeloa import Erabiltzailea, Pelikula, Connection
db=Connection()

class Filmoteka:
    def __init__(self):
        self.erabiltzaileak = []
        self.pelikulak = []
        
def erabiltzailea_logeatu(pPosta, pPasahitza):
    pasahitza=Erabiltzailea.getPasahitza(pPosta)[0][0]
    if pasahitza==pPasahitza:
        return True
    else:
        return False


def sortuErabiltzailea(pIzena, pPasahitza, pPosta):
    existing_user=Erabiltzailea.getErabiltzailea(pPosta)
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
        Onartua = False
        db.insert("INSERT INTO Erabiltzailea (kodePers,izena, pasahitza, posta,alokairuKop,adminDa,Onartua) VALUES (?,?,?,?,?,?,?)", (kodePers,izena, pasahitza,posta,alokairuKop,adminDa,Onartua))