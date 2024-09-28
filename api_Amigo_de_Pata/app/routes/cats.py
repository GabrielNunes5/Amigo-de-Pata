from flask import Response, request, Blueprint
import json
from ..database import db
from ..models.cats import Cats

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


# Filtrar um gato por nome do DB
@cats_bp.route('/cats/name/<string:cat_name>', methods=['GET'])
def get_cat_name(cat_name):

    try:
        cat = Cats.query.filter_by(cat_name=cat_name).first()
        cat_json = cat.to_json()

        return gerar_response(
            200,
            'cat',
            cat_json,
            'ok')

    except Exception as e:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error: {str(e)}'
        )


# Filtrar um gato por idade do DB
@cats_bp.route('/cats/age/<int:cat_age>', methods=['GET'])
def get_cat_age(cat_age):

    try:
        cats = Cats.query.filter_by(cat_age=cat_age).all()
        cats_json = [cat.to_json() for cat in cats]

        return gerar_response(
            200,
            'cat',
            cats_json,
            'ok')

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
                'A cat with this name already exists')

        # Criando o objeto Cats com os campos corretos
        cat = Cats(cat_name=body['cat_name'],
                   cat_age=int(body['cat_age']),
                   cat_image_url=body['cat_image_url'],
                   cat_color=body['cat_color']
                   )

        db.session.add(cat)
        db.session.commit()
        return gerar_response(
            201,
            'cat',
            cat.to_json(),
            'cat created successfully')
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
    cat = Cats.query.filter_by(cat_id=cat_id).first()
    body = request.get_json()

    try:
        if 'cat_adopted' in body:
            cat.cat_adopted = body['cat_adopted']
        if 'cat_adopter_id' in body:
            cat.cat_adopter_id = body['cat_adopter_id']

        db.session.add(cat)
        db.session.commit()
        return gerar_response(
            200,
            'cat',
            cat.to_json(),
            'cat updated successfully')
    except Exception as e:
        return gerar_response(
            400,
            'Cat',
            {},
            f'Error updating cat: {str(e)}'
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