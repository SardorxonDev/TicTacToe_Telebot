import telebot

bot = telebot.TeleBot('2142718885:AAFNwMfbBpKq9lrfEvydERsOn4RM5AhjiS8')

def Pbot():
    print("In PBot")

def TwoP():
    print("In 2P")

#To Determine Gamemode 2P or Bot
def TwoPorBot(message):
    if message.text == "2P" :
        TwoP()    
    elif message.text == "Bot" :
        Pbot()

@bot.message_handler(commands=['startgame'])
def start_game(message):
    start_game_message = "Game will begin. \n 2P or Bot?"
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row('2P',"Bot")
    sent = bot.send_message(message.chat.id, start_game_message, reply_markup=start_markup)
    bot.register_next_step_handler(sent,TwoPorBot)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    welcome_message = "Hello,\n /start to start the bot \n /help to get instructions \n /startgame to start game"
    bot.reply_to(message,welcome_message)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "out of first loop")

print("I'm listening...")
bot.infinity_polling()