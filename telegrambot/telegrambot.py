#myapp/telegrambot.py
# Example code for telegrambot.py module
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from django_telegrambot.apps import DjangoTelegramBot
#from telegrambot.constants import *
from telegrambot.botcommands import csv
from telegrambot.botcommands import file
from telegrambot.botcommands import commands
from telegrambot import utils

import logging
logging.basicConfig(filename='/home/django/tour/debug.log')
logger = logging.getLogger('django')
logger.info('logger created')


def callback(bot, update):
    query = update.callback_query
    data = query.data
    da = data.split(';')

    # handle csv
    if da[0] == 'csv':
        if da[1] == 'gpx':
            logger.info('calling csv2gpx')
            gpx = utils.csv2gpx(da[2], bot, update)
            #update.message.reply('csv2gpx done')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for radtourbot")
    dp = DjangoTelegramBot.getDispatcher('radtourbot')
    dp.add_error_handler(error)
    # on different commands - answer in Telegram
    for cmd in commands:
        pass_args = cmd.pass_args if hasattr(cmd, 'pass_args') else False
        name = cmd.command if hasattr(cmd, 'command') else cmd.__name__
        dp.add_handler(CommandHandler(name, cmd))
    #dp.add_handler(CommandHandler('start', start))
    #dp.add_handler(CommandHandler('help', help))
    logging.info('trying to add csv')
    dp.add_handler(MessageHandler(Filters.document, file))
    dp.add_handler(CallbackQueryHandler(callback))

    # others:
    #dp.add_handler(CommandHandler('csv', csv))
    # log all errors
