# ==================================================
# Auther: C C Sreenidhin
# Company: Techstack Innovations LLP
# Project: Music Analyser
# Date:01-09-2017
# ==================================================

#import modules
#===================================================
import os
import Tkinter, ttk,tkFileDialog
from tkFileDialog import askdirectory, askopenfile
from Tkinter import *
from pydub import AudioSegment
#===================================================

#initialise global variables========================
outdir = None
filename = None
sound = None
duration =None
val = None
scale2 = None
temp =""
#===================================================

def choosefile(scalef, scaleb):
    global filename, duration, sound, mp3name
    filename = askopenfile(defaultextension=".mp3", filetypes=(("mpeg file", "*.mp3"),("All Files", "*.*") ))
    print filename
    temp = os.path.dirname(os.path.abspath(__file__))+'/'+"temp/"+'temp.wav'
    sound = AudioSegment.from_mp3(filename)
    duration = sound.duration_seconds
    scalef.config(to = duration)
    scaleb.config(to = duration)



def choosesavefolder():
    global outdir
    outdir = askdirectory()


def startcut(scalef, scaleb):
    global val, sound, mp3name, outdir
    valb = 0
    temp = ""
    valb =scaleb.get()
    valinsec = int(val) * 1000
    valbinsec = int(valb) * 1000
    print valinsec, valbinsec
    sound1 = sound[valinsec:valbinsec]
    #sound1.export("split2.mp3", format="mp3", tags={'artist': 'Musiana', 'comments': 'By musiana'} )
    #print sound1
    path = outdir + '/' + "cutout.mp3"
    sound1.export(path, format="mp3", tags={'artist': 'Musiana', 'comments': 'By musiana'} )
    print "success"


def setscaleb(value, scaleb):
    global val
    #print value
    val  = value
    scaleb.config(from_ = value)






