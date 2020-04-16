from flask import jsonify
import bcrypt

from app import db

from models.user import User

import utils.validators.user_validator as user_validator
import utils.errors.errors_code as errors_code
import utils.auth.auth_utils as auth_utils
import utils.errors.error_manager as error_manager

def get_all_users():
    users = db.session.query(User).all()

    result = []

    for user in users:
        result.append(user.serialize())

    return jsonify(result), 200

def register_new_user(user_json):
    user_validator.new_user_fields_validator(user_json)

    user = db.session.query(User).filter(User.email == user_json.get("email")).first()

    if user:
        error_manager.return_error_code(ValueError("User already exists", errors_code.USER_ALREADY_EXISTS)), 409

    new_user = User.from_json_to_model(user_json)

    db.session.add(new_user)
    db.session.commit()

def update_user(user_json):
    user_validator.update_user_fields_validator(user_json)

    user = db.session.query(User).filter(User.id == user_json.get('id')).first()

    if not user:
        error_manager.return_error_code(ValueError("User does not exists", errors_code.USER_DOES_NOT_EXISTS)), 404

    user.update_user_values(user_json)

    db.session.commit()

def delete_user(user_id):
    user_validator.delete_user_fields_validator(user_id)

    user = db.session.query(User).filter(User.id == user_id).first()

    if not user:
        error_manager.return_error_code(ValueError("User does not exists", errors_code.USER_DOES_NOT_EXISTS)), 404

    db.session.delete(user)
    db.session.commit()

def login_user(user_json):
    user_validator.login_user_fields_validator(user_json)

    user = db.session.query(User).filter(User.email == user_json.get("email")).first()

    if not user or not bcrypt.checkpw(user_json.get('password').encode('utf-8'), user.password):
        error_manager.return_error_code(ValueError("User or password are invalids", errors_code.VALIDATION_INVALID_PASSWORD_MATCH)), 409

    return [auth_utils.encode_auth_token(user.id).decode("utf-8"), user.email, user.role]

def change_user_status(user_json):
    user_validator.change_status_fields_validator(user_json)

    user = db.session.query(User).filter(User.id == user_json.get('id')).first()

    if not user:
        error_manager.return_error_code(ValueError("User does not exists", errors_code.USER_DOES_NOT_EXISTS)), 404

    user.update_user_values(user_json)

    db.session.commit()
