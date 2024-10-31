from flask import Response, request, Blueprint
import json
from ..database import db
from ..models.birds import Birds
from ..models.adopter import Adopter

birds_bp = Blueprint('birds', __name__)


# Pegar todos os passaros do DB
@birds_bp.route('/birds', methods=['GET'])
def get_birds():
    birds = Birds.query.all()
    birds_json = [bird.to_json() for bird in birds]
    return gerar_response(
        200,
        'birds',
        birds_json)


# Filtra os passaros adotados (bird_adopted=True)
@birds_bp.route('/birds/adopted', methods=['GET'])
def get_adopted_birds():
    try:
        adopted_birds = Birds.query.filter_by(bird_adopted=True).all()
        birds_json = [bird.to_json() for bird in adopted_birds]
        if not birds_json:
            return gerar_response(
                404,
                'bird',
                {},
                'No adopted birds found'
            )
        return gerar_response(
            200,
            'birds',
            birds_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'bird',
            {},
            f'Error: {str(e)}'
        )


# Filtra os passaros adotados (bird_adopted=False)
@birds_bp.route('/birds/no_adopted', methods=['GET'])
def get_no_adopted_birds():
    try:
        no_adopted_birds = Birds.query.filter_by(bird_adopted=False).all()
        birds_json = [bird.to_json() for bird in no_adopted_birds]
        if not birds_json:
            return gerar_response(
                404,
                'bird',
                {},
                'No birds no adopted found'
            )
        return gerar_response(
            200,
            'birds',
            birds_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'bird',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um passaro por nome do DB
@birds_bp.route('/birds/name/<string:bird_name>', methods=['GET'])
def get_bird_name(bird_name):
    try:
        bird = Birds.query.filter_by(bird_name=bird_name).first()
        if not bird:
            return gerar_response(
                404,
                'bird',
                {},
                f'No birds found with name {bird_name}'
            )
        bird_json = bird.to_json()
        return gerar_response(
            200,
            'bird',
            bird_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'bird',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um passaro por idade do DB
@birds_bp.route('/birds/age/<string:bird_age>', methods=['GET'])
def get_bird_age(bird_age):
    valid_ages = ["jovem", "adulto", "idoso"]

    # Verifica se a idade passada é válida
    if bird_age not in valid_ages:
        return gerar_response(
            400,
            'bird',
            {},
            f'Invalid age value. Allowed values are: {", ".join(valid_ages)}'
        )
    try:
        birds = Birds.query.filter_by(bird_age=bird_age).all()
        birds_json = [bird.to_json() for bird in birds]
        if not birds_json:
            return gerar_response(
                404,
                'bird',
                {},
                f'No birds found with age {bird_age}'
            )
        return gerar_response(
            200,
            'birds',
            birds_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'bird',
            {},
            f'Error: {str(e)}'
        )


# Filtra um passaro pela cor
@birds_bp.route('/birds/color/<string:bird_color>', methods=['GET'])
def get_bird_color(bird_color):
    try:
        birds = Birds.query.filter_by(bird_color=bird_color).all()
        birds_json = [bird.to_json() for bird in birds]
        if not birds_json:
            return gerar_response(
                404,
                'bird',
                {},
                f'No birds found with color {bird_color}'
            )
        return gerar_response(
            200,
            'birds',
            birds_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'bird',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um passaro por ID
@birds_bp.route('/bird/id/<int:bird_id>', methods=['GET'])
def get_bird_id(bird_id):
    try:
        bird = Birds.query.filter_by(bird_id=bird_id).first()
        if not bird:
            return gerar_response(
                404,
                'bird',
                {},
                f'No birds found with name {bird_id}'
            )
        bird_json = bird.to_json()
        return gerar_response(
            200,
            'bird',
            bird_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'bird',
            {},
            f'Error: {str(e)}'
        )


# Cria um passaro no BD
@birds_bp.route('/birds', methods=['POST'])
def post_bird():
    body = request.get_json()
    try:
        # Verifica se já existe um passaro com o mesmo nome
        existing_bird = Birds.query.filter_by(
            bird_name=body['bird_name']).first()
        if existing_bird:
            return gerar_response(
                400,
                'bird',
                {},
                'A bird with this name already exists'
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
        # Criando o objeto birds com os campos corretos
        bird = Birds(
            bird_name=body['bird_name'],
            bird_age=(body['bird_age']),
            bird_image_url=body['bird_image_url'],
            bird_color=body['bird_color'],
            # Define como adotado se o adotante for informado
            bird_adopted=bool(adopter),
            adopter=adopter  # Relacionamento com o adotante
        )
        db.session.add(bird)
        db.session.commit()
        return gerar_response(
            201,
            'bird',
            bird.to_json(),
            'bird created successfully'
        )
    except Exception as e:
        return gerar_response(
            400,
            'bird',
            {},
            f'Error creating bird: {str(e)}'
        )


# Atualizar um passaro no BD
@birds_bp.route('/birds/<bird_id>', methods=['PUT'])
def update_bird(bird_id):
    try:
        # Buscar o passaro pelo ID
        bird = Birds.query.filter_by(bird_id=bird_id).first()
        if not bird:
            return gerar_response(
                404,
                'bird',
                {},
                'bird not found'
            )
        body = request.get_json()
        # Atualizar o status de adoção
        if 'bird_adopted' in body:
            bird.bird_adopted = body['bird_adopted']
        # Atualizar o adotante, se o ID foi fornecido
        if 'adopter_id' in body:
            adopter = Adopter.query.filter_by(
                adopter_id=body['adopter_id']).first()
            if adopter:
                # Atualiza o ID do adotante
                bird.adopter_id = adopter.adopter_id
                bird.bird_adopted = True
            else:
                return gerar_response(
                    404,
                    'Udopter',
                    {},
                    f'Udopter with ID {body["adopter_id"]} not found'
                )
        db.session.commit()
        return gerar_response(
            200,
            'bird',
            bird.to_json(),
            'bird updated successfully'
        )
    except Exception as e:
        return gerar_response(
            400,
            'bird',
            {},
            f'Error updating bird: {str(e)}'
        )


# Deletar um passaro do BD
@birds_bp.route('/birds/<bird_id>', methods=['DELETE'])
def delete_bird(bird_id):
    try:
        # Buscar o passaro pelo ID
        bird = Birds.query.filter_by(bird_id=bird_id).first()
        if not bird:
            return gerar_response(
                404,
                'bird',
                {},
                'bird not found'
            )
        db.session.delete(bird)
        db.session.commit()
        return gerar_response(
            200,
            'bird',
            {},
            'bird deleted successfully'
        )
    except Exception as e:
        db.session.rollback()
        return gerar_response(
            400,
            'bird',
            {},
            f'Error deleting bird: {str(e)}'
        )


# Filtro para varias descrições
@birds_bp.route('/birds/filter', methods=['GET'])
def filter_birds():
    try:
        # Obtendo parâmetros opcionais da query string
        # Nome do passaro
        bird_name = request.args.get('bird_name', type=str)
        # Idade do passaro
        bird_age = request.args.get('bird_age', type=str)
        # Cor do passaro
        bird_color = request.args.get('bird_color', type=str)
        # URL da imagem
        bird_image_url = request.args.get('bird_image_url', type=str)
        # Se está adotado
        bird_adopted = request.args.get(
            'bird_adopted', type=lambda x: (str(x).lower() == 'true'))
        # ID do adotante
        adopter_id = request.args.get('adopter_id', type=int)
        # Construindo a query com base nos filtros fornecidos
        query = Birds.query
        if bird_name is not None:
            query = query.filter_by(bird_name=bird_name)
        if bird_age is not None:
            query = query.filter_by(bird_age=bird_age)
        if bird_color is not None:
            query = query.filter_by(bird_color=bird_color)
        if bird_image_url is not None:
            query = query.filter_by(bird_image_url=bird_image_url)
        if bird_adopted is not None:
            query = query.filter_by(bird_adopted=bird_adopted)
        if adopter_id is not None:
            query = query.filter_by(adopter_id=adopter_id)
        # Executa a query final
        birds = query.all()
        birds_json = [bird.to_json() for bird in birds]
        if not birds_json:
            return gerar_response(
                404,
                'bird',
                {},
                'No birds found with the specified filters'
            )
        return gerar_response(
            200,
            'birds',
            birds_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'bird',
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
        mimetype='applibirdion/json'
    )
