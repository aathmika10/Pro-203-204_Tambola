import socket
from tkinter import *
import tkinter as tk
from  threading import Thread
import random
from PIL import ImageTk, Image
#from tkmacosx import Button
import platform

screen_width = None
screen_height = None

SERVER = None
PORT = 6000
IP_ADDRESS = '127.0.0.1'
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow=None

ticketGrid=[]
currentNumberList=[]
flashNumberList=[]
flashNumberLabel=None

def createTicket():
    global gameWindow
    global ticketGrid

    mainLabel=Label(gameWindow,width=65,height=16,relief="ridge",borderwidth=5,bg="white")
    mainLabel.place(x=95,y=119)

    xPos=105
    yPos=130
    for row in range(0,3):
        rowList=[]
        for col in range(0,9):
            if(platform.system()=='Darwin'):
                boxButton=Button(gameWindow,font=("chalkboard SE",18),borderwidth=3,pady=23,padx=22,bg='#fff176',highlightbackground="#fff176",activebackground='#c5e1a5')
                boxButton.place(x=xPos,y=yPos)
            else:
                boxButton=tk.Button(gameWindow,font=("chalkboard SE",18),borderwidth=5,width=3,height=2,bg='#fff176')
                boxButton.place(x=xPos,y=yPos)
            
            rowList.append(boxButton)
            xPos+=64
        
        ticketGrid.append(rowList)
        xPos=105
        yPos+=82

def placeNumbers():
    global ticketGrid
    global currentNumberList

    for row in range (0,3):
        randomColList=[]
        counter=0
        while counter<=4:
            randomCol=random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1

        numberContainer={
            "0":[1,2,3,4,5,6,7,8,9],
            "1":[10,11,12,13,14,15,16,17,18,19],
            "2":[20,21,22,23,24,25,26,27,28,29],
            "3":[30,31,32,33,34,35,36,37,38,39],
            "4":[40,41,42,43,44,45,46,47,48,49],
            "5":[50,51,52,53,54,55,56,57,58,59],
            "6":[60,61,62,63,64,65,66,67,68,69],
            "7":[70,71,72,73,74,75,76,77,78,79],
            "8":[80,81,82,83,84,85,86,87,88,89,90],
        }

        counter=0
        while(counter<len(randomColList)):
            colNum=randomColList[counter]
            numbersListByIndex=numberContainer[str(colNum)]
            randomNumber=random.choice(numbersListByIndex)

            if(randomNumber not in currentNumberList):
                numberBox=ticketGrid[row][colNum]
                numberBox.configure(text=randomNumber,fg="black")
                currentNumberList.append(randomNumber)
                counter+=1
    for row in ticketGrid:
        for numberBox in row:
            if (not numberBox['text']):
                numberBox.configure(
                    state='disabled',disabledbackground='#ff8a65',highlightbackground='#ff8a65'
                )


def gameWindow():
    global gameWindow
    global canvas2
    global screen_height
    global screen_width
    global dice
    global winningMessage
    global resetbutton
    global flashNumberLabel
    
    #global playerType
    #global playerName
    #global playerTurn

    gameWindow=Tk()
    gameWindow.title("TAMBOLA")
    gameWindow.geometry('800x600')
    screen_height=gameWindow.winfo_screenheight()
    screen_width=gameWindow.winfo_screenwidth()
    bg=ImageTk.PhotoImage(file="./assets/background.png")
    
    canvas2=Canvas(gameWindow,width=500,height=500)
    canvas2.pack(fill="both",expand=True)
    canvas2.create_image(0,0,image=bg,anchor="nw")
    #canvas2.create_text(screen_width/2,screen_height/5,text="TAMBOLA")
    canvas2.create_text(screen_width/4.5,50,text="TAMBOLA",font=("Chalkboard SE",60), fill="#3e2723")

    createTicket()
    placeNumbers()

    flashNumberLabel=canvas2.create_text(400,screen_height/2.3,text="Waiting for players...",font=("Chalkboard SE",60), fill="#3e2723")

    gameWindow.resizable(True,True)
    gameWindow.mainloop()



def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())
    gameWindow()
    



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Tambola Family Fun")
    nameWindow.geometry('800x600')


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/3.8,screen_height/8, text = "Enter Name", font=("Calibri",60), fill="black")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 30), bd=5, bg='white')
    nameEntry.place(x = screen_width/7, y=screen_height/5.5 )


    button = Button(nameWindow, text="Save", font=("Cambria", 26),width=10, command=saveName, height=1, bg="#80deea", bd=3)
    button.place(x = screen_width/5, y=screen_height/3)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()







def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    askPlayerName()


setup()