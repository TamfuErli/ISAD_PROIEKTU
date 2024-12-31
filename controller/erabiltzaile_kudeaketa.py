from flask import session
from modeloa import Erabiltzailea, Pelikula, Connection
db=Connection()

def erabiltzailea_logeatu(pPosta, pPasahitza):
    pasahitza=Erabiltzailea.getPasahitza(pPosta)
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
        
def erabiltzaileaEzabatu(pPosta):
    db.delete("DELETE FROM Erabiltzailea WHERE posta = ?", (pPosta,))
    
def listaErabiltzaileak():
    erabiltzaileak = db.select("SELECT * FROM Erabiltzailea WHERE Onartua = 0") 
    return [Erabiltzailea(*erabiltzailea) for erabiltzailea in erabiltzaileak]

def listaErabiltzaileakOnartuta():
    erabiltzaileak = db.select("SELECT * FROM Erabiltzailea WHERE Onartua = 1") 
    return [Erabiltzailea(*erabiltzailea) for erabiltzailea in erabiltzaileak]

def erabiltzaileaOnartu(pPosta):
    posta = pPosta
    Erabiltzailea.setOnartua(posta)

def erabiltzaileaOnartua(pPosta):
    return Erabiltzailea.getOnartua(pPosta)

def aldatuErabiltzailea(pIzena,pPosta,sPosta):
    izena = pIzena
    posta = pPosta
    db.update("UPDATE Erabiltzailea SET izena = ?, posta= ? WHERE posta = ?", (izena,posta,sPosta))
    session['sPosta'] = posta