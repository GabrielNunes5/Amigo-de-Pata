from flask import Response, request, Blueprint
import json
from ..database import db
from ..models.dogs import Dogs

dogs_bp = Blueprint('dogs', __name__)


# Pegar todos os cachorros do DB
@dogs_bp.route('/dogs', methods=['GET'])
def get_dogs():
    dogs = Dogs.query.all()
    dogs_json = [dog.to_json() for dog in dogs]

    return gerar_response(
        200,
        'dogs',
        dogs_json)


# Filtrar um cachorro por nome do DB
@dogs_bp.route('/dogs/name/<string:dog_name>', methods=['GET'])
def get_dog_name(dog_name):

    try:
        dog = Dogs.query.filter_by(dog_name=dog_name).first()
        dog_json = dog.to_json()

        return gerar_response(
            200,
            'dog',
            dog_json,
            'ok')

    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um cachorro por idade do DB
@dogs_bp.route('/dogs/age/<int:dog_age>', methods=['GET'])
def get_dog_age(dog_age):

    try:
        dogs = Dogs.query.filter_by(dog_age=dog_age).all()
        dogs_json = [dog.to_json() for dog in dogs]

        return gerar_response(
            200,
            'dog',
            dogs_json,
            'ok')

    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error: {str(e)}'
        )


# Cria um cachorro no BD
@dogs_bp.route('/dogs', methods=['POST'])
def post_dog():
    body = request.get_json()

    try:
        # Verifica se já existe um cachorro com o mesmo nome
        existing_dog = Dogs.query.filter_by(dog_name=body['dog_name']).first()
        if existing_dog:
            return gerar_response(
                400,
                'dog',
                {},
                'A dog with this name already exists')

        # Criando o objeto dogs com os campos corretos
        dog = Dogs(dog_name=body['dog_name'],
                   dog_age=int(body['dog_age']),
                   dog_image_url=body['dog_image_url'],
                   dog_color=body['dog_color']
                   )

        db.session.add(dog)
        db.session.commit()
        return gerar_response(
            201,
            'dog',
            dog.to_json(),
            'dog created successfully')
    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error creating dog: {str(e)}'
        )


# Atualizar um cachorro no BD
@dogs_bp.route('/dogs/<dog_id>', methods=['PUT'])
def update_dog(dog_id):
    dog = Dogs.query.filter_by(dog_id=dog_id).first()
    body = request.get_json()

    try:
        if 'dog_adopted' in body:
            dog.dog_adopted = body['dog_adopted']
        if 'dog_adopter_id' in body:
            dog.dog_adopter_id = body['dog_adopter_id']

        db.session.add(dog)
        db.session.commit()
        return gerar_response(
            200,
            'dog',
            dog.to_json(),
            'dog updated successfully')
    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error updating dog: {str(e)}'
        )


def gerar_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if mensagem:
        body['mensagem'] = mensagem

    return Response(
        json.dumps(body),
        status=status,
        mimetype='application/json'
        )