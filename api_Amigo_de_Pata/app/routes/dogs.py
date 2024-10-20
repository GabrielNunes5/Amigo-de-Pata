from flask import Response, request, Blueprint
import json
from ..database import db
from ..models.dogs import Dogs
from ..models.users import Users

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


# Filtra os cachorros adotados (dog_adopted=True)
@dogs_bp.route('/dogs/adopted', methods=['GET'])
def get_adopted_dogs():
    try:
        adopted_dogs = Dogs.query.filter_by(dog_adopted=True).all()
        dogs_json = [dog.to_json() for dog in adopted_dogs]

        if not dogs_json:
            return gerar_response(
                404,
                'dog',
                {},
                'No adopted dogs found'
            )

        return gerar_response(
            200,
            'dogs',
            dogs_json,
            'ok'
        )

    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error: {str(e)}'
        )


# Filtra os cachorros adotados (dog_adopted=False)
@dogs_bp.route('/dogs/no_adopted', methods=['GET'])
def get_no_adopted_dogs():
    try:
        no_adopted_dogs = Dogs.query.filter_by(dog_adopted=False).all()
        dogs_json = [dog.to_json() for dog in no_adopted_dogs]

        if not dogs_json:
            return gerar_response(
                404,
                'dog',
                {},
                'No dogs no adopted found'
            )

        return gerar_response(
            200,
            'dogs',
            dogs_json,
            'ok'
        )

    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um gato por nome do DB
@dogs_bp.route('/dogs/name/<string:dog_name>', methods=['GET'])
def get_dog_name(dog_name):
    try:
        dog = Dogs.query.filter_by(dog_name=dog_name).first()

        if not dog:
            return gerar_response(
                404,
                'dog',
                {},
                f'No dogs found with name {dog_name}'
            )

        dog_json = dog.to_json()
        return gerar_response(
            200,
            'dog',
            dog_json,
            'ok'
        )

    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um gato por idade do DB
@dogs_bp.route('/dogs/age/<string:dog_age>', methods=['GET'])
def get_dog_age(dog_age):
    valid_ages = ["jovem", "adulto", "idoso"]

    # Verifica se a idade passada é válida
    if dog_age not in valid_ages:
        return gerar_response(
            400,
            'dog',
            {},
            f'Invalid age value. Allowed values are: {", ".join(valid_ages)}'
        )

    try:
        dogs = Dogs.query.filter_by(dog_age=dog_age).all()
        dogs_json = [dog.to_json() for dog in dogs]

        if not dogs_json:
            return gerar_response(
                404,
                'dog',
                {},
                f'No dogs found with age {dog_age}'
            )

        return gerar_response(
            200,
            'dogs',
            dogs_json,
            'ok'
        )

    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error: {str(e)}'
        )


# Filtra um gato pela cor
@dogs_bp.route('/dogs/color/<string:dog_color>', methods=['GET'])
def get_dog_color(dog_color):
    try:
        dogs = Dogs.query.filter_by(dog_color=dog_color).all()
        dogs_json = [dog.to_json() for dog in dogs]
        if not dogs_json:
            return gerar_response(
                404,
                'dog',
                {},
                f'No dogs found with color {dog_color}'
            )
        return gerar_response(
            200,
            'dogs',
            dogs_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error: {str(e)}'
        )


# Cria um gato no BD
@dogs_bp.route('/dogs', methods=['POST'])
def post_dog():
    body = request.get_json()

    try:
        # Verifica se já existe um gato com o mesmo nome
        existing_dog = Dogs.query.filter_by(dog_name=body['dog_name']).first()
        if existing_dog:
            return gerar_response(
                400,
                'dog',
                {},
                'A dog with this name already exists'
            )

        # Verifica se o ID do adotante foi enviado e se o usuário existe
        adopter_id = body.get('adopter_id')  # O adotante é opcional
        adopter = None
        if adopter_id:
            adopter = Users.query.get(adopter_id)
            if not adopter:
                return gerar_response(
                    404,
                    'User',
                    {},
                    'Adopter not found'
                )

        # Criando o objeto dogs com os campos corretos
        dog = Dogs(
            dog_name=body['dog_name'],
            dog_age=(body['dog_age']),
            dog_image_url=body['dog_image_url'],
            dog_color=body['dog_color'],
            # Define como adotado se o adotante for informado
            dog_adopted=bool(adopter),
            adopter=adopter  # Relacionamento com o adotante
        )

        db.session.add(dog)
        db.session.commit()

        return gerar_response(
            201,
            'dog',
            dog.to_json(),
            'dog created successfully'
        )

    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error creating dog: {str(e)}'
        )


