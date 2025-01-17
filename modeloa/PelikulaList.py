import sqlite3
from modeloa import Pelikula

class PelikulaList:
    """def __init__(self):
        self.films = []

    def add_film(self, film):
        if isinstance(film, Pelikula):
            self.films.append(film)

    def remove_film(self, film):
        if film in self.films:
            self.films.remove(film)

    def get_films(self):
        return self.films"""
    
    _instance = None  # Variable de clase para garantizar una sola instancia.

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._pelikula = []  # Inicializa la lista de películas.
        return cls._instance

    def cargar_peliculas(self):
        conn = sqlite3.connect('datuBasea.db')
        cursor = conn.cursor()
        cursor.execute("SELECT kodeFilm, izena, poster_path, deskripzioa, balorazioa, data, onartua FROM Filma")

        rows = cursor.fetchall()
        self._pelikula = [Pelikula(*row) for row in rows]

        conn.close()

    def obtener_peliculas(self):
        """
        Retorna la lista de películas cargadas.
        """
        return self._pelikula

    def agregar_pelicula(self, pelicula):
        """
        Agrega una nueva película a la lista y la guarda en la base de datos.
        """
        if not isinstance(pelicula, Pelikula):
            raise ValueError("El objeto debe ser una instancia de la clase Peliculas.")

        # Agrega a la lista en memoria.
        self._pelikula.append(pelicula)

        # Guarda en la base de datos.
        conn = sqlite3.connect('datuBasea.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Filma (kodeFilm, izena, poster_path, deskripzioa, balorazioa, data, onartua)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (pelicula.kodeFilma, pelicula.izena, pelicula.poster_path, pelicula.deskripzioa, pelicula.balorazioa, pelicula.data, pelicula.onartua))

        conn.commit()
        conn.close()

    def eliminar_pelicula(self, pelicula_id):
        """
        Elimina una película de la lista y de la base de datos.
        """
        # Busca la película en la lista.
        pelicula_a_eliminar = next((p for p in self._peliculas if p.id == pelicula_id), None)
        if pelicula_a_eliminar is None:
            raise ValueError("Película no encontrada.")

        # Elimina de la lista en memoria.
        self._pelikula.remove(pelicula_a_eliminar)

        # Elimina de la base de datos.
        conn = sqlite3.connect('datuBasea.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Filma WHERE id = ?", (pelicula_id,))
        conn.commit()
        conn.close()