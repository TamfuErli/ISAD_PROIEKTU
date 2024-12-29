from modeloa import Erabiltzailea, Pelikula, Connection


class Filmoteka:
    def __init__(self):
        self.erabiltzaileak = []
        self.pelikulak = []
        self.erabiltzailea = None

def sortuErabiltzailea(izena, pasahitza, posta):
    Erabiltzailea.gehituErabiltzailea((izena, pasahitza, posta))