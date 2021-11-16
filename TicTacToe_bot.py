import telebot

bot = telebot.TeleBot('2142718885:AAFNwMfbBpKq9lrfEvydERsOn4RM5AhjiS8')



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