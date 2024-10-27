from flask import Response, request, Blueprint
import json
from ..database import db
from ..models.cats import Cats
from ..models.users import Users

cats_bp = Blueprint('cats', __name__)


# Pegar todos os gatos do DB
@cats_bp.route('/cats', methods=['GET'])
def get_cats():
    cats = Cats.query.all()
    cats_json = [cat.to_json() for cat in cats]
    return gerar_response(
        200,
        'cats',
        cats_json)


# Filtra os gatos adotados (cat_adopted=True)
@cats_bp.route('/cats/adopted', methods=['GET'])
def get_adopted_cats():
    try:
        adopted_cats = Cats.query.filter_by(cat_adopted=True).all()
        cats_json = [cat.to_json() for cat in adopted_cats]
        if not cats_json:
            return gerar_response(
                404,
                'Cat',
                {},
                'No adopted cats found'
            )
        return gerar_response(
            200,
            'cats',
            cats_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error: {str(e)}'
        )


# Filtra os gatos adotados (cat_adopted=False)
@cats_bp.route('/cats/no_adopted', methods=['GET'])
def get_no_adopted_cats():
    try:
        no_adopted_cats = Cats.query.filter_by(cat_adopted=False).all()
        cats_json = [cat.to_json() for cat in no_adopted_cats]
        if not cats_json:
            return gerar_response(
                404,
                'Cat',
                {},
                'No cats no adopted found'
            )
        return gerar_response(
            200,
            'cats',
            cats_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um gato por nome do DB
@cats_bp.route('/cats/name/<string:cat_name>', methods=['GET'])
def get_cat_name(cat_name):
    try:
        cat = Cats.query.filter_by(cat_name=cat_name).first()
        if not cat:
            return gerar_response(
                404,
                'Cat',
                {},
                f'No cats found with name {cat_name}'
            )
        cat_json = cat.to_json()
        return gerar_response(
            200,
            'cat',
            cat_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um gato por idade do DB
@cats_bp.route('/cats/age/<string:cat_age>', methods=['GET'])
def get_cat_age(cat_age):
    valid_ages = ["jovem", "adulto", "idoso"]

    # Verifica se a idade passada é válida
    if cat_age not in valid_ages:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Invalid age value. Allowed values are: {", ".join(valid_ages)}'
        )
    try:
        cats = Cats.query.filter_by(cat_age=cat_age).all()
        cats_json = [cat.to_json() for cat in cats]
        if not cats_json:
            return gerar_response(
                404,
                'Cat',
                {},
                f'No cats found with age {cat_age}'
            )
        return gerar_response(
            200,
            'cats',
            cats_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error: {str(e)}'
        )


# Filtra um gato pela cor
@cats_bp.route('/cats/color/<string:cat_color>', methods=['GET'])
def get_cat_color(cat_color):
    try:
        cats = Cats.query.filter_by(cat_color=cat_color).all()
        cats_json = [cat.to_json() for cat in cats]
        if not cats_json:
            return gerar_response(
                404,
                'Cat',
                {},
                f'No cats found with color {cat_color}'
            )
        return gerar_response(
            200,
            'cats',
            cats_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error: {str(e)}'
        )
    
# Filtrar um gato por ID
@cats_bp.route('/cat/id/<int:cat_id>', methods=['GET'])
def get_cat_id(cat_id):
    try:
        cat = Cats.query.filter_by(cat_id=cat_id).first()
        if not cat:
            return gerar_response(
                404,
                'Cat',
                {},
                f'No cats found with name {cat_id}'
            )
        cat_json = cat.to_json()
        return gerar_response(
            200,
            'cat',
            cat_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error: {str(e)}'
        )


# Cria um gato no BD
@cats_bp.route('/cats', methods=['POST'])
def post_cat():
    body = request.get_json()
    try:
        # Verifica se já existe um gato com o mesmo nome
        existing_cat = Cats.query.filter_by(cat_name=body['cat_name']).first()
        if existing_cat:
            return gerar_response(
                400,
                'Cat',
                {},
                'A cat with this name already exists'
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
        # Criando o objeto Cats com os campos corretos
        cat = Cats(
            cat_name=body['cat_name'],
            cat_age=(body['cat_age']),
            cat_image_url=body['cat_image_url'],
            cat_color=body['cat_color'],
            # Define como adotado se o adotante for informado
            cat_adopted=bool(adopter),
            adopter=adopter  # Relacionamento com o adotante
        )
        db.session.add(cat)
        db.session.commit()
        return gerar_response(
            201,
            'cat',
            cat.to_json(),
            'Cat created successfully'
        )
    except Exception as e:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error creating cat: {str(e)}'
        )


# Atualizar um gato no BD
@cats_bp.route('/cats/<cat_id>', methods=['PUT'])
def update_cat(cat_id):
    try:
        # Buscar o gato pelo ID
        cat = Cats.query.filter_by(cat_id=cat_id).first()
        if not cat:
            return gerar_response(
                404,
                'Cat',
                {},
                'Cat not found'
            )
        body = request.get_json()
        # Atualizar o status de adoção
        if 'cat_adopted' in body:
            cat.cat_adopted = body['cat_adopted']
        # Atualizar o adotante, se o ID foi fornecido
        if 'adopter_id' in body:
            adopter = Users.query.filter_by(user_id=body['adopter_id']).first()
            if adopter:
                cat.adopter_id = adopter.user_id  # Atualiza o ID do adotante
                cat.cat_adopted = True
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
            'cat',
            cat.to_json(),
            'Cat updated successfully'
        )
    except Exception as e:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error updating cat: {str(e)}'
        )


