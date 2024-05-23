import requests
from bs4 import BeautifulSoup
import os 
from dotenv import load_dotenv
import schedule
import time

load_dotenv()

def get_exchange_rate():
    url = requests.get("https://www.dolar-colombia.com/")
    soup = BeautifulSoup(url.content, "html.parser")
    result = soup.find("span", class_="exchange-rate exchange-rate_up").get_text()
    return result

def telegram_bot_sendtext(bot_message):
    bot_token = os.getenv('bot_token')
    bot_chatID = os.getenv('bot_chatID')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def get_dollar(update, context):
    exchange_rate = get_exchange_rate()
    message = f"El precio del dólar hoy es: {exchange_rate}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def job():
    exchange_rate = get_exchange_rate()
    message = f"El precio del dólar hoy es: {exchange_rate}"
    telegram_bot_sendtext(message)

def main():
    from telegram.ext import Updater, CommandHandler
    updater = Updater(token=os.getenv('bot_token'), use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("dolar", get_dollar))
    updater.start_polling()
    updater.idle()

schedule.every().day.at("15:05").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)  
