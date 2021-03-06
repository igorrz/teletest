from telegram.ext import Updater
from telegram import ParseMode
from telegram.ext import CommandHandler,MessageHandler,Filters
from telegram.message import User
import logging,matplotlib,csv
import numpy as np
from matplotlib import dates as pltdates
import matplotlib.pyplot as plt
from datetime import datetime
from colors import Color

matplotlib.use('Agg') #the plot will not be shown


updater = Updater(token='823328456:AAEZqOTZcLnJywiza9PkvgtyHjdFjeFzenE', use_context=True)
dp = updater.dispatcher
data_time_directory='/home/pi/teletest/temp_measure/'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    usr_name=update.message.from_user.username
    start_message=f"Hello, {usr_name}!\
        \nThis bot can do only one thing for you: show the current temperature in Igor's apartment. He knows very few commands:\
        \n/{Color.BOLD}overview{Color.BOLDEND} will plot you the temperature over the last 6 hours\
        \n{Color.BOLD}/current{Color.BOLDEND} will show you the current temperature"
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_message,parse_mode=ParseMode.HTML)

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
    plt.xlim(datetime_obj[0],datetime_obj[-1])
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