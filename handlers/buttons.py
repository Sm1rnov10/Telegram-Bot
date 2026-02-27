from telebot import types
from handlers.common import (
    handle_generate_button,
    process_password_check,
    help_command,
    start_command
)
from handlers.callbacks import show_settings


def register_buttons(bot):
    @bot.message_handler(func=lambda message: message.text == '🔐 Сгенерировать пароль')
    def handle_generate_button_wrapper(message):
        handle_generate_button(bot, message)

    @bot.message_handler(func=lambda message: message.text == '🔍 Проверить пароль')
    def handle_check_button(message):
        msg = bot.send_message(
            message.chat.id,
            "🔍 Отправьте мне пароль, который хотите проверить:\n"
            "(или отправьте /cancel для отмены)",
            reply_markup=types.ForceReply(selective=True)
        )
        bot.register_next_step_handler(msg, lambda m: process_password_check(bot, m))

    @bot.message_handler(func=lambda message: message.text == '⚙️ Настройки')
    def handle_settings_button(message):
        show_settings(bot, message)

    @bot.message_handler(func=lambda message: message.text == '❓ Помощь')
    def handle_help_button(message):
        help_command(bot, message)