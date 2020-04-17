from flask import jsonify, session
import bcrypt

from app import db

from models.user import User
from models.customer import Customer

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

def get_user_by_id(user_id):
    user_validator.get_user_by_id_fields_validator(user_id)

    return db.session.query(User).filter(User.id == user_id).first()

def register_new_user(user_json):
    user_validator.new_user_fields_validator(user_json)

    user = db.session.query(User).filter(User.email == user_json.get("email")).first()

    if user:
        return error_manager.return_error_code(ValueError("User already exists", errors_code.USER_ALREADY_EXISTS)), 409

    new_user = User.from_json_to_model(user_json)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "ok", "message": "User created"}), 200

def update_user(user_json):
    user_validator.update_user_fields_validator(user_json)

    user = db.session.query(User).filter(User.id == user_json.get('id')).first()

    if not user:
        return error_manager.return_error_code(ValueError("User does not exists", errors_code.USER_DOES_NOT_EXISTS)), 404

    user.update_user_values(user_json)

    db.session.commit()

    return jsonify({"status": "ok", "message": "User updated"}), 200

def delete_user(user_id):
    user_validator.delete_user_fields_validator(user_id)

    user = db.session.query(User).filter(User.id == user_id).first()

    if not user:
        return error_manager.return_error_code(ValueError("User does not exists", errors_code.USER_DOES_NOT_EXISTS)), 404


    customers_created_by = db.session.query(Customer).filter(Customer.created_by == user.id).all()
    customers_updated_by = db.session.query(Customer).filter(Customer.updated_by == user.id).all()

    for customer in customers_created_by:
        customer.created_by = 0
    
    for customer in customers_updated_by:
        customer.updated_by = 0
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"status": "ok", "message": "User deleted"}), 200

def login_user(user_json):
    user_validator.login_user_fields_validator(user_json)

    user = db.session.query(User).filter(User.email == user_json.get("email")).first()

    if not user or not bcrypt.checkpw(user_json.get('password').encode('utf-8'), user.password):
        return error_manager.return_error_code(ValueError("User or password are invalids", errors_code.VALIDATION_INVALID_PASSWORD_MATCH)), 409

    return [auth_utils.encode_auth_token(user.id).decode("utf-8"), user.email, user.role]

def change_user_status(user_json):
    user_validator.change_status_fields_validator(user_json)

    user = db.session.query(User).filter(User.id == user_json.get('id')).first()

    if not user:
        return error_manager.return_error_code(ValueError("User does not exists", errors_code.USER_DOES_NOT_EXISTS)), 404

    user.update_user_values(user_json)

    db.session.commit()

    session['role'] = user.role

    return jsonify({"status": "ok", "message": "User role updated"}), 200
