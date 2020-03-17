import os
from telegrambot.constants import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
commands = []

import logging
logger = logging.getLogger('django')


def remo (bot, update):
    update.message.reply_text('from remo')


def start(bot, update):
    # get or create + logging
    update.message.reply_text(MESSAGES['start'])
start.short = 'Beginne die Unterhaltung'
commands.append(start)


def help(bot, update):
    cmds = '\n'
    for cmd in commands:
        name = cmd.name if hasattr(cmd, 'name') else cmd.__name__
        desc = ' - {}'.format(cmd.short) if hasattr(cmd, 'short') else ''
        cmds += '`/'+name+'`' + desc + '\n'
    update.message.reply_text(MESSAGES['help'].format(cmds), parse_mode='Markdown')
help.short = 'Hilfe und Befehle anzeigen'
help.long = 'Ich zeige dir wie du mit mir umgehen kannst '
commands.append(help)


def csv(bot, update, fname):
    """ abfragen was zu tun und bei callback entsprechende funktionen aufrufen
    """
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('🗺 Mach mir GPX!', callback_data='csv;gpx;{}'.format(fname))], #
        [InlineKeyboardButton('🖼 Als Bild bitte?', callback_data='csv;img;{}'.format(fname))], #
        [InlineKeyboardButton('🌎 Direkt Online..', callback_data='csv;publish;{}'.format(fname))] #
    ])
    update.message.reply_text(MESSAGES['csv'], reply_markup=keyboard, quote=False)


def file(bot, update):
    #update.message.reply_text('found file')
    docu = update.message.document
    #update.message.reply_text('found doc: {}'.format(docu.file_name))
    try:
        f = docu.get_file()

        #update.message.reply_text('got file: {}'.format(type(f)))
        path = os.path.join('/home/django/tour/media/telegram', docu.file_name)
        #update.message.reply_text('Download: {}'.format(path))
        f.download(custom_path=path)
        csv(bot, update, docu.file_name)
    except Exception as e:
        logger.error(e, exc_info=True)
        update.message.reply_text('ERROR')
    update.message.reply_text('finish')
