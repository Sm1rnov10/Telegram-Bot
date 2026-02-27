from telebot import types
from utils.keyboards import get_main_menu
from handlers.common import handle_generate_button, start_command, help_command

def register_commands(bot):
    @bot.message_handler(commands=['start'])
    def start_command_wrapper(message):
        start_command(bot, message)

    @bot.message_handler(commands=['help'])
    def help_command_wrapper(message):
        help_command(bot, message)

    @bot.message_handler(commands=['generate'])
    def generate_command_wrapper(message):
        handle_generate_button(bot, message)

    @bot.message_handler(commands=['settings'])
    def settings_command_wrapper(message):
        from handlers.callbacks import show_settings
        show_settings(bot, message)

    @bot.message_handler(commands=['check'])
    def check_command_wrapper(message):
        msg = bot.send_message(
            message.chat.id,
            "🔍 Отправьте мне пароль, который хотите проверить:\n"
            "(или отправьте /cancel для отмены)",
            reply_markup=types.ForceReply(selective=True)
        )
        from handlers.buttons import process_password_check
        bot.register_next_step_handler(msg, lambda m: process_password_check(bot, m))

    @bot.message_handler(commands=['random'])
    def random_command_wrapper(message):
        from services.password_generator import generate_password
        from services.password_checker import check_password_strength
        from utils.helpers import escape_html
        from utils.keyboards import get_password_actions_keyboard
        settings = {
            'length': 16,
            'use_lower': True,
            'use_upper': True,
            'use_digits': True,
            'use_symbols': True
        }

        password = generate_password(settings)
        strength_info = check_password_strength(password)
        escaped_password = escape_html(password)

        response = (
            f"🎲 <b>Случайный пароль:</b>\n"
            f"<code>{escaped_password}</code>\n\n"
            f"📊 <b>Характеристики:</b>\n"
            f"• Длина: {len(password)} символов\n"
            f"• Надёжность: {strength_info['color']} <b>{strength_info['name']}</b>\n"
            f"• Время взлома: примерно {strength_info['time']}"
        )

        bot.send_message(
            message.chat.id,
            response,
            parse_mode='HTML',
            reply_markup=get_password_actions_keyboard()
        )