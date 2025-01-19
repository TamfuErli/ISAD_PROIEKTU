from flask import Blueprint, request, jsonify, session, abort # type: ignore
from modeloa import Balorazioa, Pelikula, Erabiltzailea
from modeloa import Connection

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
    
