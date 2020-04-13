import os
import jwt

from flask import Flask, request, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth

from environment import ENV
import utils.auth as auth_utils

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Token')

app.config.from_object(ENV.APP_SETTINGS)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@auth.verify_token
def verify_token(token):
    user_id = auth_utils.decode_auth_token(token)
    if not user_id:
        return False
    return True

@auth.error_handler
def auth_error():
    return jsonify({'status': 'error', 'message': 'Invalid token provided. Acces Denied'}), 401

@app.route("/", methods=["GET"])
def home():
    return "Api Home"


if __name__ == '__main__':
    app.run()