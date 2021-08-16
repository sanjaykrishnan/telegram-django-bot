import django
import os
from pprint import pprint

os.environ['DJANGO_SETTINGS_MODULE'] = 'telegram_bot.settings'
django.setup()
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from home.models import ChatUserData
import re
import json
import websocket

API_KEY = '1990824433:AAFmw2fzwtFlfOT5V5hd76LLxOpnVlYR5l4'


print("startedddddddddddd")


def start(update, context):
    """Sends a message with three inline buttons attached."""
    update.message.reply_text("Hello to you too! If you're interested in yo mama jokes, just click on fat, stupid or dumb and i'll tell you an appropriate joke.")
    show_options(update, context)


def show_options(update, context):
    keyboard = [[
        InlineKeyboardButton("Fat", callback_data='fat'),
        InlineKeyboardButton("Stupid", callback_data='stupid'),
        InlineKeyboardButton("Dumb", callback_data='dumb'),
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Please Select an Option:", reply_markup=reply_markup)


def update_db_record(user_obj, message):
    user = ChatUserData.objects.filter(username=user_obj.username).first()
    if user:
        if message == 'fat':
            user.fat += 1
        elif message == 'stupid':
            user.stupid += 1
        elif message == 'dumb':
            user.dumb += 1
        user.save()
    else:
        fat = 1 if message == 'fat' else 0
        stupid = 1 if message == 'stupid' else 0
        dumb = 1 if message == 'dumb' else 0
        ChatUserData.objects.create(username=user_obj.username, first_name=user_obj.first_name,
                                    last_name=user_obj.last_name, fat=fat, stupid=stupid, dumb=dumb)
    send_ws_data(user_obj.username)


def send_ws_data(username):
    user = ChatUserData.objects.filter(username=username).first()
    ws = websocket.WebSocket()
    ws.connect('ws://localhost:8000/ws/tableData/')
    ws_data = json.dumps({
        'username': user.username,
        'stupid': user.stupid,
        'fat': user.fat,
        'dumb': user.dumb,
    })
    print(ws_data)
    ws.send(ws_data)


def respond_to_option(message):
    jokes = {
        'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                   """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
        'fat': ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
        'dumb': [
            """Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
            """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]
    }
    result_message = ''
    if 'fat' in message:
        result_message = random.choice(jokes['fat'])

    elif 'stupid' in message:
        result_message = random.choice(jokes['stupid'])

    elif 'dumb' in message:
        result_message = random.choice(jokes['dumb'])

    # elif message in ['hi', 'hey', 'hello']:
    #     result_message = "Hello to you too! If you're interested in yo mama jokes, just click on fat, stupid or dumb and i'll tell you an appropriate joke."
    # else:
    #     result_message = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message


def button(update, context):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    update_db_record(query.from_user, query.data)
    query.edit_message_text(text=respond_to_option(query.data))

    # show_options(update, context)


def help_command(update, context):
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def handle_message(update, context):
    text = str(update.message.text).lower()
    pprint(update)
    if text in ['hi', 'hey', 'hello']:
        start(update, context)
    else:
        update.message.reply_text("I don't know any responses for that.")


if __name__ == '__main__':
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling(1.0)
    updater.idle()
