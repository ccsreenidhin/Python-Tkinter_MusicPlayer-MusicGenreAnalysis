# ============================================
# Auther: Sreenidhin C C
# Company: Techstack Innovations LLP
# Project: Music Analyser
# Date:08-09-2017
# ============================================

#import modules
#=============================================
import os
import glob
import sys
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as pyplot
from pydub import AudioSegment
from matplotlib import pylab
from tkFileDialog import askdirectory
from sklearn.model_selection import ShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import scipy.io.wavfile
from scikits.talkbox.features import mfcc
from sklearn.externals import joblib
#=============================================

#=============================================
#initialise global variables==================
testsetlist = []
trainsetdir = ""
testsetdir = ""
testwavdir = "/home/nidhin/Documents/analy/testwavdir"
genres = ['classical', 'country', 'jazz', 'metal', 'pop', 'rock']
testfile = ""
progpath = "/saved/"
confmetx = []
#=============================================

#functions for training the ml==================================================


#function to read the cepsfile to array for training set------------------------


def readcepsoftrain(genres):
    X = []
    y = []
    for label, genre in enumerate(genres):
        for cepfile in glob.glob(os.path.join(trainsetdir, genre, "*.ceps.npy")):
            ceps = np.load(cepfile)
            numofceps = len(ceps)
            arr = np.mean(ceps[int(numofceps / 10):int(numofceps * 9 / 10)], axis=0)
            X.append(arr)
            y.append(label)
    return np.array(X), np.array(y)


#function to do logisticregression on model-------------------------------------
def logregontrainset(X, y):
    global model
    model = LogisticRegression()
    model.fit(X, y)
    joblib.dump(model, 'savedmodel/modeltrained.pkl')	#save the trained model to disk


#function to get the ceps value for a file--------------------------------------
def mfccnceps(filenam):
    print("creating ceps")
    sample_rate, X = scipy.io.wavfile.read(filenam)
    ceps, mspec, spec = mfcc(X)
    basename, extn = os.path.splitext(filenam)
    datafile = basename + ".ceps"
    np.save(datafile, ceps) # cache results so that ML becomes fast



#functions for testing the files(test part)=======================================


#function to convert files to wav-------------------------------------------------
def converttowav():
    print("converting to wav")
    print(testsetdir)
    for files in os.listdir(testsetdir):
        if files.endswith(".mp3"):
            print(files)
            basename, extn = os.path.splitext(files)
            song = AudioSegment.from_mp3(files)
            song = song[:30000]
            print(basename+".wav")
            song.export(testwavdir+'/', format='wav')


#function to write ceps for test file-------------------------------------------
def mfccnceps(filenam):
    print("creating ceps")
    sample_rate, X = scipy.io.wavfile.read(filenam)
    ceps, mspec, spec = mfcc(X)
    basename, extn = os.path.splitext(filenam)
    datafile = basename + ".ceps"
    np.save(datafile, ceps)
    return basename


#function to read ceps for test files-------------------------------------------
def readcepsoftest(basename):
    A = []
    b = []
    filepath = testwavdir+'/'
    print (filepath)
    print("reading ceps")
    for cepfile in glob.glob(os.path.join(filepath, basename+".ceps.npy")):
        print("ceps:",cepfile)
        ceps = np.load(cepfile)
        num_ceps = len(ceps)
        A.append(np.mean(ceps[int(num_ceps / 10):int(num_ceps * 9 / 10)], axis=0))
    return np.array(A), np.array(b)


#function to start predicting the genre-----------------------------------------
def makeprediction(X,y, predbase):
    print "prediction"
    probs = predbase.predict_proba(X)
    print "probs",probs
    probs=probs[0]
    print "probs0",probs
    max_prob = max(probs)
    print "max_prob",max_prob
    for i,j in enumerate(probs):
        if probs[i] == max_prob:
            max_prob_index=i
    print ("max_prob_index", max_prob_index)
    predicted_genre = genres[max_prob_index]
    return predicted_genre

#function to start plotting graphs----------------------------------------------
def plotconfusionmatrics(cmetx, genre_list, name, title, filename):
    pylab.clf()
    pylab.matshow(cmetx, fignum=False)
    ax = pylab.axes()
    ax.set_xticks(range(len(genre_list)))
    ax.set_xticklabels(genre_list)
    ax.xaxis.set_ticks_position("bottom")
    ax.set_yticks(range(len(genre_list)))
    ax.set_yticklabels(genre_list)
    pylab.title(title)
    pylab.colorbar()
    pylab.grid(False)
    pylab.xlabel('Predicted class')
    pylab.ylabel('True class')
    pylab.grid(False)
    pylab.show()
    filename = pathprog + '/' + filename
    pyplot.savefig(filename)

#Button functions===============================================================
def choosetestdir():
    global testsetdir
    testsetdir = askdirectory()


def choosetrainingsetdir():
    global trainsetdir
    trainsetdir = askdirectory()


def dispgraph():
    global confmetx, genres
    name = "Music Analyser"
    title = 'Confusion matrix Graph'
    filename = 'cm_musicceps.pdf'
    plotconfusionmatrics(confmetx, genres, name, title, filename)

def startpred(tree):
    global genres, model, confmetx
    x_train = []
    y_train = []
    models = []
    foo = []
    for gen in genres:
        for j in range(0,11):
            filepath = trainsetdir + '/' + gen + '/' + gen + '.' "%05d" % j + '.wav'
            mfccnceps(filepath)

    X,y = readcepsoftrain(genres)

    rs = ShuffleSplit(n_splits=1, test_size=0.3, random_state=0)
    for train, test in rs.split(X):
        print("TRAIN:", train, "TEST:", test)
        X_train, y_train = X[train], y[train]
        X_test, y_test = X[test], y[test]

    model = LogisticRegression()
    model.fit(X_train, y_train)

    models.append(model)

    predicted = model.predict(X_test)
    confmetx = confusion_matrix(y_test, predicted)

    joblib.dump(models, 'savedmodel/modeltrained.pkl')	#save the trained model to disk
    predbase = joblib.load('savedmodel/modeltrained.pkl')

    cd = os.path.dirname(testsetdir)
    testwavdir = cd + '/' + "testwavdir"
    print(testwavdir)
    #converttowav()

    for files in os.listdir(testwavdir):
        if not files.endswith(".ceps.npy"):
            testsetlist.append(files)
            filepath = testwavdir+'/'+files
            P,q = readcepsoftest(mfccnceps(filepath))
            P = np.array(P)
            print P
            predgenre = makeprediction(P,q, predbase)
            tree.insert("" , 0,    text="", values=(files, predgenre))


#================================END============================================
