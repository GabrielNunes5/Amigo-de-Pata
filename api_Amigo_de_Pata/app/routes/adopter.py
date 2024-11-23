from flask import Blueprint, request
from ..services.adopter_service import (
    get_all_adopters,
    get_adopter_filter,
    create_adopter,
    update_adopter,
    delete_adopter
)

adopters_bp = Blueprint('adopters_bp', __name__)


@adopters_bp.route('/adopter', methods=['GET'])
def get_adopters():
    # Checa se há parâmetros de filtro na query string
    if request.args:
        return get_adopter_filter()
    return get_all_adopters()


@adopters_bp.route('/adopter', methods=['POST'])
def post_adopter():
    body = request.get_json()
    return create_adopter(body)


@adopters_bp.route('/adopter/<int:adopter_id>', methods=['PUT'])
def put_adopter(adopter_id):
    body = request.get_json()
    return update_adopter(adopter_id, body)


@adopters_bp.route('/adopter/<int:adopter_id>', methods=['DELETE'])
def delete_adopter_route(adopter_id):
    return delete_adopter(adopter_id)
