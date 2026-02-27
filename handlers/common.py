from telebot import types
from utils.keyboards import get_main_menu
from utils.helpers import escape_html
from utils.keyboards import get_password_actions_keyboard
from services.password_generator import generate_password
from services.password_checker import check_password_strength, check_common_patterns
from data.user_settings import get_user_settings


def handle_generate_button(bot, message):
    user_id = message.from_user.id
    settings = get_user_settings(user_id)
    password = generate_password(settings)
    strength_info = check_password_strength(password)
    escaped_password = escape_html(password)
    response = (
        f"🔑 <b>Сгенерированный пароль:</b>\n"
        f"<code>{escaped_password}</code>\n\n"
        f"📊 <b>Характеристики:</b>\n"
        f"• Длина: {len(password)} символов\n"
        f"• Надёжность: {strength_info['color']} <b>{strength_info['name']}</b>\n"
        f"• Время взлома: примерно {strength_info['time']}\n\n"
        f"<i>Совет: Нажмите на пароль, чтобы скопировать</i>"
    )

    try:
        bot.send_message(
            message.chat.id,
            response,
            parse_mode='HTML',
            reply_markup=get_password_actions_keyboard()
        )
    except Exception as e:
        print(f"Ошибка при отправке с HTML: {e}")
        fallback_response = (
            f"🔑 Сгенерированный пароль:\n"
            f"{password}\n\n"
            f"📊 Характеристики:\n"
            f"• Длина: {len(password)} символов\n"
            f"• Надёжность: {strength_info['color']} {strength_info['name']}\n"
            f"• Время взлома: примерно {strength_info['time']}"
        )
        bot.send_message(
            message.chat.id,
            fallback_response,
            reply_markup=get_password_actions_keyboard()
        )


def process_password_check(bot, message):
    from utils.keyboards import get_main_menu
    if message.text == '/cancel' or message.text == '❌ Отмена':
        bot.send_message(
            message.chat.id,
            "❌ Проверка отменена.",
            reply_markup=get_main_menu()
        )
        return

    if message.text and message.text != '/start':
        password = message.text
        strength_info = check_password_strength(password)
        is_common = check_common_patterns(password)
        escaped_password = escape_html(password)

        response = (
            f"📊 <b>Результат проверки пароля:</b>\n"
            f"<code>{escaped_password}</code> (длина: {len(password)})\n\n"
            f"• Надёжность: {strength_info['color']} <b>{strength_info['name']}</b>\n"
            f"• Время взлома: примерно {strength_info['time']}\n"
        )

        if is_common:
            response += "• ⚠️ Обнаружены простые комбинации!\n"

        try:
            bot.send_message(
                message.chat.id,
                response,
                parse_mode='HTML',
                reply_markup=get_main_menu()
            )
        except Exception as e:
            print(f"Ошибка при отправке проверки: {e}")
            fallback_response = (
                f"📊 Результат проверки пароля:\n"
                f"{password} (длина: {len(password)})\n\n"
                f"• Надёжность: {strength_info['color']} {strength_info['name']}\n"
                f"• Время взлома: примерно {strength_info['time']}"
            )
            bot.send_message(
                message.chat.id,
                fallback_response,
                reply_markup=get_main_menu()
            )
    else:
        bot.send_message(
            message.chat.id,
            "❌ Проверка отменена.",
            reply_markup=get_main_menu()
        )


def start_command(bot, message):
    from utils.keyboards import get_main_menu
    if hasattr(message, 'from_user') and message.from_user:
        user_name = message.from_user.first_name
    elif hasattr(message, 'chat') and hasattr(message.chat, 'first_name'):
        user_name = message.chat.first_name
    else:
        user_name = "пользователь"

    welcome_text = (
        f"👋 Привет, {user_name}!\n\n"
        "Я — бот для генерации надёжных паролей 🔑\n"
        "Я помогу создать пароль, который сложно взломать, но легко запомнить.\n\n"
        "Используй кнопки ниже для навигации:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu())


def help_command(bot, message):
    from utils.keyboards import get_main_menu

    help_text = (
        "🤔 <b>Как пользоваться ботом:</b>\n\n"
        "🔐 <b>Сгенерировать пароль</b> — создаст случайный пароль с текущими настройками\n"
        "🔍 <b>Проверить пароль</b> — оценит надёжность любого пароля\n"
        "⚙️ <b>Настройки</b> — изменить параметры генерации\n\n"
        "<b>Советы по безопасности:</b>\n"
        "• Используйте разные пароли для разных сервисов\n"
        "• Длина пароля не менее 12 символов\n"
        "• Включайте все типы символов\n"
        "• Никому не сообщайте свои пароли"
    )
    bot.send_message(
        message.chat.id,
        help_text,
        parse_mode='HTML',
        reply_markup=get_main_menu()
    )