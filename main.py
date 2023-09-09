import telebot
import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_sslify import SSLify


# Loading the .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")
SECRET = os.getenv("SECRET")
print(SECRET)
ADMIN_ID = os.getenv("ADMIN_ID")
DORM_ID = os.getenv("DORM_ID")

# Creating a URL
url = "xvichoir.pythonanywhere.com/" + SECRET

# Setting a webhook
bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=url)

# Creating an app
app = Flask(__name__)
sslify = SSLify(app)


# Setting an index page
@app.route('/')
def index():
    return "<h1>Test Dormitory Bot</h1>"


# Setting a main route 
@app.route('/'+SECRET, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


# Start command
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "<b>Вітаю!</b> Цей бот допомагає людям з " +
                     "третього гурту лну знаходити важливу і корисну " +
                     "інформацію. \n\nНапишіть у чаті /faq і бот надішле "+
                     "вам посилання на статтю з усією інфою, команда /vahta " +
                     "підкаже вам графік вахтерів, а за допомогою команди " +
                     "/donate ви можете віддячити автору. \n\nСкарги і " +
                     "пропозиції примаються у пп @FleshkaXDude", 
                     parse_mode='HTML')


# Help command
@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id, "<b>Я чесно не знаю чим тобі допомогти, " +
                     "усе мало б бути і так ясно.</b> \n\nНапиши " +
                     "@FleshkaXDude якщо маєш питання.", parse_mode='HTML')


# Donate command
@bot.message_handler(commands=['donate'])
def donate(m):
    bot.send_message(m.chat.id, "<b>Донати приймаються на карти:</b> " +
                     "\nприват: 5168752084032468 \nмоно: 4441111136306531", 
                     parse_mode='HTML')


# FAQ command
@bot.message_handler(commands=['faq'])
def faq(m):
    bot.send_message(m.chat.id, 'https://telegra.ph/Dormitory-3-09-10')


# Bunt command
@bot.message_handler(commands=['bunt'])
def bunt(m):
    bot.send_sticker(m.chat.id, 
                     sticker="CAACAgIAAxkBAAEYRLBjKfNf9QtXKpeiBrBcSp5BNP2rwAACKiEAAgnVUUlHhGyMxOT0wykE")


# A command for texting in the chosen chat
@bot.message_handler(commands=['write'])
def write(m):
    if m.from_user.id == ADMIN_ID:
        chat = DORM_ID
        if m.text != '/write':
            msg = m.text[7:]
            bot.send_message(chat, msg, parse_mode='HTML')
        else:
            bot.send_message(chat, "чукча на флешці ікс дуд забула написати " +
                             "зміст повідомлення, тому розважаю вас тут сам", 
                             parse_mode='HTML')


# A command for texting in the chosen chat and pinning that message
@bot.message_handler(commands=['pin'])
def pin(m):
    chat = DORM_ID
    if m.from_user.id == ADMIN_ID:
        if m.text != '/pin':
            msg = m.text[5:]
            message = bot.send_message(chat, msg, parse_mode='HTML')
            bot.pin_chat_message(chat, message.id, True)


# Every photo sent by admin in the private bot chat is downloaded for /vahta
@bot.message_handler(content_types=['photo'])
def photo(message):
    if message.chat.type == "private":
        if message.from_user.id == ADMIN_ID:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)

            with open("dorm_bot/dorm_bot/image.jpg", 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.from_user.id, "the img is updated")


# Vahta command that sends a picture with the schedule 
@bot.message_handler(commands=['vahta'])
def vahta(message):
    img = open("image.jpg", 'rb')
    bot.send_photo(message.chat.id, img, 
                   caption="Прошу! Усе що знаю про графік наших (ваших) вахтерів:")


if __name__ == '__main__':
    app.run()


