import sqlite3

def balorazioa_gorde(pelicula_id, usuario_id, puntuacion, comentario):
    """
    Guarda la valoración de un usuario en la base de datos.
    """
    connection = sqlite3.connect('datuBasea.db')
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO valoraciones (pelicula_id, usuario_id, puntuacion, comentario)
        VALUES (?, ?, ?, ?)
    """, (pelicula_id, usuario_id, puntuacion, comentario))

    connection.commit()
    connection.close()

def get_balorazioa(pelicula_id):
    """
    Obtiene todas las valoraciones de una película.
    """
    connection = sqlite3.connect('datuBasea.db')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT usuario_id, puntuacion, comentario, fecha
        FROM valoraciones
        WHERE pelicula_id = ?
        ORDER BY fecha DESC
    """, (pelicula_id,))

    valoraciones = cursor.fetchall()
    connection.close()

    return valoraciones
