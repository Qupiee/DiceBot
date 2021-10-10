import telebot
import config
import dice

from telebot import types  # keyboard

bot = telebot.TeleBot(config.TOKEN)  # bot import

range_more = 0  # for global var use
range_less = 0


@bot.message_handler(commands=['start'])  # trigger for '/start' command
def begin(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # keyboard
    balance_but = types.KeyboardButton('Узнать баланс💰')
    bet_but = types.KeyboardButton('Играть🎲')
    help_but = types.KeyboardButton('Как играть🤔')
    markup.add(balance_but, bet_but, help_but)  # buttons import
    bot.send_message(message.chat.id, config.welcome_message, reply_markup=markup)  # welcome message


@bot.message_handler(func=lambda m: True)  # message reader
def speech(message):
    if message.text == 'Узнать баланс💰':
        bot.send_message(message.chat.id, dice.balance_line + str(dice.balance))
    elif message.text == 'Играть🎲':
        bot.send_message(message.chat.id, dice.get_less_line)
        bot.register_next_step_handler(message, get_range_less)
    elif message.text == 'Как играть🤔':
        bot.send_message(message.chat.id, dice.help_message)
    elif message.text == '-gold 1000':
        dice.balance += 1000
    elif message.text == '-zero':
        dice.balance = 0
    else:
        bot.send_message(message.chat.id, dice.error)


def get_range_less(message):
    global range_less
    range_less = 0
    if (message.text == 'Узнать баланс💰') or (message.text == 'Играть🎲') or (message.text == 'Как играть🤔'):
        bot.send_message(message.chat.id, dice.error)
        return dice.error
    bot.send_message(message.chat.id, dice.get_more_line)
    while range_less == 0:
        try:
            range_less = int(message.text)
        except Exception:
            return dice.error
    bot.register_next_step_handler(message, get_range_more)


def get_range_more(message):
    global range_more
    range_more = 0
    if (message.text == 'Узнать баланс💰') or (message.text == 'Играть🎲') or (message.text == 'Как играть🤔'):
        bot.send_message(message.chat.id, dice.error)
        return dice.error
    bot.send_message(message.chat.id, dice.bet_line)
    while range_more == 0:
        try:
            range_more = int(message.text)
        except Exception:
            return dice.error
    bot.register_next_step_handler(message, place_bet)


def place_bet(message):
    dice.bet = 0
    if (message.text == 'Узнать баланс💰') or (message.text == 'Играть🎲') or (message.text == 'Как играть🤔'):
        bot.send_message(message.chat.id, dice.error)
        return dice.error
    while dice.bet == 0:
        try:
            dice.bet = int(message.text)
        except Exception:
            return dice.error
    bot.register_next_step_handler(message, bot_result)


# исправить вывод результата
def bot_result(message):
    bot.send_message(message.chat.id, dice.dice_roll(range_less, range_more))
    if dice.result == 'win':
        dice.balance += dice.bet * 2
    if dice.result == 'lose':
        dice.balance -= dice.bet


bot.polling()  # run
