import datetime
from flask import jsonify, session
from modeloa import Erabiltzailea, Alokairua, Pelikula, PelikulaList, Connection
from modeloa.Alokairua import Alokairua
import json
from datetime import datetime
db=Connection()

def erabiltzailea_logeatu(pPosta, pPasahitza):
    erabilttzailea = bilatuErabiltzailea(pPosta)
    pasahitza=Erabiltzailea.getPasahitza(pPosta)
    onartua=erabiltzaileaOnartua(pPosta)
        
    if erabilttzailea:
        if pasahitza==pPasahitza:
            if onartua==1:
                session['sPosta'] = pPosta
                logeatua= True
                session['adminDa'] = Erabiltzailea.adminDa(pPosta)
                session['sPosta'] = pPosta
            else:
                logeatua= False
                session["error"]=1
        else:
            logeatua= False 
            session["error"]=0      
    else:
        logeatua= False
        session["error"]=2  
    return logeatua

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
    existing_user=bilatuErabiltzailea(pPosta)
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

def gehituAlokairua(pPosta, kodeFilma):
    kodePP = Erabiltzailea.getErabiltzaileKodea(pPosta)
    existingAlokairua=Alokairua.getAlokairua(kodeFilma, kodePP)
    if not existingAlokairua:
        Erabiltzailea.gehituAlokairuKop(pPosta)
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.insert("INSERT INTO Alokairua (kodeFilm, kodePers, data)  VALUES (?, ?, ?)", (kodeFilma, kodePP, data))
        return {"success": True}
    else:
        return {"success": False, "message": "Ezin da pelikula bera bi aldiz alokatu"}
    
def bilatuErabiltzailea(posta):
    return Erabiltzailea.getErabiltzailea(posta)