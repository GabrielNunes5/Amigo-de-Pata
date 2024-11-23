from flask import request
from ..models.animals import Animals
# from ..models.adopter import Adopter
from ..database import db
from ..utils.response import gerar_response


def get_all_animals():
    try:
        animals = Animals.query.all()
        animals_json = [animal.to_json() for animal in animals]
        return gerar_response(200,
                              'animals',
                              animals_json,
                              'ok')
    except Exception as e:
        return gerar_response(400,
                              'animals',
                              {},
                              str(e))


def get_animal_filter():
    try:
        # Obtendo parâmetros opcionais da query string
        filters = {
            "animal_id": request.args.get('animal_id', type=int),
            "animal_name": request.args.get('animal_name', type=str),
            "animal_age": request.args.get('animal_age', type=str),
            "animal_weight": request.args.get('animal_weight', type=float),
            "animal_num_age": request.args.get('animal_num_age', type=str),
            "animal_sex": request.args.get('animal_sex', type=str),
            "animal_color": request.args.get('animal_color', type=str),
            "animal_species": request.args.get('animal_species', type=str),
            "animal_vaccines": request.args.get('animal_vaccines', type=str),
            "animal_sized": request.args.get('animal_sized', type=str),
            "animal_neutered": request.args.get(
                'animal_neutered', type=lambda x: str(x).lower() == 'true'
            ),
            "animal_special_conditions": request.args.get(
                'animal_special_conditions', type=str
            ),
            "animal_category": request.args.get('animal_category', type=str),
            "animal_adopted": request.args.get(
                'animal_adopted', type=lambda x: str(x).lower() == 'true'
            ),
            "adopter_id": request.args.get('adopter_id', type=int),
        }

        # Filtrando apenas os filtros não-nulos
        query = Animals.query
        for key, value in filters.items():
            if value is not None:
                query = query.filter(getattr(Animals, key) == value)

        # Executando a query
        animals = query.all()
        animals_json = [animal.to_json() for animal in animals]

        if not animals_json:
            return gerar_response(
                404,
                'animals',
                {},
                'No animals found with the specified filters'
            )

        return gerar_response(200,
                              'animals',
                              animals_json,
                              'Filtered animals retrieved successfully')

    except Exception as e:
        return gerar_response(400,
                              'animals',
                              {},
                              str(e))


def create_animal(data):
    try:
        # Criar o novo animal com os campos fornecidos
        animal = Animals(
            animal_name=data.get('animal_name'),
            animal_age=data.get('animal_age'),
            animal_image_url=data.get('animal_image_url'),
            animal_color=data.get('animal_color'),
            animal_weight=data.get('animal_weight'),
            animal_num_age=data.get('animal_num_age'),
            animal_sex=data.get('animal_sex'),
            animal_species=data.get('animal_species'),
            animal_vaccines=data.get('animal_vaccines'),
            animal_sized=data.get('animal_sized'),
            animal_neutered=data.get('animal_neutered', False),
            animal_special_conditions=data.get('animal_special_conditions'),
            animal_category=data.get('animal_category'),
            animal_adopted=data.get('animal_adopted', False),
            adopter_id=data.get('adopter_id')
        )

        # Salvar o novo animal no banco de dados
        db.session.add(animal)
        db.session.commit()

        # Retornar sucesso
        return gerar_response(201,
                              'animal',
                              animal.to_json(),
                              'Animal created successfully')

    except Exception as e:
        # Rollback em caso de erro
        db.session.rollback()
        return gerar_response(400,
                              'animal',
                              {},
                              f'Error: {str(e)}')


def update_animal(animal_id, data):
    try:
        animal = Animals.query.get(animal_id)
        if not animal:
            return gerar_response(404,
                                  'animal',
                                  {},
                                  'Animal not found')

        if 'animal_adopted' in data:
            animal.animal_adopted = data['animal_adopted']
        db.session.commit()
        return gerar_response(200,
                              'animal',
                              animal.to_json(),
                              'Animal updated successfully')
    except Exception as e:
        db.session.rollback()
        return gerar_response(400,
                              'animal',
                              {},
                              str(e))


def delete_animal(animal_id):
    try:
        animal = Animals.query.get(animal_id)
        if not animal:
            return gerar_response(
                404,
                'animal',
                {},
                'Animal not found'
            )

        db.session.delete(animal)
        db.session.commit()
        return gerar_response(
            200,
            'animal',
            {},
            'Animal deleted successfully')
    except Exception as e:
        db.session.rollback()
        return gerar_response(
            400,
            'animal',
            {},
            str(e)
        )
