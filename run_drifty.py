
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:01:42 2019

Drifting Self Task Functions

@author: moriahstendel
"""


#to do list:
# hide mouse upon DD part


from __future__ import absolute_import, division
from __future__ import absolute_import, division

import sys
import time
import os
import csv
import colorsys
import pandas as pd
import numpy as np
import random
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
from psychopy import event, core, logging, visual, data, gui
from psychopy.core import getTime
import pygame
from pygame.locals import *

from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle

expName = 'Experiment Information' 
expInfo = {'id': '','counterbalance': '', 'friend': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['expName'] = expName

subject_id = expInfo['id']
friend = expInfo['friend']
friend = friend.upper()
cb = expInfo['counterbalance']
cb = int(cb)


wordlist = pd.read_csv('wordlist.csv', sep=',',header=None)
words = wordlist.reindex(np.random.permutation(wordlist.index))
words = words.reset_index(drop=True)
   
#win = visual.Window(fullscr=True)
win = visual.Window((800, 600))


#def qs(win, subject_id):
file_name = "q_" + str(subject_id) + ".csv"
questions = pd.read_csv('self_surveys.csv')
    
win.flip()
message = visual.TextStim(win, text='Press spacebar to begin questionnaires.')
message.setAutoDraw(True) 
win.flip()
event.waitKeys() 
message.setText('') 
win.flip()

ntrials = len(questions)
clicks = []
responses= []
scales = []
for n in range(0,ntrials):
    
    question = questions.loc[n,"question"]
    q_name =  questions.loc[n,"scale"]
    reverse = questions.loc[n,"reverse"]
    start_scale = questions.loc[n,"start_scale"]
    scale_2 = questions.loc[n,"scale_2"]
    scale_3 = questions.loc[n,"scale_3"]
    scale_4 = questions.loc[n,"scale_4"]
    end_scale = questions.loc[n,"end_scale"]
    
    s1 = visual.TextStim(win, text=start_scale, height=.04, units='norm', pos =(-0.6, -0.45))
    s2 = visual.TextStim(win, text=scale_2, height=.04, units='norm', pos = (-0.3, -0.45))
    s3 = visual.TextStim(win, text=scale_3, height=.04, units='norm', pos = (0.0, -0.45))
    s4 = visual.TextStim(win, text=scale_4, height=.04, units='norm', pos = (0.3, -0.45))
    s5 = visual.TextStim(win, text=end_scale, height=.04, units='norm',pos = (0.6, -0.45))

    q_scale = visual.RatingScale(win, low = 1, high = 5, stretch = 2, scale = False, labels = False)

    q = visual.TextStim(win, text=question, height=.10, units='norm')
    print('d')
    while q_scale.noResponse: # show & update until a response has been made
        q.draw()
        s1.draw()
        s2.draw()
        s3.draw()
        s4.draw()
        s5.draw()
        q_scale.draw()
        win.flip()

    q_rating = q_scale.getRating() 
    
    if reverse == 1:
        response = 6 - q_rating
    else: 
        response = q_rating
    
    
    clicks.append(q_rating)
    responses.append(response)
    scales.append(q_name)
    
    win.flip()


print('h')
#save survey data
data = pd.DataFrame({'scale' : scales,
                     'response_clicked' : clicks,
                     'response' : responses})

data.to_csv(file_name, sep=',', index = False, na_rep='na', header=True)

#def task_setup(cb, win):

title = visual.TextStim(win, text = "Word Rating Task")
sp_text = visual.TextStim(win, text="Press the spacebar to continue.", 
                          height=.06,units='norm', 
                          pos =(0.0, -0.4))
title.draw() 
sp_text.draw()
win.flip()
event.waitKeys() 
win.flip()

#decaptilize friends name
low_name = ""
str(low_name)

for l in range(1,len(friend)):
    letter = friend[l]
    low_name = low_name + letter

low_name = low_name.lower()
sf_name = friend[0] + low_name

instruct = "In each trial, you will be presented with a word in the center of the screen. \n \nFor each word you see, you must choose whether it better describes yourself or " + sf_name +  ", as quickly and accurately as possible."
instructions = visual.TextStim(win, text= instruct, 
                          height=.10,units='norm', 
                          alignHoriz='center',                          
                          alignVert = 'center')
sp_text = visual.TextStim(win, text="Press the spacebar to continue.", 
                          height=.06,units='norm', 
                          pos =(0.0, -0.7))
instructions.draw() 
sp_text.draw()
win.flip()
event.waitKeys() 
win.flip()

cb = 1
if cb == 1:
    text = "If the word better describes you, press the J key with your right index finger.\n\nIf the word better describes " + sf_name + ", press the F key with your left index finger. \n\nRemember to answer as quickly and accurately as possible."
    
elif cb == 2:
    text = "If the word better describes you, press the F key with your left index finger.\n\nIf the word better describes "+ sf_name +  ", press the J key with your right index finger. \n\nRemember to answer as quickly and accurately as possible."

instructions = visual.TextStim(win, text, 
                              height=.09,units='norm', 
                              pos =(0.0, 0.1))
sp_text = visual.TextStim(win, text="Press the spacebar to continue.", 
                          height=.06,units='norm', 
                          pos =(0.0, -0.6))
instructions.draw()
sp_text.draw() 
win.flip()
event.waitKeys() 
#win.flip()

sp_text = visual.TextStim(win, text="Press the spacebar to begin 5 practice trials.", 
                          height=.08,units='norm', 
                          pos =(0.0, 0.0))
sp_text.draw()
win.flip()
event.waitKeys()            

#def practice(cb,words,win, friend):

practicewords = ['whimsical', 'open-minded', 'disagreeable',  'intelligent', 'annoying']
for p in range(0,5):
    win.flip()
    core.wait(0.2)
    fixation = visual.TextStim(win, text="+", 
                              height=.10,units='norm', 
                              pos =(0.0, 0.0))
    fixation.draw()
    win.flip()
    core.wait(0.75)
    word = practicewords[p]
    word_text = visual.TextStim(win, text = word,
                                height = .12, units='norm',
                                pos = (0.0, 0.0))
    
    if cb == 1:
        self_text = visual.TextStim(win, text="ME", 
                                      height=.06,units='norm', 
                                      pos =(0.5, -0.4))
        other_text = visual.TextStim(win, text=friend, 
                                      height=.06,units='norm', 
                                      pos =(-0.5, -0.4))
    elif cb == 2:
        self_text = visual.TextStim(win, text="ME", 
                                      height=.06,units='norm', 
                                      pos =(-0.5, -0.4))
        other_text = visual.TextStim(win, text=friend, 
                                      height=.06,units='norm', 
                                      pos = (0.5, -0.4))
     
    self_text.draw()
    other_text.draw()
    word_text.draw()
    win.flip()
    event.waitKeys()
    win.flip()
    
message = visual.TextStim(win, text = "Great! You are done practice. Please ask the experimenter any questions.\n\nAfter you ask any questions, press the spacebar to continue.")
sp_text = visual.TextStim(win, text="Press the spacebar to continue.", 
                         height=.06,units='norm', 
                         pos =(0.0, -0.6))
message.draw()
sp_text.draw()
win.flip()
event.waitKeys()
message = visual.TextStim(win, text = "You will now begin the task. You will complete 4 blocks of 90 trials each. \n\nAfter each block, you can take short break.")
sp_text = visual.TextStim(win, text="Press the spacebar to begin task.", 
                         height=.06,units='norm', 
                        pos =(0.0, -0.6))    
message.draw()
sp_text.draw()
win.flip() 
event.waitKeys() 


#def task(subject_id, cb, words, win, friend):    
  
file_name = "d_" + str(subject_id) + ".csv"

#set up lists to keep track of variables 
ids = []
trial_numbers = [] 
cbs = []
trial_types = []
word_numbers = []
rts = []
key_presses = [] 
responses= []
word_lengths=[]


fixation = visual.TextStim(win, text="+", height=.10,units='norm', pos =(0.0, 0.0))

if cb == 1:
    self_text = visual.TextStim(win, text="ME", 
                                  height=.06,units='norm', 
                                  pos =(0.5, -0.4))
    other_text = visual.TextStim(win, text=friend, 
                                  height=.06,units='norm', 
                                  pos =(-0.5, -0.4))
elif cb == 2:
    self_text = visual.TextStim(win, text="ME", 
                                  height=.06,units='norm', 
                                  pos =(-0.5, -0.4))
    other_text = visual.TextStim(win, text=friend, 
                                  height=.06,units='norm', 
                                  pos = (0.5, -0.4))


ntrials = (len(words))-1 
                       
for x in range(1,ntrials):
    win.flip()
    core.wait(0.3)
    fixation.draw()
    win.flip()
    core.wait(0.75)

    word_number = (words.loc[x,0])
    word = (words.loc[x,1])
    trial_type = words.loc[x,3]
    word_length = len(word)
    
    word_text= visual.TextStim(win, text = word,
                                height = .12, units='norm',
                                pos = (0.0, 0.0))

    self_text.draw()
    other_text.draw()
    word_text.draw()
    win.flip()
    start_time = getTime()
    key_press = event.waitKeys()

    rt = getTime() - start_time
    
    response=[]
    #encode response
    if cb == 1:
        if key_press[0] == 'j':
            response = 1 #self
        elif key_press[0] == "f":
            response = 0 # other
        else: 
            response = "NA" #pressed wrong key
        
        
    elif cb == 2:
        if key_press[0] == "j":
            response = 0 # other
        elif key_press[0] == "f":
            response = 1 # self
        else: 
            response = "NA" #pressed wrong key
    
    #encode responses in a list
        
    ids.append(subject_id)
    trial_numbers.append(x)
    cbs.append(cb)
    trial_types.append(trial_type)
    rts.append(rt)
    key_presses.append(key_press)
    responses.append(response)
    word_numbers.append(word_number)
    word_lengths.append(word_length)
    
    if x % 55 == 0 and x != 0:  
        block_num = int(x/55)
        if block_num == 5:
            sp_text = visual.TextStim(win, text="Press spacebar to end experiment.", height=.06,units='norm', pos =(0.0, -0.6))
        else:
            sp_text = visual.TextStim(win, text="Press the spacebar to begin next block.", height=.06,units='norm', pos =(0.0, -0.6))  
            
            message = visual.TextStim(win, text = "End of block {}/5 blocks".format(block_num))
            message.draw()
            sp_text.draw()
            win.flip()
            event.waitKeys()
        
    
data = pd.DataFrame({'id' :  ids, 
                     'trial_number' : trial_numbers,
                     'counterbalance' : cbs,
                     'trial_type' : trial_types,
                     'word_number': word_numbers,
                     'word_length': word_lengths,
                     'rt' : rts,
                     'key_press' : key_presses,
                     'response': responses})

data.to_csv(file_name, sep=',', index = False, na_rep='na', header=True)
win.close()
core.quit()



# things are over now! 
