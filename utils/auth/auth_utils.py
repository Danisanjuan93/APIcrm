import os
from functools import wraps
import jwt
from flask import session, jsonify
from datetime import datetime, timedelta

from utils.errors.error_manager import return_error_code
import utils.errors.errors_code as errors_code

USER_ACCESS_ROLES = {
    'user': 0,
    'admin': 1
}

def encode_auth_token(user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.environ['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, os.environ['SECRET_KEY'])
        return payload['sub']
    except Exception:
        return False

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for role in access_level:
                if session.get('role') == role:
                    break
            else:
                return jsonify({"error": errors_code.NOT_ENOUGH_PERMISSIONS, "msg": "Not enough permissions"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
