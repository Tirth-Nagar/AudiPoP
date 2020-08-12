"""
Author: Tirth Nagar
Package Name: AudiPoP
File Name: main.py
Description: A simple and user friendly music player that supports .mp3 and .wav files to play music using the Pygame
Module and shown in a beautiful GUI created in Tkinter all in a tiny package that requires under 50mb of RAM at any time.
"""

"""Import Modules"""
import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.filedialog import askdirectory
from mutagen.mp3 import MP3
from pygame import mixer
from ttkthemes import themed_tk as tk

"""Setup Root Window + Themes"""
root = tk.ThemedTk()
root.get_themes()
root.set_theme("arc")

"""Create the status bar that will be located at the bottom"""
statusbar = ttk.Label(root, text="Welcome to AudiPoP", relief=GROOVE, font="Times 14 italic")
statusbar.pack(side=BOTTOM, pady=10, )

"""Create the menu bar that will be located at the top"""
menubar = Menu(root)
root.config(menu=menubar)
subMenu = Menu(menubar, tearoff=0)

"""Declare global variables"""
playlist = []
index = 0
paused = FALSE
muted = FALSE

def onClosing():
    stopMusic()
    root.destroy()


def browseFile():
    global filepath
    filepath = filedialog.askopenfilename()
    add_to_playlist(filepath)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    if filename.endswith(".mp3") or filename.endswith(".wav"):
        index = 0
        playlistBox.insert(index, filename)
        playlist.insert(index, filepath)
        index += 1
    else:
        tkinter.messagebox.showerror("File Error","The file you have selected isn't a supported.")


def massImport():
    try:
        global songlist
        folder = askdirectory()
        os.chdir(folder)
        for files in os.listdir(folder):
            if files.endswith(".mp3"):
                songlist = os.listdir()
                songlist.reverse()
        for files in os.listdir(folder):
            if files.endswith(".wav"):
                songlist = os.listdir()
                songlist.reverse()
        for item in songlist:
            pos = len(songlist)
            playlist.insert(pos, item)
            playlistBox.insert(pos, item)
            pos += 1
    except OSError:
        tkinter.messagebox.showerror("File Error", "No files were selected.")

"""Create the cascading tabs for the menu bar"""
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Mass Import", command=massImport)
subMenu.add_command(label="Exit", command=onClosing)


def aboutUs():
    tkinter.messagebox.showinfo("About AudiPoP", "This is a music player made using tkinter and pygame \nby Tirth Nagar")

"""Create the headings for the cascading tabs of the menu bar"""
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Info", menu=subMenu)
subMenu.add_command(label="About Us", command=aboutUs)

"""Initialize Mixer from Pygame"""
mixer.init()

"""Give the root window a name and assign it a icon"""
root.title("AuidiPoP")
root.iconbitmap(r"images\WindowIcon.ico")

"""Create a Frame to help organize the buttons"""
leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=30)

"""Create the listbox that will display your songs"""
playlistBox = Listbox(leftFrame)
playlistBox.pack()

"""Create a button that adds singular songs to the playlist"""
addbtn = ttk.Button(leftFrame, text="+ Add", command=browseFile)
addbtn.pack(side=LEFT)

def delSong():
    try:
        selected_song = playlistBox.curselection()
        selected_song = int(selected_song[0])
        playlistBox.delete(selected_song)
        playlist.pop(selected_song)
    except IndexError:
        tkinter.messagebox.showerror("File Error", "No Songs in your playlist were selected to be deleted.")

"""Create a button that deletes singular and selected songs from the playlist"""
delbtn = ttk.Button(leftFrame, text="   - Del", command=delSong)
delbtn.pack(side=RIGHT)

"""Create Frames to help organize the buttons"""
rightFrame = Frame(root)
rightFrame.pack(side=RIGHT)

topFrame = Frame(rightFrame)
topFrame.pack()

"""Create a label to display the total length of a song"""
lengthlabel = ttk.Label(topFrame, text="Total Length: --:--", font="Arial 10 bold")
lengthlabel.pack(pady=5)

"""Create a label to display the time remaining in a song"""
currentTimelabel = ttk.Label(topFrame, text="Time Remaining: --:--", relief=GROOVE, font="Arial 10 bold")
currentTimelabel.pack()

def showDetails(playIt):
    fileData = os.path.splitext(playIt)
    if fileData[1] == ".mp3":
        audio = MP3(playIt)
        totalLength = audio.info.length
    else:
        a = mixer.Sound(playIt)
        totalLength = a.get_length()

    mins, secs = divmod(totalLength, 60)
    mins = round(mins)
    secs = round(secs)
    timeFormat = "{:02d}:{:02d}".format(mins, secs)
    lengthlabel["text"] = "Total Length" + " " + timeFormat
    thread = threading.Thread(target=startCount, args=(totalLength,))
    thread.start()

