import os
import jwt
from datetime import datetime, timedelta
from environment import ENV

def encode_auth_token(user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                ENV.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, ENV.SECRET_KEY)
        return payload['sub']
    except Exception:
        return False
