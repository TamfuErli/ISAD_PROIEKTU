from flask import Blueprint, request, jsonify, session, abort # type: ignore
from modeloa import Pelikula, Erabiltzailea
from modeloa import Connection
from modeloa.Balorazioa import Balorazioa

db = Connection()

def get_balorazioGuztiak(kodeFilma):
    filma = kodeFilma
    balorazioak = db.select("SELECT * FROM Puntuazioa WHERE kodeFilm = ?", (filma,))
    baloratuGabeJSON = [
        {
            "puntuazioa": balorazioa[2],
            "iruzkina": balorazioa[3]
        }
        for balorazioa in balorazioak
    ]
    return baloratuGabeJSON
    
def gehituBalorazioa(kodeFilma, kodeErabiltzailea, nota, iruzkina):
    existing_balorazioa=Balorazioa.getBalorazioa(kodeFilma, kodeErabiltzailea)
    if not existing_balorazioa:
        kodeFilm = kodeFilma
        kodePers = kodeErabiltzailea
        nota = nota
        iruzkina = iruzkina
        db.insert(" INSERT INTO Puntuazioa (kodeFilm, kodePers, nota, iruzkina) VALUES (?, ?, ?, ?)", (kodeFilm, kodePers, nota, iruzkina))
        return True
    else:
        return False