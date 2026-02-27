from config import DEFAULT_SETTINGS
_user_settings = {}


def get_user_settings(user_id):
    if user_id not in _user_settings:
        _user_settings[user_id] = DEFAULT_SETTINGS.copy()
    return _user_settings[user_id]

def update_user_settings(user_id, **kwargs):
    if user_id not in _user_settings:
        _user_settings[user_id] = DEFAULT_SETTINGS.copy()

    for key, value in kwargs.items():
        if key in _user_settings[user_id]:
            _user_settings[user_id][key] = value

def reset_user_settings(user_id):
    _user_settings[user_id] = DEFAULT_SETTINGS.copy()