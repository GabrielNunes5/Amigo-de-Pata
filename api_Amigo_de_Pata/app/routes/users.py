from flask import Response, request, Blueprint
import json
from ..database import db
from ..models.users import Users

users_bp = Blueprint('users', __name__)


# Criar um novo usuário com a possibilidade de ser administrador
@users_bp.route('/users', methods=['POST'])
def post_user():
    body = request.get_json()

    try:
        existing_user = Users.query.filter_by(
            user_name=body['user_name']).first()
        if existing_user:
            return gerar_response(
                400,
                'User',
                {},
                'A user with this name already exists'
            )

        # Criando o objeto Users
        user = Users(
            user_name=body['user_name'],
            user_is_admin=body.get('user_is_admin', False)
        )
        user.set_password(body['user_password'])

        db.session.add(user)
        db.session.commit()
        return gerar_response(
            201,
            'user',
            user.to_json(),
            'User created successfully'
        )
    except Exception as e:
        return gerar_response(
            400,
            'User',
            {},
            f'Error creating user: {str(e)}'
        )


# Obter todos os usuários
@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = Users.query.all()
        users_json = [user.to_json() for user in users]

        return gerar_response(
            200,
            'users',
            users_json,
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'User',
            {},
            f'Error fetching users: {str(e)}'
        )


# Obter um usuário pelo ID
@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = Users.query.filter_by(user_id=user_id).first()
        if not user:
            return gerar_response(
                404,
                'User',
                {},
                f'No user found with id {user_id}'
            )

        return gerar_response(
            200,
            'user',
            user.to_json(),
            'ok'
        )
    except Exception as e:
        return gerar_response(
            400,
            'User',
            {},
            f'Error fetching user: {str(e)}'
        )


# Atualizar um usuário
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Users.query.filter_by(user_id=user_id).first()

    if not user:
        return gerar_response(
            404,
            'User',
            {},
            f'No user found with id {user_id}'
        )

    body = request.get_json()

    try:
        if 'user_name' in body:
            user.user_name = body['user_name']
        if 'user_password' in body:
            user.set_password(body['user_password'])

        db.session.commit()
        return gerar_response(
            200,
            'user',
            user.to_json(),
            'User updated successfully'
        )
    except Exception as e:
        db.session.rollback()  # Faz rollback em caso de erro
        return gerar_response(
            400,
            'User',
            {},
            f'Error updating user: {str(e)}'
        )


# Deletar um usuário
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.filter_by(user_id=user_id).first()

    if not user:
        return gerar_response(
            404,
            'User',
            {},
            f'No user found with id {user_id}'
        )

    try:
        db.session.delete(user)
        db.session.commit()
        return gerar_response(
            200,
            'User',
            {},
            'User deleted successfully'
        )
    except Exception as e:
        db.session.rollback()  # Faz rollback em caso de erro
        return gerar_response(
            400,
            'User',
            {},
            f'Error deleting user: {str(e)}'
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
