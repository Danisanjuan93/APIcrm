from app import db

from models.user import User
from models.customer import Customer
import utils.validators.customer_validator as customer_validator
import utils.errors.errors_code as errors_code
from utils.bucket.photo_utils import upload_customer_photo

def get_all_customer():
    customers = db.session.query(Customer).all()

    result = []

    for customer in customers:
        result.append(customer.serialize())
    
    return result

def get_customer_by_id(id):
    customer_validator.get_customer_by_id_fields_validator(id)

    customer = db.session.query(Customer).filter(Customer.id == id).first()

    if not customer:
        raise ValueError("Customer does not exists", errors_code.CUSTOMER_DOES_NOT_EXISTS)
    
    created_by = db.session.query(User).filter(User.id == customer.created_by).first()
    updated_by = db.session.query(User).filter(User.id == customer.updated_by).first()

    if created_by:
        customer.created_by = created_by

    if updated_by:
        customer.updated_by = updated_by

    return customer.serialize()

def create_new_customer(customer_json):
    customer_validator.new_customer_fields_validator(customer_json)

    customer = Customer.from_json_to_model(customer_json)

    db.session.add(customer)
    db.session.flush()

    photo = customer_json.get('photo')
    if photo:
        customer.photo = upload_customer_photo(customer, photo)

    db.session.commit()

def update_customer(customer_json):
    customer_validator.update_customer_fields_validator(customer_json)

    customer = db.session.query(Customer).filter(Customer.id == customer_json.get('id')).first()

    if not customer:
        raise ValueError("Customer does not exists", errors_code.CUSTOMER_DOES_NOT_EXISTS)
    
    photo = customer_json.get('photo')
    if photo:
        customer.photo = upload_customer_photo(customer, photo)

    customer.update_customer_values(customer_json)

    db.session.commit()

def delete_customer(customer_id):
    customer_validator.delete_customer_fields_validator(customer_id)

    customer = db.session.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise ValueError("Customer does not exists", errors_code.CUSTOMER_DOES_NOT_EXISTS)

    db.session.delete(customer)
    db.session.commit()