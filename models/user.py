import json
import bcrypt

from app import db

import utils.errors.errors_code as errors_code
import utils.validators.user_validator as validator

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
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
            self.name = new_data.get('name').strip()
        if new_data.get('email'):
            self.email = new_data.get('email').strip()
        if new_data.get('password'):
            self.password = bcrypt.hashpw(new_data.get('password').encode('utf-8'), bcrypt.gensalt())
        if new_data.get('role') is not None:
            self.role = int(new_data.get('role'))

    @staticmethod
    def from_json_to_model(json):
        return User(name=json.get('name').strip(), email=json.get('email').strip(), 
                    password=bcrypt.hashpw(json.get('password').encode('utf-8'), bcrypt.gensalt()), role=0)
