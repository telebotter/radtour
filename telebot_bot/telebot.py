#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'tour.settings'
django.setup()
from main.models import Tour
from django.urls import reverse

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
msg_start = "*Hi*,\n Benutze mich! \n Bin zwar noch in arbeit, aber trotzdem cool."




# ------ Create Handle Functions ----- #

def start(bot, update):
    """ This Function is called on /start.
    Its telegrams style guide to serve some info and hints on this command
    """
    bot.send_message(chat_id=update.message.chat_id, text=msg_start, parse_mode='Markdown')



def ui(bot, update):

    # create default keyboard (main menu)
    msg = 'Aktuell ist Tour xy koratzien ausgewählt\n vlt. noch wieviele tage oder so'
    keyboard = [[
        InlineKeyboardButton('Tour bearbeiten', callback_data='ui_edit_tour'),
        InlineKeyboardButton('Tour wechseln', callback_data='ui_change_tour'),
        InlineKeyboardButton('Logbuch', callback_data='cfg_time'),
        InlineKeyboardButton('Bilder', callback_data='cfg_food')
        ], [
        InlineKeyboardButton('Sprache', callback_data='cfg_lan'),
        InlineKeyboardButton('Mensa-ID', callback_data='cfg_mensa'),
        InlineKeyboardButton(Context.strings['config_btn_cancel'],
                             callback_data='cfg_cancel')
    ]]
    markup = InlineKeyboardMarkup(keyboard)
    try:  # to get a messg_id
        msg_id = update.callback_query.message.message_id
        bot.edit_message_text(
            text=cfg_txt,
            chat_id=usr.chat_id,
            message_id=msg_id,
            parse_mode='Markdown',
            reply_markup=markup)
    except:  # create new
        bot.send_message(chat_id=usr.chat_id, text=cfg_txt, parse_mode='Markdown', reply_markup=markup)



# ------ Button definitions --------- #
def button_callback():
    pass



# ----- Regist Handler ----- #
#start_handler = CommandHandler('start', start)
#dispatcher.add_handler(start_handler)

#select_tour_handler = CommandHandler('tour', select_tour)
#dispatcher.add_handler(select_tour_handler)

#select_tag_handler = CommandHandler('tag', select_tag)
#dispatcher.add_handler(select_tag_handler)



logbuch_handler = CommandHandler('logbuch', logbuch_ui)
dispatcher.add_handler(logbuch_handler)

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
