from telebot import types
from utils.keyboards import (
    get_settings_keyboard,
    get_length_selector_keyboard,
    get_main_menu
)
from utils.helpers import create_fake_message
from services.password_generator import generate_preview
from data.user_settings import get_user_settings, update_user_settings
from config import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
from handlers.common import handle_generate_button, start_command


def register_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        user_id = call.from_user.id

        try:
            if call.data == "generate_again":
                bot.answer_callback_query(call.id, "Генерируем новый пароль...")
                handle_generate_button(bot, call.message)

            elif call.data == "generate_from_settings":
                bot.answer_callback_query(call.id, "Генерируем пароль из ваших настроек...")
                handle_generate_button(bot, call.message)

            elif call.data == "open_settings":
                bot.answer_callback_query(call.id)
                show_settings(bot, call.message)

            elif call.data == "change_length":
                bot.answer_callback_query(call.id)
                bot.edit_message_text(
                    "📏 Выберите длину пароля:",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_length_selector_keyboard()
                )

            elif call.data == "custom_length":
                bot.answer_callback_query(call.id)
                msg = bot.send_message(
                    call.message.chat.id,
                    f"📏 Введите желаемую длину пароля "
                    f"(от {MIN_PASSWORD_LENGTH} до {MAX_PASSWORD_LENGTH} символов):\n"
                    f"(или отправьте /cancel для отмены)",
                    reply_markup=types.ForceReply(selective=True)
                )
                bot.register_next_step_handler(
                    msg,
                    lambda m: process_custom_length(bot, m, call.message.chat.id, call.message.message_id, call.from_user)
                )

            elif call.data.startswith("set_length_"):
                new_length = int(call.data.split("_")[2])
                update_user_settings(user_id, length=new_length)
                bot.answer_callback_query(call.id, f"Длина установлена: {new_length}")
                update_settings_message(bot, call)

            elif call.data == "toggle_lower":
                current = get_user_settings(user_id)['use_lower']
                update_user_settings(user_id, use_lower=not current)
                bot.answer_callback_query(call.id, "Настройка обновлена")
                update_settings_message(bot, call)

            elif call.data == "toggle_upper":
                current = get_user_settings(user_id)['use_upper']
                update_user_settings(user_id, use_upper=not current)
                bot.answer_callback_query(call.id, "Настройка обновлена")
                update_settings_message(bot, call)

            elif call.data == "toggle_digits":
                current = get_user_settings(user_id)['use_digits']
                update_user_settings(user_id, use_digits=not current)
                bot.answer_callback_query(call.id, "Настройка обновлена")
                update_settings_message(bot, call)

            elif call.data == "toggle_symbols":
                current = get_user_settings(user_id)['use_symbols']
                update_user_settings(user_id, use_symbols=not current)
                bot.answer_callback_query(call.id, "Настройка обновлена")
                update_settings_message(bot, call)

            elif call.data == "back_to_settings":
                bot.answer_callback_query(call.id)
                update_settings_message(bot, call)

            elif call.data == "back_to_main":
                bot.answer_callback_query(call.id)
                bot.delete_message(call.message.chat.id, call.message.message_id)
                user_name = call.from_user.first_name
                from utils.keyboards import get_main_menu

                welcome_text = (
                    f"👋 Привет, {user_name}!\n\n"
                    "Я — бот для генерации надёжных паролей 🔑\n"
                    "Я помогу создать пароль, который сложно взломать, но легко запомнить.\n\n"
                    "Используй кнопки ниже для навигации:"
                )

                bot.send_message(
                    call.message.chat.id,
                    welcome_text,
                    reply_markup=get_main_menu()
                )

        except Exception as e:
            print(f"Ошибка в callback_handler: {e}")
            bot.answer_callback_query(call.id, "Произошла ошибка, попробуйте ещё раз")


def show_settings(bot, message):
    user_id = message.from_user.id
    settings = get_user_settings(user_id)

    bot.send_message(
        message.chat.id,
        "⚙️ <b>Настройки генерации</b>\n\nНажмите на параметры для изменения:",
        parse_mode='HTML',
        reply_markup=get_settings_keyboard(settings)
    )


def update_settings_message(bot, call):
    try:
        user_id = call.from_user.id
        settings = get_user_settings(user_id)

        bot.edit_message_text(
            "⚙️ <b>Настройки генерации</b>\n\nНажмите на параметры для изменения:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=get_settings_keyboard(settings)
        )
    except Exception as e:
        print(f"Ошибка в update_settings_message: {e}")


def process_custom_length(bot, message, original_chat_id, original_message_id, from_user):
    from utils.keyboards import get_main_menu

    if message.text == '/cancel':
        bot.send_message(
            message.chat.id,
            "❌ Отменено.",
            reply_markup=get_main_menu()
        )
        return

    try:
        new_length = int(message.text)
        if MIN_PASSWORD_LENGTH <= new_length <= MAX_PASSWORD_LENGTH:
            user_id = from_user.id
            update_user_settings(user_id, length=new_length)
            bot.delete_message(message.chat.id, message.message_id)
            settings = get_user_settings(user_id)
            bot.edit_message_text(
                "⚙️ <b>Настройки генерации</b>\n\nНажмите на параметры для изменения:",
                original_chat_id,
                original_message_id,
                parse_mode='HTML',
                reply_markup=get_settings_keyboard(settings)
            )

            bot.answer_callback_query(user_id, f"✅ Длина установлена: {new_length}")
        else:
            msg = bot.send_message(
                message.chat.id,
                f"❌ Длина должна быть от {MIN_PASSWORD_LENGTH} до {MAX_PASSWORD_LENGTH} символов. "
                f"Попробуйте ещё раз:",
                reply_markup=types.ForceReply(selective=True)
            )
            bot.register_next_step_handler(
                msg,
                lambda m: process_custom_length(bot, m, original_chat_id, original_message_id, from_user)
            )
    except ValueError:
        msg = bot.send_message(
            message.chat.id,
            "❌ Пожалуйста, введите число. Попробуйте ещё раз:",
            reply_markup=types.ForceReply(selective=True)
        )
        bot.register_next_step_handler(
            msg,
            lambda m: process_custom_length(bot, m, original_chat_id, original_message_id, from_user)
        )