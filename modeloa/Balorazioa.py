import sqlite3 
from Connection import Connection

db = sqlite3.Connection()

class Balorazioa:
    def __init__(self, balioa, textua, filmId):
        self.balioa = balioa
        self.textua = textua
        self.filmId = filmId
        
