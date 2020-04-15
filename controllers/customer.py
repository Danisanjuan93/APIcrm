from app import db

from models.customer import Customer
import utils.validators.customer_validator as customer_validator
import utils.errors.errors_code as errors_code
from utils.bucket.photo_utils import upload_customer_photo

def get_all_customer():
    customers = db.session.query(Customer)

    result = []

    for customer in customers:
        result.append(customer.serialize())
    
    return result

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