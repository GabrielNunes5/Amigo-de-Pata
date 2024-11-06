from flask import Response, request, Blueprint
import json
from ..database import db
from ..models.misce import Animals
from ..models.adopter import Adopter

animals_bp = Blueprint('animals', __name__)


# Pegar todos os animais do DB
@animals_bp.route('/animals', methods=['GET'])
def get_animals():
    animals = Animals.query.all()
    animals_json = [animal.to_json() for animal in animals]
    return gerar_response(
        200,
        'animals',
        animals_json)


# Filtra os animais adotados (animal_adopted=True)
@animals_bp.route('/animals/adopted', methods=['GET'])
def get_adopted_animals():
    try:
        adopted_animals = Animals.query.filter_by(animal_adopted=True).all()
        animals_json = [animal.to_json() for animal in adopted_animals]
        if not animals_json:
            return gerar_response(
                404,
                'animal',
                {},
                'No adopted animals found'
            )
        return gerar_response(
            200,
            'animals',
            animals_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'animal',
            {},
            f'Error: {str(e)}'
        )


# Filtra os animais adotados (animal_adopted=False)
@animals_bp.route('/animals/no_adopted', methods=['GET'])
def get_no_adopted_animals():
    try:
        no_adopted_animals = Animals.query.filter_by(
            animal_adopted=False).all()
        animals_json = [animal.to_json() for animal in no_adopted_animals]
        if not animals_json:
            return gerar_response(
                404,
                'animal',
                {},
                'No animals no adopted found'
            )
        return gerar_response(
            200,
            'animals',
            animals_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'animal',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um animal por nome do DB
@animals_bp.route('/animals/name/<string:animal_name>', methods=['GET'])
def get_animal_name(animal_name):
    try:
        animal = Animals.query.filter_by(animal_name=animal_name).first()
        if not animal:
            return gerar_response(
                404,
                'animal',
                {},
                f'No animals found with name {animal_name}'
            )
        animal_json = animal.to_json()
        return gerar_response(
            200,
            'animal',
            animal_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'animal',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um animal por idade do DB
@animals_bp.route('/animals/age/<string:animal_age>', methods=['GET'])
def get_animal_age(animal_age):
    valid_ages = ["jovem", "adulto", "idoso"]

    # Verifica se a idade passada é válida
    if animal_age not in valid_ages:
        return gerar_response(
            400,
            'animal',
            {},
            f'Invalid age value. Allowed values are: {", ".join(valid_ages)}'
        )
    try:
        animals = Animals.query.filter_by(animal_age=animal_age).all()
        animals_json = [animal.to_json() for animal in animals]
        if not animals_json:
            return gerar_response(
                404,
                'animal',
                {},
                f'No animals found with age {animal_age}'
            )
        return gerar_response(
            200,
            'animals',
            animals_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'animal',
            {},
            f'Error: {str(e)}'
        )


# Filtra um animal pela cor
@animals_bp.route('/animals/color/<string:animal_color>', methods=['GET'])
def get_animal_color(animal_color):
    try:
        animals = Animals.query.filter_by(animal_color=animal_color).all()
        animals_json = [animal.to_json() for animal in animals]
        if not animals_json:
            return gerar_response(
                404,
                'animal',
                {},
                f'No animals found with color {animal_color}'
            )
        return gerar_response(
            200,
            'animals',
            animals_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'animal',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um animal por ID
@animals_bp.route('/animal/id/<int:animal_id>', methods=['GET'])
def get_animal_id(animal_id):
    try:
        animal = Animals.query.filter_by(animal_id=animal_id).first()
        if not animal:
            return gerar_response(
                404,
                'animal',
                {},
                f'No animals found with name {animal_id}'
            )
        animal_json = animal.to_json()
        return gerar_response(
            200,
            'animal',
            animal_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'animal',
            {},
            f'Error: {str(e)}'
        )


# Cria um animal no BD
@animals_bp.route('/animals', methods=['POST'])
def post_animal():
    body = request.get_json()
    try:
        # Verifica se já existe um animal com o mesmo nome
        existing_animal = Animals.query.filter_by(
            animal_name=body['animal_name']).first()
        if existing_animal:
            return gerar_response(
                400,
                'animal',
                {},
                'A animal with this name already exists'
            )
        # Verifica se o ID do adotante foi enviado e se o usuário existe
        adopter_id = body.get('adopter_id')  # O adotante é opcional
        adopter = None
        if adopter_id:
            adopter = Adopter.query.get(adopter_id)
            if not adopter:
                return gerar_response(
                    404,
                    'Adopter',
                    {},
                    'Adopter not found'
                )
        # Criando o objeto animals com os campos corretos
        animal = Animals(
            animal_name=body['animal_name'],
            animal_age=(body['animal_age']),
            animal_image_url=body['animal_image_url'],
            animal_color=body['animal_color'],
            # Define como adotado se o adotante for informado
            animal_adopted=bool(adopter),
            adopter=adopter  # Relacionamento com o adotante
        )
        db.session.add(animal)
        db.session.commit()
        return gerar_response(
            201,
            'animal',
            animal.to_json(),
            'animal created successfully'
        )
    except Exception as e:
        return gerar_response(
            400,
            'animal',
            {},
            f'Error creating animal: {str(e)}'
        )


# Atualizar um animal no BD
@animals_bp.route('/animals/<animal_id>', methods=['PUT'])
def update_animal(animal_id):
    try:
        # Buscar o animal pelo ID
        animal = Animals.query.filter_by(animal_id=animal_id).first()
        if not animal:
            return gerar_response(
                404,
                'animal',
                {},
                'animal not found'
            )
        body = request.get_json()
        # Atualizar o status de adoção
        if 'animal_adopted' in body:
            animal.animal_adopted = body['animal_adopted']
        # Atualizar o adotante, se o ID foi fornecido
        if 'adopter_id' in body:
            adopter = Adopter.query.filter_by(
                adopter_id=body['adopter_id']).first()
            if adopter:
                # Atualiza o ID do adotante
                animal.adopter_id = adopter.adopter_id
                animal.animal_adopted = True
            else:
                return gerar_response(
                    404,
                    'Adopter',
                    {},
                    f'Adopter with ID {body["adopter_id"]} not found'
                )
        db.session.commit()
        return gerar_response(
            200,
            'animal',
            animal.to_json(),
            'animal updated successfully'
        )
    except Exception as e:
        return gerar_response(
            400,
            'animal',
            {},
            f'Error updating animal: {str(e)}'
        )


# Deletar um animal do BD
@animals_bp.route('/animals/<animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    try:
        # Buscar o animal pelo ID
        animal = Animals.query.filter_by(animal_id=animal_id).first()
        if not animal:
            return gerar_response(
                404,
                'animal',
                {},
                'animal not found'
            )
        db.session.delete(animal)
        db.session.commit()
        return gerar_response(
            200,
            'animal',
            {},
            'animal deleted successfully'
        )
    except Exception as e:
        db.session.rollback()
        return gerar_response(
            400,
            'animal',
            {},
            f'Error deleting animal: {str(e)}'
        )


# Filtro para varias descrições
@animals_bp.route('/animals/filter', methods=['GET'])
def filter_animals():
    try:
        # Obtendo parâmetros opcionais da query string
        # Nome do animal
        animal_name = request.args.get('animal_name', type=str)
        # Idade do animal
        animal_age = request.args.get('animal_age', type=str)
        # Cor do animal
        animal_species = request.args.get('animal_species', type=str)
        # URL da imagem
        animal_image_url = request.args.get('animal_image_url', type=str)
        # Se está adotado
        animal_adopted = request.args.get(
            'animal_adopted', type=lambda x: (str(x).lower() == 'true'))
        # ID do adotante
        adopter_id = request.args.get('adopter_id', type=int)
        # Construindo a query com base nos filtros fornecidos
        query = Animals.query
        if animal_name is not None:
            query = query.filter_by(animal_name=animal_name)
        if animal_age is not None:
            query = query.filter_by(animal_age=animal_age)
        if animal_species is not None:
            query = query.filter_by(animal_species=animal_species)
        if animal_image_url is not None:
            query = query.filter_by(animal_image_url=animal_image_url)
        if animal_adopted is not None:
            query = query.filter_by(animal_adopted=animal_adopted)
        if adopter_id is not None:
            query = query.filter_by(adopter_id=adopter_id)
        # Executa a query final
        animals = query.all()
        animals_json = [animal.to_json() for animal in animals]
        if not animals_json:
            return gerar_response(
                404,
                'animal',
                {},
                'No animals found with the specified filters'
            )
        return gerar_response(
            200,
            'animals',
            animals_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'animal',
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
        mimetype='application/json'
    )
