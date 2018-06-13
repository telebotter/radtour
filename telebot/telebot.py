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

"""
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
"""


# ----- SETUP ------ #
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token='498664396:AAGcMqVSxVvnqxgC_a0twCnuIclORUEHYgI')
dispatcher = updater.dispatcher

# ----- Some statics ------ #
msg_start = "*Hi*,\n Benutze mich! \n Bin zwar noch in arbeit, aber trotzdem cool."
        
        

# ------ Helper Funktions -------- #
"""
def event2msg(event):
    player_yes = event.player_set.all().filter(player_status=3)
    player_no = event.player_set.all().filter(player_status=1)
    player_maybe = event.player_set.all().filter(player_status=2)
    player_count = player_yes.count()
    msg = "*"+str(event.event_name)+" (" + str(player_count) + ")*\n"
    for p in player_yes:
        msg += '\n'
        msg += str(p.player_name)
    msg += '\n\n'
    msg += str(player_maybe.count()) +' Vielleicht, ' +  str(player_no.count())+' Absagen'
    msg += ' [Details](https://kicken.sarbot.de/eventer/detail/' + str(event.id) + ')'

    #keyboard
    keyboard = [[InlineKeyboardButton("Dabei", callback_data=str(event.id)+',3'),
        InlineKeyboardButton("Hmm", callback_data=str(event.id)+',2'), 
        InlineKeyboardButton("Bin raus", callback_data=str(event.id)+',1'),
        InlineKeyboardButton("Repost", callback_data=str(event.id)+' ,99'),
        ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return msg, reply_markup

def button(bot, update):
    # TODO: checkout how to pass args from callbackqueryhandler to
    # callbackqueryfunction to pass the event and dont read it again from db?
    query = update.callback_query
    user = query.from_user
    print(user)
    user_id = user.id
    user_name = user.first_name
    data = query.data.split(',')
    event_id = data[0]
    event = Event.objects.get(pk=event_id)
    player_status = data[1]
    if player_status == str(99):
        #repost
        bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        msg, markup = event2msg(event)
        bot.send_message(chat_id=query.message.chat_id, text=msg, reply_markup=markup, parse_mode='Markdown', silent=True)
    else:

        #clear player
        for p in event.player_set.all():
            if p.player_telegram_id == user_id and user_id != 0:
                p.delete()
                print('deleting from list')

        #create new player
        player = event.player_set.create(player_name=user_name, player_status=player_status, player_telegram_id=user_id)
        player.save()
        msg, markup = event2msg(event)
        bot.edit_message_text(text=msg,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id, parse_mode='Markdown', reply_markup=markup)
    # TODO: error bzw. warnung kommt warsch wenn keine änderung vorgenommen
    # wird...


def parselocation(string):
    locs = Location.objects.all()
    lat = lon = 0
    for loc in locs:
        if string.lower() in loc.names:
            print("parser found location")
            lat=loc.lat
            lon=loc.lon
            break
    return lat, lon

"""

# ------ Create Handle Functions ----- #

def start(bot, update):
    """ This Function is called on /start.
    Its telegrams style guide to serve some info and hints on this command
    """
    bot.send_message(chat_id=update.message.chat_id, text=msg_start, parse_mode='Markdown')


def show(bot, update, args):
    """ This Function returns the newest event as signable playerlist with details.
    """
    try:
        tour = Tour.objects.get(alias=args[0])
        msg = tour.name
    except:
        msg = 'not found'
    bot.send_message(chat_id=update.message.chat_id, text=msg)


def select_tour(bot, update):
    """ Sends all Events
    """
    touren = Tour.objects.all()  # TODO: filter this bunch
    msg = 'Touren: \n'
    for tour in touren:
        msg += "\n  "
        msg += tour.name
    bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')


def tour_erstellen(bot, update):
    """eine neue Tour vom bot aus erstellen...
    """
    pass

def logbuch_ui(bot, update):
    pass



# ------ Button definitions --------- #
def logbuch_button():


# ----- Regist Handler ----- #
#start_handler = CommandHandler('start', start)
#dispatcher.add_handler(start_handler)

#select_tour_handler = CommandHandler('tour', select_tour)
#dispatcher.add_handler(select_tour_handler)

#select_tag_handler = CommandHandler('tag', select_tag)
#dispatcher.add_handler(select_tag_handler)

logbuch_handler = CommandHandler('logbuch', logbuch_ui)
dispatcher.add_handler(logbuch_handler)


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
