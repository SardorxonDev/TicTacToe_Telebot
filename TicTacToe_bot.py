import telebot
from telebot.types import Message
from telebot import types

bot = telebot.TeleBot('2142718885:AAFNwMfbBpKq9lrfEvydERsOn4RM5AhjiS8')
board = [" " for i in range(9)]
opponentlist = []
playermove = []

class Player:
    def __init__(self, userid, username, opponent, icon, order, match=False):
        self.userid = userid
        self.name = username
        self.opponent = opponent
        self.icon = icon
        self.order = order
        self.match = match

# To Print Board
def print_board(player1,player2):
    row1 = "|{}|{}|{}|\n|{}|{}|{}|\n|{}|{}|{}|".format(
        board[0], board[1], board[2], board[3], board[4], board[5], board[6], board[7], board[8])
    bot.send_message(player1, row1)
    bot.send_message(player2, row1)

def is_victory(icon):
    if (board[0] == icon and board[1] == icon and board[2] == icon) or \
        (board[3]== icon and board[4] == icon and board[5] == icon) or \
        (board[6]== icon and board[7] == icon and board[8] == icon) or \
        (board[0]== icon and board[3] == icon and board[6] == icon) or \
        (board[1]== icon and board[4] == icon and board[7] == icon) or \
        (board[2]== icon and board[5] == icon and board[8] == icon) or \
        (board[0]== icon and board[4] == icon and board[8] == icon) or \
        (board[2]== icon and board[4] == icon and board[6] == icon):
        return True
    else:
        return False

def is_draw():
    if " " not in board:
        return True
    else:
        return False

def player_move_select(message):
    playermove.append(int(message.text))    

def player_move(player):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('1')
    itembtn2 = types.KeyboardButton('2')
    itembtn3 = types.KeyboardButton('3')
    itembtn4 = types.KeyboardButton('4')
    itembtn5 = types.KeyboardButton('5')
    itembtn6 = types.KeyboardButton('6')
    itembtn7 = types.KeyboardButton('7')
    itembtn8 = types.KeyboardButton('8')
    itembtn9 = types.KeyboardButton('9')
    markup.row(itembtn1, itembtn2,itembtn3)
    markup.row(itembtn4, itembtn5, itembtn6)
    markup.row(itembtn7, itembtn8, itembtn9)
    sent = bot.send_message(player.userid, "Your turn player {}\nEnter your move (1-9)".format(player.order), reply_markup=markup)
    bot.register_next_step_handler(sent, player_move_select)
    choice = playermove.pop(0)
    if board[choice - 1] == " ":
        board[choice - 1] = player.icon
    else:
        bot.send_message(player.userid,"Spot Already Taken!")
        player_move(player)

def AddToOpponentList(message):
    if len(opponentlist) == 0:
        print("Adding {} to waitlist".format(message.chat.id))
        opponentlist.append([message.chat.id,message.chat.username])
        print(opponentlist)
    else:
        for x in opponentlist:
            if x == message.chat.id:
                print("{} Already inside waitlist".format(x))
            else:
                print("Adding {} to waitlist".format(message.chat.id))
                opponentlist.append([message.chat.id,message.chat.username])
                print(opponentlist)


def Matchmaking():
    while True:
        x = (len(opponentlist))
        if x >= 2:
            global player1,player2
            player1 = opponentlist.pop(0)
            print(player1)
            print(opponentlist)
            player2 = opponentlist.pop(0)
            print(player2)
            print(opponentlist)
            player1 = Player(player1.pop(0),player1.pop(0),player2[1],"X",1,True)
            player2 = Player(player2.pop(0),player2.pop(0),player1.name,"O",2,True)
            bot.send_message(player1.userid, "You have been matched against {}! \nYou are Player {} and will go no.{}".format(player2.name,player1.icon,player1.order))
            bot.send_message(player2.userid, "You have been matched against {}! \nYou are Player {} and will go no.{}".format(player1.name,player2.icon,player2.order))
            print("Start Match Between {} and {}".format(player1.name,player2.name))
            break
        else:
            continue

def Gameplay():
    while True:
        print_board(player1.userid,player2.userid)
        player_move(player1)
        print_board(player1.userid,player2.userid)
        if is_victory(player1.icon):
            bot.send_message(player1.userid,"X wins! Congrats! ")
            bot.send_message(player2.userid,"X wins! You Lose! ")
            break
        elif is_draw():
            bot.send_message(player1.userid,"It's a draw!")
            bot.send_message(player2.userid,"It's a draw!")
            break
        bot.send_message(player2.userid,"{} has moved, your turn {}...".format(player1.name,player2.name))
        player_move(player2)
        print_board(player1.userid,player2.userid)
        if is_victory(player2.icon):
            bot.send_message(player2.userid,"O wins! Congrats! ")
            bot.send_message(player1.userid,"O wins! You Lose! ")
            break
        elif is_draw():
            bot.send_message(player1.userid,"It's a draw!")
            bot.send_message(player2.userid,"It's a draw!")
            break
        bot.send_message(player1.userid,"{} has moved, your turn {}...".format(player2.name,player1.name))


# To Determine Gamemode 2P or Bot
def TwoPorBot(message):
    if message.text == "2P":
        bot.send_message(message.chat.id, "Looking for an Opponent...")
        AddToOpponentList(message)
        Matchmaking()
        Gameplay()
        print("Out of Matchmaking")
    elif message.text == "Bot":
        print("")
        # Pbot()


@bot.message_handler(commands=['startgame'])
def start_game(message):
    start_game_message = "Game will begin. \n 2P or Bot?"
    start_markup = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    start_markup.row('2P', "Bot")
    sent = bot.send_message(
        message.chat.id, start_game_message, reply_markup=start_markup)
    bot.register_next_step_handler(sent, TwoPorBot)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    welcome_message = "Hello,\n /start to start the bot \n /help to get instructions \n /startgame to start game"
    bot.reply_to(message, welcome_message)




print("I'm listening...")
bot.infinity_polling()
