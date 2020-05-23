from telegram.ext import Updater
from telegram.ext import CommandHandler,MessageHandler,Filters
from telegram.message import User
import logging
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import csv


updater = Updater(token='823328456:AAEZqOTZcLnJywiza9PkvgtyHjdFjeFzenE', use_context=True)
dp = updater.dispatcher
data_time_directory='/home/pi/teletest/temp_measure/'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    usr_name=update.message.from_user.username
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Privet, {usr_name}, pomahaemsa?")

def echo(update, context):
    update.message.reply_text('Di nah')

def get_temp(update,context):
    data_complete=[]
    with open(data_time_directory+'date_time_temp.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data_complete.append(row[2])
        csvfile.close()
    plt.plot([x for x in range(len(data_complete))],data_complete,color='r')
    plt.savefig(data_time_directory+'plot.png')
    update.bot.send_photo(chat_id=update.effective_chat.id, photo=open(data_time_directory+'plot.png', 'rb'))


start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)
dp.add_handler(MessageHandler(Filters.text, echo))
graph_handler=CommandHandler('get_temp',get_temp)
dp.add_handler(graph_handler)

updater.start_polling()