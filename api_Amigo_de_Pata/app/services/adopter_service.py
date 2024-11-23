# from flask import request
from ..models.adopter import Adopter
from ..database import db
from ..utils.response import gerar_response


def get_all_adopters():
    try:
        # Recupera todos os adotantes e os converte para JSON
        adopters = Adopter.query.all()
        adopters_json = [adopter.to_json() for adopter in adopters]
        return gerar_response(200,
                              'adopters',
                              adopters_json,
                              'ok')
    except Exception as e:
        return gerar_response(400,
                              'Adopter',
                              {},
                              str(e))


def get_adopter_filter():
    ...


def create_adopter(data):
    try:
        # Criar o novo adotante com os campos fornecidos
        adopter = Adopter(
            adopter_full_name=data.get('adopter_full_name'),
            adopter_age=data.get('adopter_age'),
            adopter_email=data.get('adopter_email'),
            adopter_phone=data.get('adopter_phone'),
            adopter_address=data.get('adopter_address'),
            adopter_residence_type=data.get('adopter_residence_type'),
            adopter_has_garden=data.get('adopter_has_garden'),
            adopter_other_pets=data.get('adopter_other_pets'),
            adopter_pet_type=data.get('adopter_pet_type'),
            adopter_pet_preference=data.get('adopter_pet_preference'),
            adopter_occupation=data.get('adopter_occupation'),
            adopter_work_hours=data.get('adopter_work_hours'),
            adopter_income=data.get('adopter_income'),
            adopter_adoption_reason=data.get('adopter_adoption_reason'),
            adopter_commitment_to_care=data.get('adopter_commitment_to_care'),
            adopter_experience_with_pets=data.get(
                'adopter_experience_with_pets'),
            adopter_additional_info=data.get('adopter_additional_info'),
        )

        # Salvar o novo adotante no banco de dados
        db.session.add(adopter)
        db.session.commit()

        # Retornar sucesso
        return gerar_response(201,
                              'adopter',
                              adopter.to_json(),
                              'Adopter created successfully')

    except Exception as e:
        # Rollback em caso de erro
        db.session.rollback()
        return gerar_response(400,
                              'adopter',
                              {},
                              str(e))


def update_adopter(adopter_id, data):
    ...


def delete_adopter(adopter_id):
    try:
        adopter = Adopter.query.get(adopter_id)
        if not adopter:
            return gerar_response(404,
                                  'adopter',
                                  {},
                                  'Adopter not found')

        db.session.delete(adopter)
        db.session.commit()
        return gerar_response(200,
                              'adopter',
                              {},
                              'Adopter deleted successfully')

    except Exception as e:
        db.session.rollback()
        return gerar_response(400,
                              'adopter',
                              {},
                              str(e))
