
import tkinter as tk
from tkinter import *

import TkOffice
from TkOffice import *
global acc
acc = False

def Acc():
    global acc
    if not acc:
        fr = Frame(T, bg = T['bg'])
        fr.pack(fill = X)

        l4 = Label(fr, fg = "#fcfcfc", bg = fr['bg'], text = "Note:")
        l4.pack(fill = X,padx = 20, pady = 20,expand = 1,side = LEFT)

        t = Textbox(fr, bd= 2 ,padding= 3, isReadonly = 1, Readme = "ReadMe.md", )
        t.pack(fill = X,padx = 20, pady = 20,expand = 1,side = LEFT)
        t.change(bd = 1, isReadonly = 0, Readme = "Add Your notes" ,font = "Segoe 9")


        fr = Frame(T, bg = T['bg'])
        fr.pack( anchor = "ne")

        app = Button(fr, bd=2,fg = "#fcfcfc",  bg= "#3d3d3d" , text = "Apply Form")
        app.grid(row = 0, column = 0,pady = 20, padx = 10,sticky = E )

        more = Button(fr,bd=2, fg = "#fcfcfc",  bg= "#3d3d3d" , text = "More...")
        more.grid(row = 0, column = 1, padx = 10, pady = 20,sticky = E)
    acc = True
    
    m_1dec.change(state = "disabled")

def des():
    return

def reset():
    
    
    global frc


    t.change(bd = 2, Readme = "" ,font = "Segoe 9", bg = "#3d3d3d", fg = "#fcfcfc")

    t1.change(bd = 2,  Readme = "" ,font = "Segoe 9", bg = "#3d3d3d", fg = "#fcfcfc")



    t2.change(bd = 2, Readme = "" ,font = "Segoe 9", bg = "#3d3d3d", fg = "#fcfcfc")

    m.change(state = NORMAL, bg = "#3d3d3d", command = Acc)

    m_1dec.change(state = NORMAL,bg = "#3d3d3d", fg = "#e3242b",)
    frc.destroy()

    

def Dec():
    global frc

    frc = Frame(T, bg = T['bg'])
    frc.pack(fill = X)

    lde =Alert(frc, bg = fr['bg'], text = "You are not allowed to access" ,fg ="#e3242b")
    lde.pack(fill = X,padx = 20, pady = 20,expand = 1)


    res = Button(frc, bg = "#3d3d3d", fg = "yellow", text = "   Reset   ", command = reset)
    res.pack()

    m.change(command = des)
    m_1dec.change(state = DISABLED)
    

To = ModTk()
To.configure(bg = "#222222")
To.tk.call("tk","scaling", 2.9)
To.title("survey")
'''
import ctypes
import os


if os.name == "nt":
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
    print("True")

    
'''

T = Frame(To, bg = To['bg'])
T.pack(fill = BOTH)

l = Label(T, fg = "#fcfcfc", bg=  T['bg'], text = "Survey", font = "Consolas 19")
l.pack(fill =  X, expand = 1)


fr = Frame(T, bg = T['bg'])
fr.pack(fill = X, anchor = "w")

l = Label(fr, fg = "#fcfcfc",bg = fr['bg'], text = "Name:             ")
l.pack(fill = X,padx = 20, pady = 20,expand = 0,side = LEFT, anchor = "w")

t = Textbox(fr, bd= 2, bg = "#3d3d3d" ,padding= 3, Readme = "ReadMe.md", )
t.pack(fill = X,padx = 20, pady = 20,expand = 1,side = RIGHT, anchor = "e")
t.change(bd = 2, Readme = "Name Here" ,font = "Segoe 9", bg = "#3d3d3d", fg = "#fcfcfc")

fr = Frame(T, bg = T['bg'])
fr.pack(fill = X, anchor = "w")

l1 = Label(fr, fg = "#fcfcfc", bg = fr['bg'], text = "Occupation:    ")
l1.pack(fill = X,padx = 20, pady = 20,expand = 0,side = LEFT, anchor = "w")

