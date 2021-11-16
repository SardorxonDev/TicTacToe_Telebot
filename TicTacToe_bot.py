import telebot
from telebot.types import Message

bot = telebot.TeleBot('2142718885:AAFNwMfbBpKq9lrfEvydERsOn4RM5AhjiS8')
board = [" " for i in range(9)]
opponentlist = []

def print_board(message):
    row1="|{}|{}|{}|\n|{}|{}|{}|\n|{}|{}|{}|".format(board[0],board[1],board[2],board[3],board[4],board[5],board[6],board[7],board[8])
    row2="|{}|{}|{}|".format(board[3],board[4],board[5])
    row3="|{}|{}|{}|".format(board[6],board[7],board[8])
    bot.send_message(message.chat.id,row1)

def AddToOpponentList(message):
    print("In addtoopp")
    if len(opponentlist) == 0 :
        opponentlist.append(message.chat.id)
        print(opponentlist)
    else:
        for x in opponentlist :
            print(x)
            if x == message.chat.id :
                print("Already inside waitlist")
            else:
                opponentlist.append(message.chat.id)
                print(opponentlist)


def Matchmaking():
    x = (len(opponentlist))
    if x >= 2:
        print("Big 2")
    else:
        print("Not Big 2")

def Pbot(message):
    bot.send_message(message.chat.id,"Looking for an Opponent...")
    print(message.chat.id)
    AddToOpponentList(message)
    Matchmaking()


def TwoP():
    print_board()

#To Determine Gamemode 2P or Bot
def TwoPorBot(message):
    if message.text == "2P" :
        Pbot(message)
        #print_board(message)
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