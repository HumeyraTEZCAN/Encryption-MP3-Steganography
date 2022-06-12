import time
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox

import pygame.mixer

import tkinter as tk
from tinytag import TinyTag
import mp3Stego
from AES2 import AESCipher
import mp3Parser
from huffmanc import HuffmanCoding
import math
import numpy as np

# root window
root = Tk()
root.geometry('820x450')
root.title('steGOgirl')


mp3filename = ""

def mp3about():
    tag = TinyTag.get(mp3filename)
    title="Title:"+tag.title+'\n'
    bitrate="Bitrate:"+f'{tag.bitrate}'+'\n'
    sample_rate= "Sample rate:"+f'{tag.samplerate}'

    raporlabel = Label(embedframe, text="About mp3", bg='#264653', fg='#E76F51', font=("Helvetica", 18))
    aboutmp3label = Label(embedframe, text=title+bitrate+sample_rate,height=10, width=17, bg="#E9C46A")
    raporlabel.place(x=610, y=120)
    aboutmp3label.place(x=612, y=160)
    playbutton = Button(embedframe, text="Play",bg='#f4a261', command=lambda: play())
    playbutton.place(x=645, y=280)
    stopbutton=Button(embedframe, text="Stop", bg='#f4a261',command=lambda: stop())
    stopbutton.place(x=682, y=280)

    calculatesizebutton = Button(embedframe, height=1, width=12, text="calculate size", bg='#f4a261',command=lambda: calculate_size())
    calculatesizebutton.place(x=630, y=330)

def play():
    global mp3filename
    pygame.mixer.init()
    pygame.mixer.music.load(mp3filename)
    pygame.mixer.music.play(loops=0)

def stop():
    pygame.mixer.music.stop()


def select_file():
    global mp3filename
    filetypes = (('mp3 files', '*.mp3'), ('All files', '*.*'))
    mp3filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    mp3about()



# create a menubar
menubar = Menu(root)
root.config(menu=menubar)

# create the file_menu
file_menu = Menu(
    menubar,
    tearoff=0
)


# add menu items to the File menu
file_menu.add_command(label='Open', command= select_file)
file_menu.add_command(label='Close')
file_menu.add_separator()


# add Exit menu item
file_menu.add_command(
    label='Exit',
    command=root.destroy
)

# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)
# create the Help menu
help_menu = Menu(
    menubar,
    tearoff=0
)

help_menu.add_command(label='Welcome')
help_menu.add_command(label='About...')

# add the Help menu to the menubar
menubar.add_cascade(
    label="Help",
    menu=help_menu
)


###########---- embed frame -----------------------------
embedframe = Frame(root,  bg='#264653')
embedframe.place(x=0, y=0)
embedframe.config(width=820 , height=450)

########## ----- extract frame -----------
extractframe = Frame(root, bg='#264653')
extractframe.place(x=0, y=0)
extractframe.config(width=820 , height=450)

### başlangıç framei
startframe = Frame(root, bg='#2a9d8f')
startframe.place(x=0, y=0)
startframe.config(width = 820, height = 450)

def openembed():
    extractframe.place_forget()
    startframe.place_forget()
    embedframe.place(x=0, y=0)



def openextract():
    embedframe.place_forget()
    startframe.place_forget()
    extractframe.place(x=0, y=0)



loadimg=tk.PhotoImage(file="images/arkaplanresim.jpg")
iconLabel=Label(startframe,image=loadimg)
iconLabel.pack()
iconLabel["border"] = "0"
iconLabel.place(x=300,y=60)



loadimage = tk.PhotoImage(file="images/encbackphoto.png")
roundedbutton = tk.Button(startframe,image=loadimage, command=lambda : openembed())
roundedbutton["bg"] = "#2a9d8f"
roundedbutton["border"] = "0"
roundedbutton.pack()
roundedbutton.place(x=240,y=290)

loadimage2 = tk.PhotoImage(file="images/decryptbackphoto.png")
roundedbutton2 = tk.Button(startframe,image=loadimage2, command=lambda : openextract())
roundedbutton2["bg"] = "#2a9d8f"
roundedbutton2["border"] = "0"
roundedbutton2.pack()
roundedbutton2.place(x=440,y=290)


filename = ""

def encrypt():
    global filename, mp3filename
    print(mp3filename)
    mp3Parser.openFile(mp3filename)
    message=newfileentrymessage.get("1.0", "end-1c")
    password = getpassword.get()
    newmp3filename=newfileentry.get()
    aes = AESCipher(password)
    encryptedMessage = aes.encrypt(message)
    if (var1.get() == 1):
        mp3Parser.openFile(mp3filename)
        h = HuffmanCoding(encryptedMessage)
        huffmanencodedencryptedmessage = h.compress()
        mp3Stego.embedText(23, huffmanencodedencryptedmessage)
        mp3Stego.yazdir(newmp3filename)
        compressinfo = "Length of message before huffman encoding: " + str(len(encryptedMessage)) + "\n" "Length of" \
        "Message after huffman encoding: " + str(len(huffmanencodedencryptedmessage))

        tk.messagebox.showinfo(title="Huffman Compress", message=compressinfo)
    else:
        encryptedMessage = encryptedMessage.encode("ascii")
        mp3Stego.embedText(33, encryptedMessage)
        mp3Stego.yazdir(newmp3filename)

