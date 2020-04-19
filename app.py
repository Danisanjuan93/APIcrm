import os
import jwt

from flask import Flask, request, g, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth


app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Token')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import controllers.user as user_controller
import controllers.customer as customer_controller

import utils.auth.auth_utils as auth_utils
from utils.errors.error_manager import return_error_code

@auth.verify_token
def verify_token(token):
    user_id = auth_utils.decode_auth_token(token)
    if not user_id:    
        return False

    response = user_controller.get_user_by_id(user_id)
    
    if response[1] == 200:
        user_decoded = json.loads(response[0].response[0].decode("UTF-8"))
        session['user_id'] = int(user_decoded['id'])
        session['role'] = int(user_decoded['role'])
        return True
    else:
        return False

@auth.error_handler
def auth_error():
    return jsonify({'status': 'error', 'message': 'Invalid token provided. Acces Denied'}), 401


@app.route("/user", methods=["GET"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['admin']])
def get_users():
    try:
        users = user_controller.get_all_users()
        return users
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/user/<id>", methods=["GET"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['admin']])
def get_user_by_id(id):
    try:
        user = user_controller.get_user_by_id(id)
        return user
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/user", methods=["PUT"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['admin']])
def update_user():
    try:
        response = user_controller.update_user(request.json)
        return response
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/user/register", methods=["POST"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['admin']])
def register_user():
    try:
        response = user_controller.register_new_user(request.json)
        return response
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/user/<user_id>", methods=["DELETE"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['admin']])
def delete_user(user_id):
    try:
        response = user_controller.delete_user(user_id)
        return response
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/user/status", methods=["PUT"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['admin']])
def change_user_status():
    try:
        response = user_controller.change_user_status(request.json)
        return response
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/user/login", methods=["POST"])
def login_user():
    try:
        response = user_controller.login_user(request.json)
        return response
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/customer", methods=["GET"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['user'], auth_utils.USER_ACCESS_ROLES['admin']])
def get_customers():
    try:
        customers = customer_controller.get_all_customer()
        return customers
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/customer/<id>", methods=["GET"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['user'], auth_utils.USER_ACCESS_ROLES['admin']])
def get_customer_by_id(id):
    try:
        customer = customer_controller.get_customer_by_id(id)
        return customer
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/customer", methods=["POST"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['user'], auth_utils.USER_ACCESS_ROLES['admin']])
def create_new_customer():
    try:
        response = customer_controller.create_new_customer(request.json)
        return response
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/customer", methods=["PUT"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['user'], auth_utils.USER_ACCESS_ROLES['admin']])
def update_customer():
    try:
        response = customer_controller.update_customer(request.json)
        return response
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400

@app.route("/customer/<user_id>", methods=["DELETE"])
@auth.login_required
@auth_utils.requires_access_level([auth_utils.USER_ACCESS_ROLES['user'], auth_utils.USER_ACCESS_ROLES['admin']])
def delete_customer(user_id):
    try:
        response = customer_controller.delete_customer(user_id)
        return response
    except Exception as exception:
        return jsonify(return_error_code(exception)), 400


if __name__ == '__main__':
    app.run()