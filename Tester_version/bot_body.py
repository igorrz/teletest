from telegram.ext import Updater
from telegram.ext import CommandHandler,MessageHandler,Filters
from telegram.message import User
import logging,matplotlib
from matplotlib import dates as pltdates
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import csv
from datetime import datetime


updater = Updater(token='823328456:AAEZqOTZcLnJywiza9PkvgtyHjdFjeFzenE', use_context=True)
dp = updater.dispatcher
data_time_directory='/home/pi/teletest/temp_measure/'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    usr_name=update.message.from_user.username
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Privet, {usr_name}, pomahaemsa?")

#def echo(update, context):
#    update.message.reply_text('Di nah')

def get_temp(update,context):
    data_time,data_temp=read_date_temp_file(data_time_directory)
    plt_title='The complete temperature plot'
    temp_plot(data_time,data_temp,plt_title)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(data_time_directory+'current_plot.png', 'rb'))


def get_temp_last_6(update,context):
    data_time,data_temp=read_date_temp_file(data_time_directory)
    data_time=data_time[-180:]; data_temp=data_temp[-180:]
    plt_title='The temperature plot over last 6 hours'
    temp_plot(data_time,data_temp,plt_title)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(data_time_directory+'current_plot.png', 'rb'))
    

def get_current_temp(update,context):
    data_time,data_temp=read_date_temp_file(data_time_directory)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Current Temperature: {np.round(data_temp[-1],1)} Celcius\n"+\
        f'Last measure: {data_time[-1]}')

start_handler = CommandHandler('start', start)
graph_handler=CommandHandler('get_temp',get_temp)
last_6=CommandHandler('overview',get_temp_last_6)
curr_temp=CommandHandler('current',get_current_temp)
dp.add_handler(start_handler)
dp.add_handler(last_6)
dp.add_handler(curr_temp)
#dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_handler(graph_handler)

updater.start_polling()



'''

Here bot unrelated backend functions

'''

def temp_plot(time,temp,title):
    datetime_obj=[matplotlib.dates.date2num(datetime.strptime(i,'%H:%M:%S')) for i in time]
    plt.plot(datetime_obj,temp,color='r')
    plt.title(title)
    plt.xlabel('Time'); plt.ylabel('Temperature in Grad Celsius')
    plt.gca().xaxis.set_major_formatter(pltdates.DateFormatter('%H:%M'))
    plt.savefig(data_time_directory+'current_plot.png')

def read_date_temp_file(path):
    data_temp=[]
    data_time=[]
    with open(path+'date_time_temp.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields=next(csvreader)
        for row in csvreader:
            data_temp.append(float(row[2]))
            data_time.append(row[1])
        csvfile.close()
    return data_time,data_temp