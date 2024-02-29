#!/usr/bin/env python3

from projectModules import GraphicalUserInterface as gui
from tkinter import *
from os import getcwd
from os.path import join

def socialmedia():
    global rootwindow, session_userid, isloggedin
    
    # define a title for the window
    rootwindow.title("Social Media")
    
    # get control
    control = gui.generate(rootwindow, join(getcwd(), 'images'))
    # get login/register values
    control._start()
    
if __name__=="__main__":
    session_userid = ""
    isloggedin = False
    rootwindow = Tk()
    socialmedia()
    rootwindow.mainloop()