import string
from config import PASSWORD_STRENGTH


def check_password_strength(password):
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    variety = sum([has_lower, has_upper, has_digit, has_symbol])

    if length < 8 or variety < 2:
        return PASSWORD_STRENGTH['weak']
    elif length < 10 or (variety < 3 and length < 12):
        return PASSWORD_STRENGTH['medium']
    elif length >= 12 and variety >= 3:
        if length >= 16 and variety == 4:
            return PASSWORD_STRENGTH['very_strong']
        return PASSWORD_STRENGTH['strong']
    else:
        return PASSWORD_STRENGTH['medium']


def check_common_patterns(password):
    common_patterns = ['123', 'qwerty', 'password', 'admin', '111']
    return any(pattern in password.lower() for pattern in common_patterns)