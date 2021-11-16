import telebot
from telebot.types import Message

bot = telebot.TeleBot('2142718885:AAFNwMfbBpKq9lrfEvydERsOn4RM5AhjiS8')
board = [" " for i in range(9)]
opponentlist = []
iconSelectionList = {}


def print_board(message):
    row1="|{}|{}|{}|\n|{}|{}|{}|\n|{}|{}|{}|".format(board[0],board[1],board[2],board[3],board[4],board[5],board[6],board[7],board[8])
    bot.send_message(message.chat.id,row1)

def player_icon(message):
    icon = message.text
    userid = message.chat.id
    iconSelectionList[userid] = icon
    print(iconSelectionList)

def player_move(icon):
    if icon =="X":
        number = 1
    elif icon =="O":
        number = 2

    print("your turn player {}".format(number))

    choice = int(input("Enter your move (1-9)").strip())
    if board[choice - 1] == " ":
        board[choice - 1] = icon
    else:
        print("Spot already taken")
        player_move(icon)

def AddToOpponentList(message):
    if len(opponentlist) == 0 :
        print("Adding {} to waitlist".format(message.chat.id))
        opponentlist.append(message.chat.id)
        print(opponentlist)
    else:
        for x in opponentlist :
            if x == message.chat.id :
                print("{} Already inside waitlist".format(x))
            else:
                print("Adding {} to waitlist".format(x))
                opponentlist.append(message.chat.id)
                print(opponentlist)


def Matchmaking(message):
    x = (len(opponentlist))
    if x >= 2:
        print("Start Match")
        bot.send_message(message.chat.id,"You have been matched!")
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row('X',"O")
        sent = bot.send_message(message.chat.id, "Choose X/O", reply_markup=start_markup)
        bot.register_next_step_handler(sent,player_icon)
    else:
        print("Not Big 2")

def Pbot(message):
    print("")


def TwoP(message):
    bot.send_message(message.chat.id,"Looking for an Opponent...")
    print(message.chat.id)
    AddToOpponentList(message)
    Matchmaking(message)

#To Determine Gamemode 2P or Bot
def TwoPorBot(message):
    if message.text == "2P" :
        TwoP(message)
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