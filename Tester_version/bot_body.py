from telegram.ext import Updater
from telegram.ext import CommandHandler,MessageHandler,Filters
from telegram.message import User
import logging

updater = Updater(token='823328456:AAEZqOTZcLnJywiza9PkvgtyHjdFjeFzenE', use_context=True)
dp = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    usr_name=update.message.from_user.username
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Privet, {usr_name}, pomahaemsa?")

def echo(update, context):
    update.message.reply_text('Di nah')


start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)
dp.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()