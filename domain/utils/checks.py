def check_type(name, value, expected_type):
    if not isinstance(value, expected_type):
        error_msg = f"{name} must be of type {expected_type.__name__}"
        error_msg += f", got {type(value).__name__}"
        raise TypeError(error_msg)
