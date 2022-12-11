import telebot
from telebot import types
import helga_module

TOKEN = '5942130702:AAF-s2i84p07Kh9oIXGkHf3W1a-8mF4_ALQ'
bot = telebot.TeleBot(TOKEN)


# t.me/test_book_helga_bot

@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!')
    bot.send_message(message.chat.id, f"List of available commands:\n/books - start searching")


selected = {}


@bot.message_handler(['books'])
def get_user_category(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    fiction = types.KeyboardButton('fiction')
    n_fiction = types.KeyboardButton('non-fiction')
    markup.add(fiction, n_fiction)
    bot.send_message(message.chat.id, f"Select category:", reply_markup=markup)
    bot.register_next_step_handler(message, receive_category)


def receive_category(message):
    selected['category'] = message.text
    bot.register_next_step_handler(message, get_user_subcategory)


@bot.message_handler(content_types=['text'])
def get_user_subcategory(message):
    if message.text == 'fiction':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("science fiction")
        btn2 = types.KeyboardButton("fantasy")
        back = types.KeyboardButton("action & adventure")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Select subcategory", reply_markup=markup)
    elif message.text == 'non-fiction':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("biographies")
        btn2 = types.KeyboardButton("history")
        back = types.KeyboardButton("science & nature")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Select subcategory", reply_markup=markup)
    bot.register_next_step_handler(message, receive_subcategory)


def receive_subcategory(message):
    selected['subcategory'] = message.text
    bot.send_message(message.chat.id, f"Search params: {selected['category']} & {selected['subcategory']}")
    result = helga_module.book_commend(selected['category'], selected['subcategory'])
    bot.send_message(message.chat.id, '5 bestselling books for you: ', parse_mode=None)
    bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)
