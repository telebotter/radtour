#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'tour.settings'
django.setup()
from django.urls import reverse

from main.models import Tour
from telebot.models import User

import logging
import telegram  # pkg: python-telegram-bot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup



# ----- SETUP ------ #
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token='498664396:AAGcMqVSxVvnqxgC_a0twCnuIclORUEHYgI')
dispatcher = updater.dispatcher

# ----- Some statics ------ #
msg_greets= "*Hi* {},\n Gut dass du fragst, "
msg_start = "*Benutze mich!* \n Bin zwar noch in arbeit, aber trotzdem cool. \n Mit /menu kriegst du ne kleine 'grafische' Oberfläche. /befehle gibt dir die direkten Befehle, falls du weißt was du tust."


# --------- Helper Functions -------- #
def get_or_create_user(update):
    """
    Diese Funktion durchsucht die Datenbank nach einem user mit passender
    chat_id, wenn keiner gefunden wurde, wird ein neuer erstellt in die DB
    geschrieben und übergeben.
    :param update: Nimmt ein telegram update objekt (für id und name)
    :return user: User-Objekt das aus der Datenbank erstellt wurde
    """
    try:
        chat_id = update.message.chat_id
    except:
        chat_id = update.callback_query.from_user.id

    user, new = User.objects.get_or_create(telegram_id=chat_id)

    return user, new



# ------ Create Handle Functions ----- #

def start(bot, update):
    """ This Function is called on /start.
    Its telegrams style guide to serve some info and hints on this command
    """
    user, new = get_or_create_user(update)
    msg = msg_start
    if new:
        msg = msg_greets + msg_start

    bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')



def ui(bot, update):
    user, new = get_or_create_user(update)
    """
    if user.tour:
        ui_tour(bot, update)
    """

    msg = 'Wähle eine der folgenden Touren:'
    touren = Tour.objects.all()
    keyboard = []
    for tour in touren:
        try:
            btn = InlineKeyboardButton(tour.name,
                                       callback_data='ui_tour;{}'.format(tour.alias)),
            keyboard.append([*btn])
        except:
            print('error')
            logging.exception('Could not create Button for Tourlist')

    keyboard.append([InlineKeyboardButton('Neu erstellen', callback_data='ui_new;')])
    markup = InlineKeyboardMarkup(keyboard)
    """
    try:  # to get a messg_id and edit
        print('trying')
        msg_id = update.callback_query.message.message_id
        bot.edit_message_text(
            text=msg,
            chat_id=user.telegram_id,
            message_id=msg_id,
            parse_mode='Markdown',
            reply_markup=markup)
        print('done')
    except:  # create new
        print('exception')
        print(user.telegram_id)
        bot.send_message(chat_id=user.telegram_id, text=msg, parse_mode='Markdown', reply_markup=markup)
        print('msg send')
    """
    bot.send_message(chat_id=user.telegram_id, text=msg, parse_mode='Markdown', reply_markup=markup)


def ui_tour(bot, update):

    # create default keyboard (main menu)
    user, new = get_or_create_user(update)
    msg = 'Ausgewählte Tour: {}'.format(user.tour.name)
    bot.send_message(chat_id=user.telegram_id, text='msg')
    return
    """
    keyboard = [[
        InlineKeyboardButton('Tour bearbeiten', callback_data='ui_edit_tour'),
        InlineKeyboardButton('Tour wechseln', callback_data='ui_change_tour'),
        InlineKeyboardButton('Logbuch', callback_data='cfg_time'),
        InlineKeyboardButton('Bilder', callback_data='cfg_food')
        ], [
        InlineKeyboardButton('Sprache', callback_data='cfg_lan'),
        InlineKeyboardButton('Mensa-ID', callback_data='cfg_mensa'),
        InlineKeyboardButton('Abbrechen',
                             callback_data='cfg_cancel')
    ]]
    markup = InlineKeyboardMarkup(keyboard)
    try:  # to get a messg_id
        msg_id = update.callback_query.message.message_id
        bot.edit_message_text(
            text=msg,
            chat_id=user.telegram_id,
            message_id=msg_id,
            parse_mode='Markdown',
            reply_markup=markup)
    except:  # create new
        bot.send_message(chat_id=user.telegram_id, text=msg, parse_mode='Markdown', reply_markup=markup)
    """

# ------ Button definitions --------- #
def button_callback(bot, update):
    data = update.callback_query.data.split(';')
    user, new = get_or_create_user(update)
    if data[0] == 'ui_tour':
        try:
            print(data[1])
            user.tour = Tour.objects.get(alias=data[1])
            user.save()
            ui_tour(bot, update)
        except:
            print('error in callback')
    elif data[0] == 'cfg_cancel':
        cancel_config(bot, update, usr)
    elif data[0] == 'cfg_abo':
        show_cfg_abo(bot, update, usr)
    elif data[0] == 'cfg_time':
        show_cfg_time(bot, update, usr)
    elif data[0] == 'cfg_mensa':
        show_cfg_mensa(bot, update, usr)
    elif data[0] == 'cfg_food':
        show_cfg_food(bot, update, usr)
    elif data[0] == 'cfg_lan':
        show_cfg_lan(bot, update, usr)
    elif data[0] == 'cfg_delfood':
        show_cfg_food_del(bot, update, usr)
    else:
        logging.warning('unbekannter button gedrückt')


logging.warning(usr.chat_id, usr.first_name)


# ----- Regist Handler ----- #
#start_handler = CommandHandler('start', start)
#dispatcher.add_handler(start_handler)

#select_tour_handler = CommandHandler('tour', select_tour)
#dispatcher.add_handler(select_tour_handler)

#select_tag_handler = CommandHandler('tag', select_tag)
#dispatcher.add_handler(select_tag_handler)



#logbuch_handler = CommandHandler('logbuch', ui_tour_logbuch)
#dispatcher.add_handler(logbuch_handler)
ui_handler = CommandHandler('menu', ui)
dispatcher.add_handler(ui_handler)

dispatcher.add_handler(CallbackQueryHandler(button_callback))



"""
new_handler = CommandHandler('new', new, pass_args=True)
dispatcher.add_handler(new_handler)

map_handler = CommandHandler('map', locate, pass_args=True)
dispatcher.add_handler(map_handler)

help_handler = CommandHandler('help', help_text)
dispatcher.add_handler(help_handler)

show_handler = CommandHandler('show', show_event, pass_args=True)
dispatcher.add_handler(show_handler)

dispatcher.add_handler(CallbackQueryHandler(button))
"""

# ---- Start Bot ---- #
updater.start_polling()
