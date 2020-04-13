import os
import jwt

from flask import Flask, request, g, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth

from environment import ENV



app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Token')

app.config.from_object(ENV.APP_SETTINGS)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models.user import User

import controllers.user as user_controller

import utils.auth as auth_utils
from utils.error_manager import return_error_code

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

@app.route("/user", methods=["GET"])
@auth_utils.requires_access_level(auth_utils.USER_ACCESS_ROLES['user'])
def get_users():
    try:
        users = user_controller.get_all_users()
        return jsonify(users), 200
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/user", methods=["PUT"])
@auth_utils.requires_access_level(auth_utils.USER_ACCESS_ROLES['user'])
def update_user():
    try:
        user_controller.update_user(request.json)
        return jsonify({"status": "ok", "message": "User updated"}), 200
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/user/register", methods=["POST"])
@auth_utils.requires_access_level(auth_utils.USER_ACCESS_ROLES['user'])
def register_user():
    try:
        user_controller.register_new_user(request.json)
        return jsonify({"status": "ok", "message": "User created"}), 200
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/user", methods=["DELETE"])
@auth_utils.requires_access_level(auth_utils.USER_ACCESS_ROLES['user'])
def delete_user():
    try:
        user_controller.delete_user(request.json)
        return jsonify({"status": "ok", "message": "User deleted"}), 200
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/user/login", methods=["POST"])
def login_user():
    try:
        token, email, role = user_controller.login_user(request.json)
        session['email'] = email
        session['role'] = role
        return jsonify({"token": token}), 200
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

if __name__ == '__main__':
    app.run()