# Atualizar um gato no BD
@dogs_bp.route('/dogs/<dog_id>', methods=['PUT'])
def update_dog(dog_id):
    try:
        # Buscar o gato pelo ID
        dog = Dogs.query.filter_by(dog_id=dog_id).first()

        if not dog:
            return gerar_response(
                404,
                'dog',
                {},
                'dog not found'
            )

        body = request.get_json()

        # Atualizar o status de adoção
        if 'dog_adopted' in body:
            dog.dog_adopted = body['dog_adopted']

        # Atualizar o adotante, se o ID foi fornecido
        if 'adopter_id' in body:
            adopter = Users.query.filter_by(user_id=body['adopter_id']).first()
            if adopter:
                dog.adopter_id = adopter.user_id  # Atualiza o ID do adotante
            else:
                return gerar_response(
                    404,
                    'User',
                    {},
                    f'User with ID {body["adopter_id"]} not found'
                )

        db.session.commit()

        return gerar_response(
            200,
            'dog',
            dog.to_json(),
            'dog updated successfully'
        )

    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error updating dog: {str(e)}'
        )


# Deletar um gato do BD
@dogs_bp.route('/dogs/<dog_id>', methods=['DELETE'])
def delete_dog(dog_id):
    try:
        # Buscar o gato pelo ID
        dog = Dogs.query.filter_by(dog_id=dog_id).first()
        if not dog:
            return gerar_response(
                404,
                'dog',
                {},
                'dog not found'
            )
        db.session.delete(dog)
        db.session.commit()
        return gerar_response(
            200,
            'dog',
            {},
            'dog deleted successfully'
        )
    except Exception as e:
        db.session.rollback()
        return gerar_response(
            400,
            'dog',
            {},
            f'Error deleting dog: {str(e)}'
        )


# Filtro para varias descrições
@dogs_bp.route('/dogs/filter', methods=['GET'])
def filter_dogs():
    try:
        # Obtendo parâmetros opcionais da query string
        # Nome do gato
        dog_name = request.args.get('dog_name', type=str)
        # Idade do gato
        dog_age = request.args.get('dog_age', type=str)
        # Cor do gato
        dog_color = request.args.get('dog_color', type=str)
        # URL da imagem
        dog_image_url = request.args.get('dog_image_url', type=str)
        # Se está adotado
        dog_adopted = request.args.get(
            'dog_adopted', type=lambda x: (str(x).lower() == 'true'))
        # ID do adotante
        adopter_id = request.args.get('adopter_id', type=int)
        # Construindo a query com base nos filtros fornecidos
        query = Dogs.query

        if dog_name is not None:
            query = query.filter_by(dog_name=dog_name)
        if dog_age is not None:
            query = query.filter_by(dog_age=dog_age)
        if dog_color is not None:
            query = query.filter_by(dog_color=dog_color)
        if dog_image_url is not None:
            query = query.filter_by(dog_image_url=dog_image_url)
        if dog_adopted is not None:
            query = query.filter_by(dog_adopted=dog_adopted)
        if adopter_id is not None:
            query = query.filter_by(adopter_id=adopter_id)

        # Executa a query final
        dogs = query.all()
        dogs_json = [dog.to_json() for dog in dogs]

        if not dogs_json:
            return gerar_response(
                404,
                'dog',
                {},
                'No dogs found with the specified filters'
            )

        return gerar_response(
            200,
            'dogs',
            dogs_json,
            'ok'
        )

    except Exception as e:
        return gerar_response(
            400,
            'dog',
            {},
            f'Error: {str(e)}'
        )


def gerar_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if mensagem:
        body['mensagem'] = mensagem

    return Response(
        json.dumps(body),
        status=status,
        mimetype='applidogion/json'
        )
