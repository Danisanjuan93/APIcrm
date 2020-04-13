ERROR_KEY = "error"
ERROR_MSG = "msg"

def return_error_code(error):
    if len(error.args) > 1 and isinstance(error.args[1], int):
        return {ERROR_KEY: error.args[1],
                ERROR_MSG: error.args[0]}
    elif len(error.args) > 0 and isinstance(error.args[0], str):
        return {ERROR_KEY: None,
                ERROR_MSG: error.args[0]}
    else:
        return {ERROR_KEY: None,
                ERROR_MSG: None}