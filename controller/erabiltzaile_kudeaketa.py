import datetime
from flask import jsonify, session
from modeloa import Erabiltzailea, Alokairua, Pelikula, PelikulaList, Connection
import json
db=Connection()

def erabiltzailea_logeatu(pPosta, pPasahitza):
    pasahitza=Erabiltzailea.getPasahitza(pPosta)
    if pasahitza==pPasahitza:
        return True
    else:
        return False

def filmAlokairuaErakutsi():
    posta = session.get('sPosta')
    if not posta:
        raise ValueError("Erabiltzailea ez dago saio hasita")

    erabiltzailea = db.select("SELECT kodePers FROM Erabiltzailea WHERE posta = ?", (posta,))
    if not erabiltzailea:
        raise ValueError("Erabiltzailea ez da existitzen")

    kodePers = erabiltzailea[0][0]
    pelikulak = db.select("SELECT Pelikula.* FROM Alokairua JOIN Pelikula ON Alokairua.pelikulaId = Pelikula.id WHERE Alokairua.erabiltzaileaId = ?", (kodePers,))
    return [Pelikula(*pelikula) for pelikula in pelikulak]

def sortuErabiltzailea(pIzena, pPasahitza, pPosta):
    existing_user=Erabiltzailea.getErabiltzailea(pPosta)
    if existing_user:
        raise ValueError("Posta horrekin dagoeneko existitzen da")
    else:
                 
        izena = pIzena
        pasahitza = pPasahitza
        posta = pPosta 
          
        line_count = db.select("SELECT COUNT(*) FROM Erabiltzailea")[0][0]
        kodePers = line_count+1
        alokairuKop = 0
        adminDa = False
        Onartua = False
        db.insert("INSERT INTO Erabiltzailea (kodePers,izena, pasahitza, posta,alokairuKop,adminDa,Onartua) VALUES (?,?,?,?,?,?,?)", (kodePers,izena, pasahitza,posta,alokairuKop,adminDa,Onartua))
        
def erabiltzaileaEzabatu(pPosta):
    db.delete("DELETE FROM Erabiltzailea WHERE posta = ?", (pPosta,))
    
def listaErabiltzaileakEzOnartuta():
    erabiltzaileak = db.select("SELECT * FROM Erabiltzailea WHERE Onartua = 0") 
    erabiltzaile_json = [
        {
            "kodePers": erabiltzailea[0],
            "izena": erabiltzailea[1],
            "posta": erabiltzailea[3],
            "alokairuKop": erabiltzailea[4],
            "adminDa": erabiltzailea[5],
            "Onartua": erabiltzailea[6]
        }
        for erabiltzailea in erabiltzaileak
    ]
    return erabiltzaile_json

def listaErabiltzaileakOnartuta():
    erabiltzaileak = db.select("SELECT * FROM Erabiltzailea WHERE Onartua = 1") 
    erabiltzaile_json = [
        {
            "kodePers": erabiltzailea[0],
            "izena": erabiltzailea[1],
            "posta": erabiltzailea[3],
            "alokairuKop": erabiltzailea[4],
            "adminDa": erabiltzailea[5],
            "Onartua": erabiltzailea[6]
        }
        for erabiltzailea in erabiltzaileak
    ]
    return erabiltzaile_json

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

def gehituAlokairua(kodeFilm, kodePers):
    existingAlokairua=Alokairua.getAlokairua(kodeFilm, kodePers)
    if not existingAlokairua:
        kodeFilm = kodeFilm
        kodePers = kodePers
        Erabiltzailea.gehituAlokairuKop()
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.insert("INSERT INTO Alokairua (kodeFilm, kodePers, data)  VALUES (?, ?, ?)", (kodeFilm, kodePers, data))
        return True
    else:
        return False