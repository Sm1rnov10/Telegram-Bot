import telebot
from config import BOT_TOKEN
from handlers.commands import register_commands
from handlers.buttons import register_buttons
from handlers.callbacks import register_callbacks
from handlers.about import register_about_handlers
from utils.keyboards import get_main_menu

bot = telebot.TeleBot(BOT_TOKEN)

register_commands(bot)
register_buttons(bot)
register_callbacks(bot)
register_about_handlers(bot)


# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.lower()

    if text == 'привет':
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name}! Используй кнопки для навигации 👇",
            reply_markup=get_main_menu()
        )
    elif text == 'id':
        bot.reply_to(
            message,
            f"🆔 Твой ID: {message.from_user.id}",
            reply_markup=get_main_menu()
        )
    else:
        bot.send_message(
            message.chat.id,
            "Я не понимаю эту команду. Используй кнопки меню или /help для помощи.",
            reply_markup=get_main_menu()
        )


if __name__ == '__main__':
    print("🚀 Бот запущен...")
    print("📋 Нажмите Ctrl+C для остановки")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"❌ Ошибка: {e}")