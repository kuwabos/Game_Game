#AI made by Isaya
import time
import datetime
from tkinter import *
from PIL import ImageTk,Image
import os

'''def create_window():
    new_window = Toplevel()
'''
tday = datetime.date.today()
date = "what is the date" or "what's the date"
window = None

def run_game_game():
    os.chdir("/Users/arl003zusmbk/Documents/Game_Game")
    os.system("python3 /Users/arl003zusmbk/Documents/Game_Game/Game_Game.py")


def open():

    top = Toplevel()
#lbl = Label(top, text="Hello").pack()
    my_img = ImageTk.PhotoImage(Image.open("Python_Logo.png").convert('RGB'))
    my_label = Label(master=top, image= my_img)
    my_label.pack()


print("Jobot 1.0, all rights reserved\nMade by Isaya 2021")
name = input("My name is Jobot. What is your name?\n")
namein = bool(name)

if name == "end":
    print("Bye")
    exit()

if namein == False:
    print("So you don't have a name???")
elif namein == True:
    time.sleep(0.75)
    print("Hello " + name)
    time.sleep(0.75)
    what = input("What do you want to do today? please type 1 to 3 (1.Sum Caculator, 2.Talk , 3 Game, 4 Nothing)\n")


    if what == "1":
        first = input("First: ")
        second = input("Second: ")
        sum = float(first) + float(second)
        print("The sum is " + str(sum))
    elif what == "2":
        talk2 = input("What do you want to talk about? please write it in lowercase. type ""end"" to close the program\n")
        if talk2 == "what is the date" and "what's the date":
            print("Today is " + str(tday))
        elif talk2 == "end":
            print("Thank you for using Jobot!")
    elif what == "3":
        window=Tk()
        window.title('Game_Game')
        Button(window, text="play Game_Game",command=run_game_game).pack()
    elif what == "4":
                print("What do you mean nothing")
if(window):
    window.mainloop()
