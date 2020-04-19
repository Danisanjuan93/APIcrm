import base64

import utils.errors.errors_code as errors_code
import utils.validators.general_validator as validator


def get_customer_by_id_fields_validator(customer_id):
    if not validator.validate_integer(customer_id):
        raise ValueError("Field id is required to get a customer and should be a valid integer")

def new_customer_fields_validator(customer_json):
    if not validator.validate_string(customer_json.get('name')):
        raise ValueError("Field name is mandatory and must be a valid string", errors_code.CUSTOMER_NAME_MANDATORY)
    
    if not validator.validate_string(customer_json.get('surname')):
        raise ValueError("Field surname is mandatory and must be a valid string", errors_code.CUSTOMER_SURNAME_MANDATORY)
    
    if not validator.validate_base64(customer_json.get('photo'), nullable=True):
        raise ValueError("Field photo must be a valid base64 string", errors_code.VALIDATION_INVALID_BASE64)

def update_customer_fields_validator(customer_json):
    if not customer_json.get('id'):
        raise ValueError("Field id is required to update a customer", errors_code.CUSTOMER_ID_MANDATORY)

    if not validator.validate_string(customer_json.get('name'), nullable=True):
        raise ValueError("Field name is mandatory or must be a valid string", errors_code.CUSTOMER_NAME_MANDATORY)
    
    if not validator.validate_string(customer_json.get('surname'), nullable=True):
        raise ValueError("Field surname is mandatory or must be a valid string", errors_code.CUSTOMER_SURNAME_MANDATORY)
    
    if not validator.validate_base64(customer_json.get('photo'), nullable=True):
        raise ValueError("Field photo must be a valid base64 string", errors_code.VALIDATION_INVALID_BASE64)

def delete_customer_fields_validator(customer_id):
    if not validator.validate_integer(customer_id):
        raise ValueError("Field id is required to delete a customer and should be a valid integer")


