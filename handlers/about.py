from telebot import types
from utils.keyboards import get_developers_keyboard, get_main_menu


def register_about_handlers(bot):

    @bot.message_handler(func=lambda message: message.text == '👨‍💻 О разработчиках')
    def about_command(message):
        show_about_info(bot, message)


def show_about_info(bot, message):
    about_text = (
        "🎯 <b>О проекте:</b>\n"
        "Password Generator Bot — это проект, "
        "созданный для помощи в генерации безопасных паролей.\n\n"

        "🛠 <b>Технологии:</b>\n"
        "• Python 3\n"
        "• pyTelegramBotAPI\n"
        "• Криптостойкая генерация (secrets)\n\n"

        "👥 <b>Разработчик:</b>\n"
        "• Подписывайтесь на канал: https://t.me/+Wp6cznxlr15iMDdi\n\n"

    )
    bot.send_message(
        message.chat.id,
        about_text,
        parse_mode='HTML',
        reply_markup=get_developers_keyboard(),
        disable_web_page_preview=False
    )