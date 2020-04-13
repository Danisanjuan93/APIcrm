import bcrypt

from app import db

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
            'role': self.role,
            'password': self.password
        }
    
    @staticmethod
    def from_json_to_model(json):
        return User(name=json.get('name'), email=json.get('email'), 
                    password=bcrypt.hashpw(json.get('password').encode('utf-8'), bcrypt.gensalt()), role=0)
