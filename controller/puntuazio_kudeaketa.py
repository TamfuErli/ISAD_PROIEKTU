from flask import Blueprint, request, jsonify, session, abort # type: ignore
from modeloa import Balorazioa, Pelikula, Erabiltzailea

def baloratu_pelikula(movie_id):
    """
    Guarda la valoración de un usuario para una película.
    """
    usuario_id = session.get('user_id')  # Erabiltzaileak saioa hasi behar du balorazio bat egin aurretik.
                                        # Ez dakit nola ikusi ondoren inplementatu
    if not usuario_id:
        return abort(403, "Debes iniciar sesión para valorar una película.")

    data = request.json
    puntuacion = data.get('puntuacion')
    comentario = data.get('comentario', '')

    if not 1 <= puntuacion <= 5:
        return abort(400, "La puntuación debe estar entre 1 y 5.")

    balorazioa_gorde(movie_id, usuario_id, puntuacion, comentario)

    return jsonify({"message": "Valoración registrada correctamente."}), 201

def get_balorazioGuztiak():
    """
    Devuelve todas las valoraciones de todas las películas.
    """
    balorazioak = Balorazioa.select()
    return jsonify([b.serialize() for b in balorazioak])
    
