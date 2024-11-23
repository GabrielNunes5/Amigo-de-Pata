from flask import Blueprint, request
from ..services.animals_service import (
    get_all_animals,
    get_animal_filter,
    create_animal,
    update_animal,
    delete_animal
)

animals_bp = Blueprint('animals', __name__)


@animals_bp.route('/animals', methods=['GET'])
def get_animals():
    # Checa se há parâmetros de filtro na query string
    if request.args:
        return get_animal_filter()
    return get_all_animals()


@animals_bp.route('/animals', methods=['POST'])
def post_animal():
    body = request.get_json()
    return create_animal(body)


@animals_bp.route('/animals/<int:animal_id>', methods=['PUT'])
def put_animal(animal_id):
    body = request.get_json()
    return update_animal(animal_id, body)


@animals_bp.route('/animals/<int:animal_id>', methods=['DELETE'])
def delete_animal_route(animal_id):
    return delete_animal(animal_id)
