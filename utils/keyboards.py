from telebot import types


def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_generate = types.KeyboardButton('🔐 Сгенерировать пароль')
    btn_check = types.KeyboardButton('🔍 Проверить пароль')
    btn_settings = types.KeyboardButton('⚙️ Настройки')
    btn_help = types.KeyboardButton('❓ Помощь')
    markup.add(btn_generate, btn_check, btn_settings, btn_help)
    markup.add(types.KeyboardButton('👨‍💻 О разработчиках'))

    return markup


def get_password_actions_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_new = types.InlineKeyboardButton("🔄 Ещё один", callback_data="generate_again")
    btn_settings = types.InlineKeyboardButton("⚙️ Настройки", callback_data="open_settings")
    markup.add(btn_new, btn_settings)
    return markup


def get_settings_keyboard(settings):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(
        f"📏 Длина: {settings['length']}",
        callback_data="change_length"
    ))
    btn_lower = types.InlineKeyboardButton(
        f"{'✅' if settings['use_lower'] else '❌'} Строчные (a-z)",
        callback_data="toggle_lower"
    )
    btn_upper = types.InlineKeyboardButton(
        f"{'✅' if settings['use_upper'] else '❌'} Заглавные (A-Z)",
        callback_data="toggle_upper"
    )
    btn_digits = types.InlineKeyboardButton(
        f"{'✅' if settings['use_digits'] else '❌'} Цифры (0-9)",
        callback_data="toggle_digits"
    )
    btn_symbols = types.InlineKeyboardButton(
        f"{'✅' if settings['use_symbols'] else '❌'} Спецсимволы (!@#)",
        callback_data="toggle_symbols"
    )
    markup.add(btn_lower, btn_upper, btn_digits, btn_symbols)
    markup.add(types.InlineKeyboardButton(
        "🔐 Сгенерировать из этих настроек",
        callback_data="generate_from_settings"
    ))
    markup.add(types.InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_main"))
    return markup


def get_length_selector_keyboard():
    from config import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
    markup = types.InlineKeyboardMarkup(row_width=3)
    lengths = [8, 10, 12, 14, 16, 18, 20, 24, 32]
    buttons = []
    for l in lengths:
        if MIN_PASSWORD_LENGTH <= l <= MAX_PASSWORD_LENGTH:
            buttons.append(types.InlineKeyboardButton(str(l), callback_data=f"set_length_{l}"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("✏️ Своя длина", callback_data="custom_length"))
    markup.add(types.InlineKeyboardButton("◀️ Назад к настройкам", callback_data="back_to_settings"))
    return markup


def get_developers_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(
        "🔗Мой GitHub",
        url="https://github.com/Sm1rnov10"
    ))
    markup.add(types.InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_main"))
    return markup