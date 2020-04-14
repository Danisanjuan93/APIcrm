
import utils.errors_code as errors_code

def customer_required_fields_validator(customer_json):
    customer_json_keys = customer_json.keys()

    if 'name' not in customer_json_keys:
        raise ValueError("Field name is mandatory", errors_code.CUSTOMER_NAME_MANDATORY)
    
    if 'surname' not in customer_json_keys:
        raise ValueError("Field surname is mandatory", errors_code.CUSTOMER_SURNAME_MANDATORY)
    