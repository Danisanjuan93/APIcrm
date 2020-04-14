import json
import bcrypt

from app import db

import utils.errors_code as errors_code
import utils.user_validator as validator

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.LargeBinary())
    role = db.Column(db.Integer())

    def __init__(self, id=None, name=None, email=None, password=None, role=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'email': self.email,
            'role': self.role
        }
    
    def update_user_values(self, new_data):
        if new_data.get('name'):
            self.name = new_data.get('name')
        if new_data.get('email'):
            self.email = new_data.get('email')
        if new_data.get('password'):
            if new_data.get('confirm_password'):
                validator.validate_password(new_data.get('password'), new_data.get('confirm_password'))
                self.password = bcrypt.hashpw(new_data.get('password').encode('utf-8'), bcrypt.gensalt())
            else:
                raise ValueError("To update user password should provide confirm_password", errors_code.USER_CONFIRM_PASSWORD_MANDATORY)
        if new_data.get('role'):
            self.role = validator.validate_role(new_data.get('role'))

    @staticmethod
    def from_json_to_model(json):
        return User(name=json.get('name'), email=json.get('email'), 
                    password=bcrypt.hashpw(json.get('password').encode('utf-8'), bcrypt.gensalt()), role=0)