# Deletar um gato do BD
@cats_bp.route('/cats/<cat_id>', methods=['DELETE'])
def delete_cat(cat_id):
    try:
        # Buscar o gato pelo ID
        cat = Cats.query.filter_by(cat_id=cat_id).first()
        if not cat:
            return gerar_response(
                404,
                'Cat',
                {},
                'Cat not found'
            )
        db.session.delete(cat)
        db.session.commit()
        return gerar_response(
            200,
            'Cat',
            {},
            'Cat deleted successfully'
        )
    except Exception as e:
        db.session.rollback()
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error deleting cat: {str(e)}'
        )

# Filtro para varias descrições
@cats_bp.route('/cats/filter', methods=['GET'])
def filter_cats():
    try:
        # Obtendo parâmetros opcionais da query string
        # Nome do gato
        cat_name = request.args.get('cat_name', type=str)
        # Idade do gato
        cat_age = request.args.get('cat_age', type=str)
        # Cor do gato
        cat_color = request.args.get('cat_color', type=str)
        # URL da imagem
        cat_image_url = request.args.get('cat_image_url', type=str)
        # Se está adotado
        cat_adopted = request.args.get('cat_adopted', type=lambda x: (str(x).lower() == 'true'))
        # ID do adotante
        adopter_id = request.args.get('adopter_id', type=int)
        # Construindo a query com base nos filtros fornecidos
        query = Cats.query
        if cat_name is not None:
            query = query.filter_by(cat_name=cat_name)
        if cat_age is not None:
            query = query.filter_by(cat_age=cat_age)
        if cat_color is not None:
            query = query.filter_by(cat_color=cat_color)
        if cat_image_url is not None:
            query = query.filter_by(cat_image_url=cat_image_url)
        if cat_adopted is not None:
            query = query.filter_by(cat_adopted=cat_adopted)
        if adopter_id is not None:
            query = query.filter_by(adopter_id=adopter_id)
        # Executa a query final
        cats = query.all()
        cats_json = [cat.to_json() for cat in cats]
        if not cats_json:
            return gerar_response(
                404,
                'Cat',
                {},
                'No cats found with the specified filters'
            )
        return gerar_response(
            200,
            'cats',
            cats_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'Cat',
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