def startCount(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeFormat = "{:02d}:{:02d}".format(mins, secs)
            currentTimelabel["text"] = "Time Remaining" + " " + timeFormat
            time.sleep(1)
            t -= 1

def playMusic():
    try:
        global paused
        global playIt
        global index
        if paused:
            mixer.music.unpause()
            statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
            paused = FALSE
        else:
            try:
                index += 1
                index = 0
                if len(playlist) >= 0:
                    playIt = playlist[index]
                    mixer.music.load(playIt)
                    mixer.music.play()
                    statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
                    showDetails(playIt)
            except:
                tkinter.messagebox.showerror("File Error",
                                             "AudiPoP Is Unable To Read The Files or Your Playlist Maybe Empty! Try Adding Songs")
    except NameError:
        tkinter.messagebox.showerror("File Error",
                                     "AudiPoP Is Unable To Read The Files or Your Playlist Maybe Empty! Try Adding Songs")

def stopMusic():
    mixer.music.stop()
    statusbar["text"] = "Stopped"

def pauseMusic():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar["text"] = "Paused"

def previousMusic():
    try:
        global paused
        global playIt
        global index
        index -= 1
        stopMusic()
        time.sleep(1)
        if paused:
            mixer.music.unpause()
            statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
            paused = FALSE
        if index == -1:
            index = len(playlist) - 1
            playIt = playlist[index]
            mixer.music.load(playIt)
            mixer.music.play()
            statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
            showDetails(playIt)
        playIt = playlist[index]
        mixer.music.load(playIt)
        mixer.music.play()
        statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
        showDetails(playIt)
    except IndexError:
        tkinter.messagebox.showerror("File Error",
                                     "AudiPoP Is Unable To Read The Files or Your Playlist Maybe Empty! Try Adding Songs")

def nextMusic():
    try:
        global paused
        global playIt
        global index
        index += 1
        stopMusic()
        time.sleep(1)
        if paused:
            mixer.music.unpause()
            statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
            paused = FALSE
        if index == len(playlist):
            index = -1
            playIt = playlist[index]
            mixer.music.load(playIt)
            mixer.music.play()
            statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
            showDetails(playIt)

        playIt = playlist[index]
        mixer.music.load(playIt)
        mixer.music.play()
        statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
        showDetails(playIt)
    except IndexError:
        tkinter.messagebox.showerror("File Error",
                                 "AudiPoP Is Unable To Read The Files or Your Playlist Maybe Empty! Try Adding Songs")

def setVol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    return val

def muteMusic():
    global muted
    if muted:
        mixer.music.set_volume(0.5)
        scale.set(50)
        volumeBtn.configure(image=volumephoto)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        scale.set(0)
        volumeBtn.configure(image=mutephoto)
        muted = TRUE

"""Create a Frame to help organize the buttons"""
middleFrame = Frame(rightFrame)
middleFrame.pack(padx=30, pady=30)

"""Turn the images into buttons for various different functions"""
playphoto = PhotoImage(file="Images/Play.png")
playBtn = ttk.Button(middleFrame, image=playphoto, command=playMusic)
playBtn.grid(row=0, column=0, padx=10)

stopphoto = PhotoImage(file="Images/Stop.png")
stopBtn = ttk.Button(middleFrame, image=stopphoto, command=stopMusic)
stopBtn.grid(row=0, column=1, padx=10)

pausephoto = PhotoImage(file="Images/Pause.png")
pauseBtn = ttk.Button(middleFrame, image=pausephoto, command=pauseMusic)
pauseBtn.grid(row=0, column=2, padx=10)

"""Create a Frame to help organize the buttons"""
bottomFrame = Frame(rightFrame)
bottomFrame.pack()

"""Turn the images into buttons for various different functions"""
previousphoto = PhotoImage(file="Images/Previous.png")
previousBtn = ttk.Button(bottomFrame, image=previousphoto, command=previousMusic)
previousBtn.grid(row=0, column=0, padx=10)

nextphoto = PhotoImage(file="Images/Next.png")
nextBtn = ttk.Button(bottomFrame, image=nextphoto, command=nextMusic)
nextBtn.grid(row=0, column=1, padx=10)

mutephoto = PhotoImage(file="Images/Mute.png")
volumephoto = PhotoImage(file="Images/Volume.png")
volumeBtn = ttk.Button(bottomFrame, image=volumephoto, command=muteMusic)
volumeBtn.grid(row=0, column=2, padx=10)

"""Create a scale to use as a volume bar to control the volume"""
scale = ttk.Scale(bottomFrame, from_=0, to_=100, orient=HORIZONTAL, command=setVol)
scale.set(50)
mixer.music.set_volume(0.5)
scale.grid(row=0, column=3, pady=15)

"""Create a Frame to help organize the buttons"""
bottomleftFrame = Frame(leftFrame)
bottomleftFrame.pack(side=BOTTOM)

"""Create a label to help identify where the playlist is"""
playlistLabel = ttk.Label(bottomleftFrame, text="Playlist", font="Arial 13 bold")
playlistLabel.grid(row=1, column=0, pady=10,padx=5)

"""Create a protocol that exeutes when the window is closed insuring the program finishes correctly"""
root.protocol("WM_DELETE_WINDOW", onClosing)
root.mainloop()
