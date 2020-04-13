import bcrypt

from app import db

from models.user import User

import utils.user_validator as user_validator
import utils.errors_code as errors_code
import utils.auth as auth

def get_all_users():
    users = db.session.query(User).all()

    result = []

    for user in users:
        result.append(user.serialize())

    return result

def register_new_user(user_json):
    user_validator.user_required_fields_validator(user_json)

    user = db.session.query(User).filter(User.email == user_json.get("email")).first()

    if user:
        raise ValueError("User already exists", errors_code.USER_ALREADY_EXISTS)

    new_user = User.from_json_to_model(user_json)

    db.session.add(new_user)
    db.session.commit()

def update_user(user_json):
    user = db.session.query(User).filter(User.email == user_json.get('email')).first()

    if not user:
        raise ValueError("User does not exists", errors_code.USER_DOES_NOT_EXISTS)

    user.update_user_values(user_json)

    db.session.commit()

def delete_user(user_json):
    user = db.session.query(User).filter(User.email == user_json.get('email')).first()

    if not user:
        raise ValueError("User does not exists", errors_code.USER_DOES_NOT_EXISTS)

    db.session.delete(user)
    db.session.commit()

def login_user(user_json):
    user_validator.login_user_required_fields_validator(user_json)

    user = db.session.query(User).filter(User.email == user_json.get("email")).first()

    if not user or not bcrypt.checkpw(user_json.get('password').encode('utf-8'), user.password):
        raise ValueError("User or password are invalids", errors_code.VALIDATION_INVALID_PASSWORD_MATCH)

    return [auth.encode_auth_token(user.id).decode("utf-8"), user.email, user.role]
