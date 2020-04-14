from app import db

from models.customer import Customer
import utils.customer_validator as customer_validator
import utils.errors_code as errors_code
from utils.photo_utils import upload_customer_photo

def get_all_customer():
    customers = db.session.query(Customer)

    result = []

    for customer in customers:
        result.append(customer.serialize())
    
    return result

def create_new_customer(customer_json):
    customer_validator.customer_required_fields_validator(customer_json)

    #TODO: photo
    customer = Customer.from_json_to_model(customer_json)

    db.session.add(customer)
    db.session.commit()

def update_customer(customer_json):
    customer = db.session.query(Customer).filter(Customer.id == customer_json.get('id')).first()

    if not customer:
        raise ValueError("Customer does not exists", errors_code.CUSTOMER_DOES_NOT_EXISTS)
    
    #TODO: photo
    customer.update_customer_values(customer_json)

    db.session.commit()

def delete_customer(customer_id):
    customer = db.session.query(Customer).filter(Customer.id == customer_id.get('id')).first()

    if not customer:
        raise ValueError("Customer does not exists", errors_code.CUSTOMER_DOES_NOT_EXISTS)

    db.session.delete(customer)
    db.session.commit()