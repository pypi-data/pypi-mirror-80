def validate_type_str(val):
    return isinstance(val, str)

def validate_size_string(val):
    try:
        if len(val) <= 10:
            return True
    except TypeError as e:
        return False
    return len(val) <= 10