from flask import session

from datetime import datetime

from app import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    surname = db.Column(db.String(), nullable=False)
    photo = db.Column(db.String())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creation_date = db.Column(db.DateTime(), default=datetime.now())
    last_update_date = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, id=None, name=None, surname=None, photo=None, created_by=None,
                updated_by=None, creation_date=None, last_update_date=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.photo = photo
        self.created_by = created_by
        self.updated_by = updated_by
        self.creation_date = creation_date
        self.last_update_date = last_update_date

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'surname': self.surname,
            'photo': self.photo,
            'created_by': self.created_by
        }
    
    def update_customer_values(self, new_data):
        if new_data.get('name'):
            self.name = new_data.get('name').strip()
        if new_data.get('surname'):
            self.surname = new_data.get('surname').strip()
        self.updated_by = session['user_id']
        self.last_update_date = datetime.now()

    @staticmethod
    def from_json_to_model(json):
        return Customer(name=json.get('name'), surname=json.get('surname'), created_by=session['user_id'],
                        updated_by=session['user_id'])