def calculate_size():
    global mp3filename
    mp3Parser.openFile(mp3filename)
    framec=mp3Stego.calculateEmptyBytes()
    sizelabel = Label(embedframe, text=str(framec)+" empty bytes", bg='#264653', fg='#e9c46a', font=("Helvetica", 12))
    sizelabel.place(x=617, y=360)

def decrypt():
    global mp3filename
    password = extractaesgetpassword.get()
    mp3Parser.openFile(mp3filename)
    extractedMessage, ismodifiednum = mp3Stego.extractText()
    aes = AESCipher(password)
    if(ismodifiednum == 33):
        try:
            decryptedMessage = aes.decrypt(bytes(extractedMessage))
        except:
            tk.messagebox.showerror(title=None, message="wrong password")
            decryptedMessage=""

    if(ismodifiednum == 23):
        h = HuffmanCoding(" ")
        decom_path = h.decompress(bytes(extractedMessage))
        try:
            decryptedMessage = aes.decrypt(decom_path)
        except:
            tk.messagebox.showerror(title=None, message="wrong password")
            decryptedMessage=""

    extractaesmessage = Label(extractframe, text=decryptedMessage, height=12, width=25, bg="white")
    extractaesmessage.pack()
    extractaesmessage.place(x=415, y=180)
    tk.messagebox.showerror(title=None, message="THIS MESSAGE WILL SELF DESTRUCT IN 5 SECONDS!")
    time.sleep(5)
    mp3Parser.openFile(mp3filename)
    messagelen= len(decryptedMessage)
    number = math.floor(messagelen)
    a = np.zeros(number, int)
    mp3Stego.embedText(11, a)
    mp3Stego.yazdir(mp3filename)





extractaesmessagelabel = Label(extractframe, text="Extracted message", bg='#264653', fg='#E9C46A',font=("Helvetica", 16))
extractaesmessagelabel.place(x=415, y=145)
extractaesmessage = Label(extractframe, height=12, width=25, bg="white")
extractaesmessage.pack()
extractaesmessage.place(x=415, y=180)

def upload_file():
    global filename
    filetypes = (('text files', '*.txt'), ('All files', '*.*'))
    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)

####---- aes text field get password
var1 = tk.IntVar()
huffmancheck=ttk.Checkbutton(embedframe, variable=var1, onvalue=1, offvalue=0, text='Huffman')
huffmancheck.place(x=340,y=350)


passwordlabel = Label(embedframe, text = "Enter password",bg='#264653',fg='#E9C46A',font=("Helvetica", 16))
getpassword = Entry(embedframe,  width = 25,bg = "white")
passwordlabel.place(x=340, y=120)
getpassword.place(x=340, y=160)


aesokeybutton = Button(embedframe, height = 2,  width = 12, text ="upload mp3 file",bg='#f4a261' ,command = lambda:select_file())
aesokeybutton.place(x=375, y=220)


aestitle=Label(embedframe,text="AES",bg='#264653',fg="#E76F51",font=("Helvetica", 32))
aestitle.place(x=375,y=25)

newfilelabel = Label(embedframe, text = "Enter new mp3 name",bg='#264653',fg='#e9c46a',font=("Helvetica", 16))
newfilelabel.place(x=325, y=285)

newfileentry = Entry(embedframe,  width = 25,bg = "white")
newfileentry.place(x=340, y=315)


newfilelabelmessage = Label(embedframe, text = "Enter message",bg='#264653',fg='#e9c46a',font=("Helvetica", 16))
newfilelabelmessage.place(x=30, y=120)
newfileentrymessage= Text(embedframe, height=15, width = 25,bg = "white")
newfileentrymessage.place(x=30, y=160)


newfilename = newfileentry.get()
aesembedbutton = Button(embedframe, height = 1,  width = 12, text ="Embed", bg="#E9C46A", command = lambda : encrypt())
aesembedbutton.place(x=380, y=395)




def back():
    extractframe.place_forget()
    embedframe.place_forget()
    startframe.place(x=0, y=0)




#extract frame
backbutton = Button(extractframe, height=1, width=5, text="Back", command=lambda: back())
backbutton.place(x=740, y=400)
#embed back
back2button = Button(embedframe, height=1, width=5, text="Back", command=lambda: back())
back2button.place(x=740, y=400)




#extract devam
aestitleex=Label(extractframe,text="AES",bg='#264653',fg="#E76F51",font=("Helvetica", 32))
aestitleex.place(x=320,y=30)

uploadmp3exbuttonaes = Button(extractframe, height = 2,  width = 12, text ="upload mp3 file",bg='#f4a261' ,   command = lambda : select_file())
uploadmp3exbuttonaes.place(x=200, y=230)


extractaespasswordlabel = Label(extractframe, text = "Enter password",bg='#264653',fg='#E9C46A',font=("Helvetica", 16))
extractaesgetpassword = Entry(extractframe,  width = 25,bg = "white")
extractaespasswordlabel.place(x=170, y=145)
extractaesgetpassword.place(x=170, y=175)

aesextractbutton = Button(extractframe, height = 1,  width = 12, text ="Extract", bg="#E9C46A",   command = lambda : decrypt())
aesextractbutton.place(x=200, y=345)




root.mainloop()