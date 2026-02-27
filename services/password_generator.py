import secrets
import string
from config import DEFAULT_SETTINGS


def generate_password(settings=None):
    if settings is None:
        settings = DEFAULT_SETTINGS.copy()
    chars = ''
    if settings['use_lower']:
        chars += string.ascii_lowercase
    if settings['use_upper']:
        chars += string.ascii_uppercase
    if settings['use_digits']:
        chars += string.digits
    if settings['use_symbols']:
        chars += string.punctuation
    if not chars:
        chars = string.ascii_letters + string.digits
        settings['use_lower'] = True
        settings['use_upper'] = True
        settings['use_digits'] = True

    password = ''.join(secrets.choice(chars) for _ in range(settings['length']))
    return password


def generate_preview(settings, preview_length=12):
    chars = ''
    if settings['use_lower']:
        chars += string.ascii_lowercase
    if settings['use_upper']:
        chars += string.ascii_uppercase
    if settings['use_digits']:
        chars += string.digits
    if settings['use_symbols']:
        chars += string.punctuation

    if chars:
        return ''.join(secrets.choice(chars) for _ in range(preview_length))
    else:
        return "Нет выбранных символов!"