import re

import utils.errors.errors_code as errors_code
from utils.auth.auth_utils import USER_ACCESS_ROLES
import utils.validators.general_validator as validator

def login_user_fields_validator(user_json):
    if not validator.validate_string(user_json.get('email')) or not validator.validate_email(user_json.get('email')):
        raise ValueError("Field email is required to register new user and should be a valid email", errors_code.USER_EMAIL_MANDATORY)
    if not validator.validate_string(user_json.get('password')):
        raise ValueError("Field password is required to register new user", errors_code.USER_CONFIRM_PASSWORD_MANDATORY)

def get_user_by_id_fields_validator(user_id):
    if not validator.validate_integer(user_id):
        raise ValueError("Field id is required to get an user by id and should be a valid integer")

def new_user_fields_validator(user_json):
    if not validator.validate_string(user_json.get('name')):
        raise ValueError("Field name is required to register new user and must be a valid string", errors_code.USER_NAME_MANDATORY)

    if not validator.validate_string(user_json.get('email')) or not validator.validate_email(user_json.get('email')):
        raise ValueError("Field email is required to register new user and should be a valid email", errors_code.USER_EMAIL_MANDATORY)

    if not validator.validate_string(user_json.get('password')):
        raise ValueError("Field password is required to register new user and must be a valid string", errors_code.USER_PASSWORD_MANDATORY)

    if not validator.validate_string(user_json.get('confirm_password')):
        raise ValueError("Field confirm_password is required to register new user and must be a valid string", errors_code.USER_CONFIRM_PASSWORD_MANDATORY)
    
    validator.validate_password(user_json.get('password'), user_json.get('confirm_password'))

def update_user_fields_validator(user_json):
    if not user_json.get('id'):
        raise ValueError("Field id is required to update an user", errors_code.USER_ID_MANDATORY)

    if not validator.validate_string(user_json.get('name'), nullable=True):
        raise ValueError("Field name should be a valid string", errors_code.VALIDATION_INVALID_STRING)

    if not validator.validate_string(user_json.get('email'), nullable=True) or not validator.validate_email(user_json.get('email'), nullable=True):
        raise ValueError("Field email should be a valid email", errors_code.VALIDATION_INVALID_EMAIL)

    if not validator.validate_string(user_json.get('password'), nullable=True if user_json.get('confirm_password') is None else False):
        raise ValueError("Field password should be a valid string and is required if confirm_password field is sent", errors_code.VALIDATION_INVALID_PASSWORD)

    if not validator.validate_string(user_json.get('confirm_password'), nullable=True if user_json.get('password') is None else False):
        raise ValueError("Field confirm_password should be a valid string and is required to update user password", errors_code.VALIDATION_INVALID_CONFIRM_PASSWORD)
    
    if not validator.validate_integer(user_json.get('role'), nullable=True) or not validator.validate_role(user_json.get('role'), nullable=True):
        raise ValueError("Field role should be a valid role", errors_code.VALIDATION_INVALID_ROLE)

    validator.validate_password(user_json.get('password'), user_json.get('confirm_password'), nullable=True)

def delete_user_fields_validator(user_id):
    if not validator.validate_integer(user_id):
        raise ValueError("Field id is required to delete an user and should be a valid integer")

def change_status_fields_validator(user_json):
    if not validator.validate_integer(user_json.get('id')):
        raise ValueError("Field id is required to change user status and should be a valid integer")
    
    if not validator.validate_integer(user_json.get('role')) or not validator.validate_role(user_json.get('role')):
        raise ValueError("Field role is required and should be a valid role", errors_code.VALIDATION_INVALID_ROLE)

