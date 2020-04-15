import re
import base64

import utils.errors.errors_code as errors_code
from utils.auth.auth_utils import USER_ACCESS_ROLES

def validate_integer(value, nullable=False):
    try:
        if (value is None and nullable) or int(value):
            return True
        
        if (value is None and not nullable) or not isinstance(value, int):
            return False
    except Exception as exception:
        return False
    return True

def validate_string(value, nullable=False):
    if value is None and nullable:
        return True

    if (value is None and not nullable) or not isinstance(value, str) or len(value.strip()) < 3:
        return False
    return True

def validate_base64(value, nullable=False):
    try:
        if value is None and nullable:
            return True

        base64.b64decode(value)
    except Exception as exception:
        return False
    return True

def validate_email(value, nullable=False):
    if value is None and nullable:
        return True
    if value is None or not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        return False
    return True

def validate_password(password, confirm_password, nullable=False):
    if (password is None or confirm_password is None) and nullable:
        return True
    if ((password is None or confirm_password is None) and not nullable) or len(password) < 8 or len(confirm_password) < 8:
        raise ValueError("Password must not be empty values. Minimal 8 characters", errors_code.VALIDATION_INVALID_PASSWORD_LENGTH)
    if password != confirm_password:
        raise ValueError("Passwords does not match", errors_code.VALIDATION_INVALID_PASSWORD_MATCH)

def validate_role(role, nullable=False):
    if role is None and nullable:
        return True
    if (role is None and not nullable) or int(role) not in USER_ACCESS_ROLES.values():
        return False
    return True
