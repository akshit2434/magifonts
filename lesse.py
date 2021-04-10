from telegram import *
from telegram.ext import *
import os
import shutil
import logging
import constants as keys
import responses as r

def ttfdownload(update, context):
    update.message.reply_text("file detected...")
    context.bot.get_file(update.message.document).download()

def start_command(update, context):
    update.message.reply_text("type something to begin!")
    
def help_command(update,context):
    update.message.reply_text("Search for it on Google, duh")
    
def handle_message(update,context):
    text = str(update.message.text).lower()
    update.message.reply_text(r.sample_responses(text))
    
def error(update,context):
    update.message.reply_text(f"Update {update} caused error {context.error}")
    
def main():
    updater = Updater(keys.API_KEY)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help",help_command))
    
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    dp.add_handler(MessageHandler(Filters.document, ttfdownload))
    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()
    
main()
