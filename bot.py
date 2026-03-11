import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8623847440:AAEIdP_xJEVaqx8HIf_FtY_qkVBJvF2Dudg"
ADMIN_ID = 8376476787

bot = telebot.TeleBot(TOKEN)

users = {}

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton("Регистрация"))

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(
    KeyboardButton("📦 Заказать"),
    KeyboardButton("📋 Мои заказы")
)
menu_keyboard.add(
    KeyboardButton("💬 Служба поддержки")
)

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        "Здравствуйте 👋\n"
        "Добро пожаловать в наш магазин 📦\n\n"
        "Нажмите кнопку для регистрации",
        reply_markup=start_keyboard
    )

@bot.message_handler(func=lambda message: message.text == "Регистрация")
def register(message):

    users[message.chat.id] = {"step": "name", "orders": []}

    bot.send_message(
        message.chat.id,
        "Введите имя и фамилию\n"
        "Пример: Рома Смит"
    )

@bot.message_handler(func=lambda message: True)
def handle(message):

    if message.chat.id == ADMIN_ID:

        parts = message.text.split(" ", 1)

        if len(parts) == 2 and parts[0].isdigit():

            user_id = int(parts[0])
            text = parts[1]

            bot.send_message(
                user_id,
                f"💬 Ответ оператора:\n\n{text}"
            )

            bot.send_message(
                ADMIN_ID,
                "✅ Сообщение отправлено клиенту"
            )

        return

    user = users.get(message.chat.id)

    if not user:
        return

    step = user["step"]

    if step == "name":

        users[message.chat.id]["name"] = message.text
        users[message.chat.id]["step"] = "address"

        bot.send_message(
            message.chat.id,
            "Введите адрес 📍"
        )

    elif step == "address":

        users[message.chat.id]["address"] = message.text
        users[message.chat.id]["step"] = "phone"

        bot.send_message(
            message.chat.id,
            "Введите номер телефона 📞"
        )

    elif step == "phone":

        users[message.chat.id]["phone"] = message.text
        users[message.chat.id]["step"] = "menu"

        bot.send_message(
            message.chat.id,
            "Регистрация завершена ✅",
            reply_markup=menu_keyboard
        )

    elif message.text == "📦 Заказать":

        users[message.chat.id]["step"] = "order"

        bot.send_message(
            message.chat.id,
            "Напишите ваш заказ ✏️"
        )

    elif step == "order":

        users[message.chat.id]["orders"].append(message.text)
        users[message.chat.id]["step"] = "menu"

        bot.send_message(
            message.chat.id,
            "✅ Заказ принят!"
        )

        bot.send_message(
            ADMIN_ID,
            f"📦 Новый заказ\n\n"
            f"UserID: {message.chat.id}\n"
            f"Имя: {users[message.chat.id]['name']}\n"
            f"Телефон: {users[message.chat.id]['phone']}\n\n"
            f"Заказ:\n{message.text}"
        )

    elif message.text == "📋 Мои заказы":

        orders = users[message.chat.id]["orders"]

        if not orders:

            bot.send_message(
                message.chat.id,
                "У вас нет заказов 📭"
            )

        else:

            text = "📋 Ваши заказы:\n\n"

            for i, order in enumerate(orders, start=1):
                text += f"{i}. {order}\n"

            bot.send_message(message.chat.id, text)

    elif message.text == "💬 Служба поддержки":

        users[message.chat.id]["step"] = "support"

        bot.send_message(
            message.chat.id,
            "Напишите ваш вопрос ✉️"
        )

    elif step == "support":

        bot.send_message(
            message.chat.id,
            "Ваш вопрос отправлен оператору ✅"
        )

        bot.send_message(
            ADMIN_ID,
            f"💬 Новый вопрос\n\n"
            f"UserID: {message.chat.id}\n"
            f"Имя: {users[message.chat.id]['name']}\n"
            f"Телефон: {users[message.chat.id]['phone']}\n\n"
            f"Вопрос:\n{message.text}"
        )

        users[message.chat.id]["step"] = "menu"

bot.infinity_polling()
