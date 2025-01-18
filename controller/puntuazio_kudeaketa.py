from flask import Blueprint, request, jsonify, session, abort # type: ignore
from modeloa.Balorazioa import balorazioa_gorde, get_balorazioa

valoraciones_bp = Blueprint('valoraciones', __name__)

@valoraciones_bp.route('/rate/<int:movie_id>', methods=['POST'])
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

@valoraciones_bp.route('/ratings/<int:movie_id>', methods=['GET'])
def get_balorazioGuztiak(movie_id):
    """
    Obtiene todas las valoraciones de una película.
    """
    valoraciones = get_balorazioa(movie_id)
    valoraciones_list = [
        {"usuario_id": v[0], "puntuacion": v[1], "comentario": v[2], "fecha": v[3]}
        for v in valoraciones
    ]

    return jsonify(valoraciones_list), 200
