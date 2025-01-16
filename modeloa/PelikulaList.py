from modeloa import Pelikula

class PelikulaList:
    def __init__(self):
        self.films = []

    def add_film(self, film):
        if isinstance(film, Pelikula):
            self.films.append(film)

    def remove_film(self, film):
        if film in self.films:
            self.films.remove(film)

    def get_films(self):
        return self.films