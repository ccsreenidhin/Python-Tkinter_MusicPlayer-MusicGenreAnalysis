# ============================================
# Auther: C C Sreenidhin
# Company: Techstack Innovations LLP
# Project: Music Analyser
# Date:01-09-2017
# ============================================

#import modules
#=============================================
import os
from shutil import copyfile
import shutil
import Tkinter, ttk,tkFileDialog
import pygame
from tkFileDialog import askdirectory
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from Tkinter import *

#=============================================

#initialise global variables==================
listofsongs = []
realnames = []
index = 0
pause = False
title = ""
directory = ""
genre = ""
destiny = ""
#=============================================

#function to choose directory=================
def directorychooser():
    global listofsongs
    global directory
    directory = askdirectory()
    os.chdir(directory)
    for files in os.listdir(directory):
        if files.endswith(".mp3") or files.endswith(".ogg") or files.endswith(".wav"):
            realdir = os.path.realpath(files)
            listofsongs.append(files)
    print (listofsongs)
    return listofsongs


#function to add music to music listbox=======
def setlistbox(musiclistbox):
    print("hi")
    listofsongs = directorychooser()
    listofsongs.reverse()
    for items in listofsongs:
        musiclistbox.insert(0,items)


#function to update label details============
def updatelabel():
    global genre
    global title
    try:
        meta=EasyID3(listofsongs[index])
        if 'genre' in meta:
            genre =meta['genre'][0]
    except:
        title = listofsongs[index]
    print(genre, listofsongs)


#function to play nextsong===================
def nextsong():
    global listofsongs
    global index
    updatelabel()
    index += 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()


#function to play previous song==============
def prevsong():
    global listofsongs
    global index
    updatelabel()
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()


#function to stop playing song==============
def stopsong():
    pygame.mixer.music.stop()
    #return songname


#function to play song======================
def playsong():
    global listofsongs
    global pause
    updatelabel()
    if pause == False:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        pause = False


#function to pausesong======================
def pausesong():
    global pause
    pause = True
    pygame.mixer.music.pause()


#function to choose Destination Directory===
def destchooser():
    global destiny
    destiny = askdirectory()


#function to start collecting music==========
def classifier():
    global destiny
    for items in listofsongs:
        gene = EasyID3(items)["genre"][0]
        if not os.path.exists(destiny+'/'+gene):
            os.makedirs(destiny+'/'+gene)

        shutil.copy(items, destiny+'/'+gene)
