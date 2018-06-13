#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'kicken.settings'
django.setup()
from eventer.models import Player, Event, Location
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
updater = Updater(token='446028208:AAGoCpsLnDaZhIA8MOEPvaPOpnRfTpjCevw')
dispatcher = updater.dispatcher

# ----- Some statics ------ #
msg_start = "*Hi*,\n \
Benutze mich um blitzgeschwind ein Event zu erstellen zu dem Abgestimmt werden kann.\n\
Die Events sind neben Telegram auch [online erreichbar](https://kicken.sarbot.de/eventer).\n\n\
*Befehle:*\n \
/start - _Zeigt diese Nachricht an_\n \
/new - _Erstellt ein Event. Bsp: /new Sonntag 18:00_\n \
/list - _Postet eine Liste von allen Events_\n \
/link - _Postet den Link zur Website_\n \
/map - _Standort vom Aktuellen Event oder Name von der Location dahinter. zB /map vfl_\n \
\n \
*In Arbeit:* \n \
/clean _Löscht alle Posts des Bots_\n \
/cancel - _Ein Event absagen_\n \
/post - _Postet das naechste Event in alle Kanaele (Whatsapp/Facebook/Email)_\n \
@kickenbot - _Inline Steuerung mit allen Befehlen, Chat uebergreifend_\
"

msg_help = "*Moin*,\n \
        Die wichtigsten Befehle sind: \n\
        /new - gefolgt vom Titel erstellt ein event zB /new Sonntag 12:00 Vfl\n\
        /post - schickt das event mit der id (oder das letzt erstellte) an alle abonenten, diese funktion ist noch nicht fertig\n\
        /start - liste aller Befehle\n\
        \n\ Die Befehle können auch über den kleinen Button mit dem slash drauf neben dem textfenster eingegeben werden (vlt. muss man dazu den bot auf der freundesliste haben)"
        
        

# ------ Helper Funktions -------- #

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



# ------ Create Handle Functions ----- #

def help_text(bot, update):
    """ This Function is called on /help.
    """
    bot.send_message(chat_id=update.message.chat_id, text=msg_start, parse_mode='Markdown')

def start(bot, update):
    """ This Function is called on /start.
    Its telegrams style guide to serve some info and hints on this command
    """
    bot.send_message(chat_id=update.message.chat_id, text=msg_start, parse_mode='Markdown')


def show(bot, update, args):
    """ This Function returns the newest event as signable playerlist with details.
    """
    try:
        event = Event.objects.get(args[0])
    except:
        event = Event.objects.all().order_by('event-date')[-1]  
    bot.send_message(chat_id=update.message.chat_id, text=event.event_name)


def listall(bot, update):
    """ Sends all Events
    """
    event_list = Event.objects.all()  # TODO: filter this bunch
    msg = "*Termine:*"
    for event in event_list:
        msg += "\n  "
        #msg += "[" + event.event_name + "](" + str(reverse('eventer:detail', args=[event.id])) + ")"
        msg += "[" + event.event_name +"](https://kicken.sarbot.de/eventer/detail/" + str(event.id) +")"
    bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')


def link(bot, update):
    """ Sends Link to Website
    """
    url = "https://kicken.sarbot.de/eventer"
    msg = "[Webseite](" + url + ")"
    bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')


def new(bot, update, args):
    """ Creates a new Event. 
    If possible direct from args, else asking for name
    """
    msg_noname="Kannst direkt den Namen dahinter tun: /new Name des Events"
    if len(args)>0:
        name = ' '.join(args)
        event = Event(event_name=name)
        event.save()
        event_id = event.id
        event_db = Event.objects.get(pk=event_id)
        msg, markup = event2msg(event_db)
        #update.message.reply_text(text=msg, parse_mode='Markdown', reply_markup=markup)
        bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.send_message(chat_id=update.message.chat_id, text=msg_noname)




def locate(bot, update, args):
    """ Post Location from current Event or from args
    """
    found = False
    lat = lon = 0
    if len(args)>0:
        # post specific location
        words = args
        print(words)
    else:
        # current event 
        events = Event.objects.order_by('-event_date')
        event = events[0]
        event_name = event.event_name
        words = event_name.split(' ')
        print(words)
    for word in words:
        lat, lon = parselocation(word)
        if lat != 0 or lon != 0:
            bot.send_location(chat_id=update.message.chat_id, latitude=lat, longitude=lon)
            found = True
            break
    if not found:
         bot.send_message(chat_id=update.message.chat_id, text="Kein Ort gefunden.")




def show_event(bot, update, args):
    event = Event.objects.all()[0]
    if len(args)>0:
        try:
            event = Event.objects.get(pk=args[0])
        except Exection as e:
            bot.send_message(chat_id=update.message.chat_id, text='ID: nicht gefunden')
    msg, markup = event2msg(event)
    bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown', reply_markup=markup)
    
    

# ----- Regist Handler ----- #
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

listall_handler = CommandHandler('list', listall)
dispatcher.add_handler(listall_handler)

link_handler = CommandHandler('link', link)
dispatcher.add_handler(link_handler)

new_handler = CommandHandler('new', new, pass_args=True)
dispatcher.add_handler(new_handler)

map_handler = CommandHandler('map', locate, pass_args=True)
dispatcher.add_handler(map_handler)

help_handler = CommandHandler('help', help_text)
dispatcher.add_handler(help_handler)

show_handler = CommandHandler('show', show_event, pass_args=True)
dispatcher.add_handler(show_handler)

dispatcher.add_handler(CallbackQueryHandler(button))

# ---- Start Bot ---- #
updater.start_polling()