t1 = Textbox(fr, bg = "#3d3d3d", bd= 2 ,padding= 3,  Readme = "ReadMe.md", )
t1.pack(fill = X,padx = 19, pady = 20,expand = 1,side = RIGHT, anchor = "e")
t1.change(bd = 2,  Readme = "Job" ,font = "Segoe 9", bg = "#3d3d3d", fg = "#fcfcfc")


fr = Frame(T, bg = T['bg'])
fr.pack(fill = X, anchor = "w")

l2 = Label(fr, fg = "#fcfcfc", bg = fr['bg'], text = "Reason to join:")
l2.pack(fill = X,padx = 19, pady = 20,expand = 0,side = LEFT, anchor = "w")

t2 = Textbox(fr, bg = "#3d3d3d", bd= 2 ,padding= 3, Readme = "ReadMe.md", )
t2.pack(fill = X,padx = 17, pady = 20,expand = 1,side =RIGHT, anchor = "e")
t2.change(bd = 2, Readme = "Reaon must be given" ,font = "Segoe 9", bg = "#3d3d3d", fg = "#fcfcfc")



fr = Frame(T, bg = T['bg'])
fr.pack( anchor = "nw", padx = 20)

l3 = Label(fr, fg = "#fcfcfc", bg = fr['bg'], text = "Course:")
l3.grid(row = 0, column = 0,pady = 20, padx = 10,sticky = W )


lr = Label(fr, fg = "#fcfcfc", bg = fr['bg'], text = "Registered Date:")
lr.grid(row = 0, column = 1,pady = 20, padx = 10,sticky = E )


co = Combobox(fr,bg = "#3d3d3d", fg = "#fcfcfc", bd= 2 ,padding= 3, access = To, Readme = "GUI Development", width= 18 , isReadonly = False,  font = "Segoe 9")
co.val = ['Django', "Spring", "Angular", "WPF", "Tkinter", "PyQt", "kivy"]
co.grid(row = 1, column = 0,pady = 20, padx = 10,sticky = E )


date =Textbox(fr, fg = "#fcfcfc", bg = "#3d3d3d", bd= 2 ,padding= 3, isReadonly = 1, Readme = "19.9.2020", width = 12)
date.grid(row = 1, column = 1, padx = 10, pady = 20,sticky = E)


fr = Frame(T, bg = T['bg'])
fr.pack(anchor ="w",padx = 20,expand = 1)

lw = Alert(fr, bg ="#3d3d3d",font= "Arial 8", fg = "#f9d71c",
          text = "I do Accept the terms of the Agreements\nnot to discriminate others\nBut to create a better society")
lw.pack(fill = BOTH,expand = 1)


fr = Frame(T, bg = T['bg'])
fr.pack( anchor = "ne")

m = Button(fr,bg = "#3d3d3d", text = "Accept", fg= "#73c2fb", bd=2, command = Acc)
m.grid(row = 0, column = 0,pady = 20, padx = 10,sticky = E )




m_1dec = Button(fr,bg = "#3d3d3d", text = "Decline..",fg ="#e3242b",bd=2, activeforeground = "red", command = Dec)
m_1dec.grid(row = 0, column = 1, padx = 10, pady = 20,sticky = E)


'''
fr = Frame(T, bg = T['bg'])
fr.pack(fill = X)

l = Label(fr, bg = fr['bg'], text = "Note:")
l.pack(fill = X,padx = 20, pady = 20,expand = 1,side = LEFT)

t = Textbox(fr, bd= 2 ,padding= 3, isReadonly = 1, Readme = "ReadMe.md", )
t.pack(fill = X,padx = 20, pady = 20,expand = 1,side = LEFT)
t.change(bd = 1, isReadonly = 0, Readme = "" ,font = "Segoe 9",)


fr = Frame(T, bg = T['bg'])
fr.pack( anchor = "ne")

m = Button(fr,  bg= "#eee" , text = "Apply Form")
m.grid(row = 0, column = 0,pady = 20, padx = 10,sticky = E )




m_1 = Button(fr,  bg= "#eee" , text = "More...")
m_1.grid(row = 0, column = 1, padx = 10, pady = 20,sticky = E)

'''

#To.resizable(False, False)

To.mainloop()

































