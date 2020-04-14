import re

import utils.errors_code as errors_code
from utils.auth import USER_ACCESS_ROLES

def user_required_fields_validator(user_json):
    user_json_keys = user_json.keys()

    if 'name' not in user_json_keys:
        raise ValueError("Field name is required to register new user", errors_code.USER_NAME_MANDATORY)
    if 'email' not in user_json_keys or not validate_email(user_json.get('email')):
        raise ValueError("Field email is required to register new user and should be a valid email", errors_code.USER_EMAIL_MANDATORY)
    if 'password' not in user_json_keys:
        raise ValueError("Field password is required to register new user", errors_code.USER_PASSWORD_MANDATORY)
    if 'confirm_password' not in user_json_keys:
        raise ValueError("Field confirm_password is required to register new user", errors_code.USER_CONFIRM_PASSWORD_MANDATORY)
    
    validate_password(user_json.get('password'), user_json.get('confirm_password'))

def login_user_required_fields_validator(user_json):
    user_json_keys = user_json.keys()

    if 'email' not in user_json_keys or not validate_email(user_json.get('email')):
        raise ValueError("Field email is required to register new user and should be a valid email", errors_code.USER_EMAIL_MANDATORY)
    if 'password' not in user_json_keys:
        raise ValueError("Field confirm_password is required to register new user", errors_code.USER_CONFIRM_PASSWORD_MANDATORY)
    
def validate_email(email):
    if email is None or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    
    return True

def validate_password(password, confirm_password):
    if password is None or confirm_password is None or len(password) < 8 or len(confirm_password) < 8:
        raise ValueError("Password must not be empty values. Minimal 8 characters", errors_code.VALIDATION_INVALID_PASSWORD_LENGTH)
    if password != confirm_password:
        raise ValueError("Passwords does not match", errors_code.VALIDATION_INVALID_PASSWORD_MATCH)

def validate_role(role):
    if role not in USER_ACCESS_ROLES.values():
        raise ValueError("Not enough permissions", 403)
    return role
