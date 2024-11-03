from flask import Response, request, Blueprint
import json
from ..database import db
from ..models.adopter import Adopter

# Definindo o Blueprint para as rotas relacionadas aos adotantes
adopters_bp = Blueprint('adopters', __name__)


# Rota para criar um novo adotante
@adopters_bp.route('/adopters', methods=['POST'])
def post_adopter():
    body = request.get_json()

    # Verifica se já existe um adotante com o mesmo email
    try:
        existing_adopter = Adopter.query.filter_by(
            adopter_email=body['adopter_email']).first()
        if existing_adopter:
            return generate_response(400,
                                     'Adopter',
                                     {},
                                     'Adopter with this email already exists')

        # Cria um novo objeto Adopter com os dados recebidos
        adopter = Adopter(
            adopter_full_name=body['adopter_full_name'],
            adopter_age=body['adopter_age'],
            adopter_email=body['adopter_email'],
            adopter_phone=body['adopter_phone'],
            adopter_address=body['adopter_address'],
            adopter_residence_type=body['adopter_residence_type'],
            adopter_has_garden=body.get('adopter_has_garden', False),
            adopter_other_pets=body.get('adopter_other_pets'),
            adopter_pet_type=body['adopter_pet_type'],
            adopter_pet_preference=body.get('adopter_pet_preference'),
            adopter_occupation=body['adopter_occupation'],
            adopter_work_hours=body['adopter_work_hours'],
            adopter_income=body['adopter_income'],
            adopter_adoption_reason=body['adopter_adoption_reason'],
            adopter_commitment_to_care=body['adopter_commitment_to_care'],
            adopter_experience_with_pets=body.get(
                'adopter_experience_with_pets'),
            adopter_additional_info=body.get('adopter_additional_info')
        )

        # Adiciona e confirma o novo adotante no banco de dados
        db.session.add(adopter)
        db.session.commit()
        return generate_response(201,
                                 'adopter',
                                 adopter.to_json(),
                                 'Adopter created successfully')
    except Exception as e:
        return generate_response(400,
                                 'Adopter',
                                 {},
                                 f'Error creating adopter: {str(e)}')


# Rota para obter todos os adotantes
@adopters_bp.route('/adopters', methods=['GET'])
def get_adopters():
    try:
        # Recupera todos os adotantes e os converte para JSON
        adopters = Adopter.query.all()
        adopters_json = [adopter.to_json() for adopter in adopters]
        return generate_response(200,
                                 'adopters',
                                 adopters_json,
                                 'ok')
    except Exception as e:
        return generate_response(400,
                                 'Adopter',
                                 {},
                                 f'Error fetching adopters: {str(e)}')


# Rota para obter um único adotante pelo ID
@adopters_bp.route('/adopters/<int:adopter_id>', methods=['GET'])
def get_adopter(adopter_id):
    try:
        # Busca o adotante pelo ID fornecido
        adopter = Adopter.query.filter_by(adopter_id=adopter_id).first()
        if not adopter:
            return generate_response(404,
                                     'Adopter',
                                     {},
                                     f'No adopter found with id {adopter_id}')
        return generate_response(200, 'adopter', adopter.to_json(), 'ok')
    except Exception as e:
        return generate_response(400,
                                 'Adopter',
                                 {},
                                 f'Error fetching adopter: {str(e)}')


# Rota para atualizar os dados de um adotante existente
@adopters_bp.route('/adopters/<int:adopter_id>', methods=['PUT'])
def update_adopter(adopter_id):
    adopter = Adopter.query.filter_by(adopter_id=adopter_id).first()

    # Verifica se o adotante existe
    if not adopter:
        return generate_response(404,
                                 'Adopter',
                                 {},
                                 f'No adopter found with id {adopter_id}')

    body = request.get_json()

    # Atualizar os dados do adotante com o que foi passado na requisição
    try:
        if 'adopter_full_name' in body:
            adopter.adopter_full_name = body['adopter_full_name']
        if 'adopter_age' in body:
            adopter.adopter_age = body['adopter_age']
        if 'adopter_phone' in body:
            adopter.adopter_phone = body['adopter_phone']
        if 'adopter_address' in body:
            adopter.adopter_address = body['adopter_address']
        if 'adopter_residence_type' in body:
            adopter.adopter_residence_type = body['adopter_residence_type']
        if 'adopter_has_garden' in body:
            adopter.adopter_has_garden = body['adopter_has_garden']
        if 'adopter_other_pets' in body:
            adopter.adopter_other_pets = body['adopter_other_pets']
        if 'adopter_pet_type' in body:
            adopter.adopter_pet_type = body['adopter_pet_type']
        if 'adopter_pet_preference' in body:
            adopter.adopter_pet_preference = body['adopter_pet_preference']
        if 'adopter_occupation' in body:
            adopter.adopter_occupation = body['adopter_occupation']
        if 'adopter_work_hours' in body:
            adopter.adopter_work_hours = body['adopter_work_hours']
        if 'adopter_income' in body:
            adopter.adopter_income = body['adopter_income']
        if 'adopter_adoption_reason' in body:
            adopter.adopter_adoption_reason = body['adopter_adoption_reason']
        if 'adopter_commitment_to_care' in body:
            adopter.adopter_commitment_to_care = body
            ['adopter_commitment_to_care']
        if 'adopter_experience_with_pets' in body:
            adopter.adopter_experience_with_pets = body
            ['adopter_experience_with_pets']
        if 'adopter_additional_info' in body:
            adopter.adopter_additional_info = body['adopter_additional_info']

        # Confirma a atualização dos dados no banco de dados
        db.session.commit()
        return generate_response(200,
                                 'adopter',
                                 adopter.to_json(),
                                 'Adopter updated successfully')
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return generate_response(400,
                                 'Adopter',
                                 {},
                                 f'Error updating adopter: {str(e)}')

# Rota para deletar um adotante pelo ID


@adopters_bp.route('/adopters/<int:adopter_id>', methods=['DELETE'])
def delete_adopter(adopter_id):
    adopter = Adopter.query.filter_by(adopter_id=adopter_id).first()

    # Verifica se o adotante existe
    if not adopter:
        return generate_response(404,
                                 'Adopter',
                                 {},
                                 f'No adopter found with id {adopter_id}')

    # Tenta deletar o adotante do banco de dados
    try:
        db.session.delete(adopter)
        db.session.commit()
        return generate_response(200,
                                 'Adopter',
                                 {},
                                 'Adopter deleted successfully')
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return generate_response(400, 'Adopter',
                                 {},
                                 f'Error deleting adopter: {str(e)}')


# Função para gerar uma resposta HTTP padronizada
def generate_response(status, content_name, content, message=False):
    body = {content_name: content}
    if message:
        body['message'] = message

    return Response(json.dumps(body),
                    status=status,
                    mimetype='application/json')
