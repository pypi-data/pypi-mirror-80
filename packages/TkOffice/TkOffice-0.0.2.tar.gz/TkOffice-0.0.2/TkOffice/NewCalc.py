#new calculator

import tkinter as tk
from tkinter import *

import d
from d import *

import TkOffice
from TkOffice import *
import re
global Eval
Eval = []

def backspace():
    n = len(e.text())
    s = e.getrid(n-1, END)

def negative_returner():
    global exhaust
    ori_val = e.text()
    e.getrid(0,END)
    e.put(1, -(eval(ori_val)))
    exhaust = False

global Eqq
Eqq = False

def Eq():
    global Eval
    global exhaust,Eqq

    exhaust = False
    
    Eval.append(e.text())
    try:
        Anseq = eval("".join(Eval))
        e.getrid(0,END)
        e.put(END, Anseq)
    except:
        e.getrid(0,END)
        e.put(1, "Error")

    e1.getrid(0,END)
    Eqq = True
    Eval= []
    


def screen(x):
    global Eqq
    global exhaust

    
    if exhaust:
        e.getrid(0,END)

    if e.textbox.get()=="0":
        e.textbox.delete(0,END)

    if e1.textbox.get()=="0":
        e1.textbox.delete(0,END)
        
    e.textbox.insert(END, x)
    exhaust = False
    #e1.textbox.insert(END, x)
    
    Eqq= False
    
    ac.button.configure(text = "  C  ")

    minus.change(command = lambda:operator("-"))
    


def dec(x):
    global Eqq
    if Eqq:
        e.getrid(0,END)
        
    if not re.search("\.",e.textbox.get()):
        
        if e.textbox.get()=="":
            e.textbox.insert(END, "0.")
        else:
            e.textbox.insert(END, ".")
        
    Eqq= False



global exhaust
exhaust = True

def operator(x):
    global Eval,Eqq
    global exhaust

    if not exhaust and e.text != "-":
        n = len(Eval)

        value= e.text()
        
        if re.search("\-", value):
            e1.put(END, "("+value+")"+x)
            
        else:
            e1.put(END, value+x)
        e.getrid(0,END)
        #print ("".join(Eval))
        Eval.append(str(eval(value)))
        
        
        Ans = eval("".join(Eval))
        Eval =[]
        Eval.append(str(Ans))
        e.put(1, Ans)
        Eval.append(x)
        #print("".join(Eval))
        exhaust = True

        
        Eqq= False
        
    
def All_Clear():
    global press,Eval
    
    if ac.button['text']=="  C  ":
        if e.text() != "0":


            e.getrid(0,END)
            e.put(1,"0")
        ac.change(text  = "  AC ")

    else:
        if e1.text() != "0":
            e.getrid(0,END)
            e.put(1,"0")
            e1.getrid(0,END)

            minus.change(command = minuser)
    
         
            Eval = []
        ac.change(text  = "  C  ")

    if e.text()=="":
    
        Eval = []



def minuser():
    global exhaust
    exhaust = False
    
    if e.text()=="0":
        e.getrid(0,END)
        e.put(1, "-")
    minus.change(command = lambda:operator("-"))
    


t = ModTk()
t.title("Windows Calculator")
t.configure(bg ="#d6daeb")
t.geometry("450x630")

ef = Frame(t, bg = t["bg"])
ef.pack(fill = X,)


search = Button(ef,bg = t["bg"],fg = "#a0a0a0",bd = 0, bdcolor = "#fcfcfc" ,focuscolorfg = "#313335", text = " \u2630 ", font = "Constantine")
search.pack(side =LEFT, anchor = "w", pady = 10)

ef = Frame(ef, bg = t["bg"])
ef.pack( anchor = "e", padx = 20, pady = 10, side = RIGHT)

sea = Textbox(ef ,bd = 1, justify = LEFT, font = "Consolas 9" , Readme ="Search", bg = "#eeeeee")
sea.grid(row = 0, column = 0)


searchs = Button(ef, bg= "#57a0d3" , bdcolor = "#20639b", fg = "#fcfcfc", pady = 1,bd = 2, text = "Search", font = "Consolas 7")
searchs.grid(row = 0, column = 1, padx = 4, rowspan = 1)

#################################################################################


ef = Frame(t, bg = "#20639B")
ef.pack(fill = X,)

e = Textbox(ef , bg = "#20639B",bd = 2, bdcolor = "#20639b",
            bdactivecolor= "white",fg = "#fcfcfc",focuscolorfg = "#313335",
            focuscolorbg = "#20639b", justify = RIGHT, font = "Consolas 18")


e.put(1, "0")
e.pack(expand = 1, anchor = "e", padx = 20, pady = 10, fill = X)


allpad = Frame(t, bg = t['bg'])
allpad.pack(anchor = "w", padx = 20, pady = 27,fill = X, expand = 0)



e1 = Textbox(allpad , bg = t['bg'],bd = 0,fg = "#a0a0a0",focuscolorfg = "#a0a0a0",focuscolorbg = t['bg'],
             justify = RIGHT, font = "Consolas 8",
             width = 11)
e1.put(1, "0")

e1.pack(fill = BOTH , expand = 1)



allpad = Frame(t, bg = t['bg'])
allpad.pack(anchor = "w", padx = 20, pady = 27)



#########################################################

eq = Button(allpad, text = "      =      ", bg= "#57a0d3" , bdcolor = "#20639b", fg = "#fcfcfc", command = Eq)
eq.grid(row = 1, column = 0, columnspan = 2,padx = 10, pady = 10)


bs = Button(allpad, text = "  ←  ", bg= "#eeeff4", command = backspace)
bs.grid(row = 1, column = 2, padx = 10, pady = 10)




ac = Button(allpad, text = "  C  ", bg= "#eeeff4", command = All_Clear)
ac.grid(row = 1, column = 3, padx = 10, pady = 10)


################################################################

sev = Button(allpad, text = "  7  ", command = lambda :screen(7), bg= "#eeeff4")
sev.grid(row = 2, column = 0, padx = 10, pady = 10)


eig = Button(allpad, text = "  8  ", command = lambda :screen(8), bg= "#eeeff4")
eig.grid(row = 2, column = 1, padx = 10, pady = 10)


nin = Button(allpad, text = "  9  ", command = lambda :screen(9), bg= "#eeeff4")
nin.grid(row = 2, column = 2, padx = 10, pady = 10)


plus = Button(allpad, text = "  +  ", command = lambda: operator("+"), bg= "#eeeff4")
plus.grid(row = 2, column = 3, padx = 10, pady = 10)



#################################################################

fou = Button(allpad, text = "  4  ", command = lambda :screen(4), bg= "#eeeff4")
fou.grid(row = 3, column = 0, padx = 10, pady = 10)


fiv = Button(allpad, text = "  5  ", command = lambda :screen(5), bg= "#eeeff4")
fiv.grid(row = 3, column = 1, padx = 10, pady = 10)


six = Button(allpad, text = "  6  ", command = lambda :screen(6), bg= "#eeeff4")
six.grid(row = 3, column = 2, padx = 10, pady = 10)


minus = Button(allpad, text = "  -  ", command = minuser, bg= "#eeeff4")
minus.grid(row = 3, column = 3, padx = 10, pady = 10)

#################################################################

one = Button(allpad, text = "  1  ", command = lambda :screen(1), bg= "#eeeff4")
one.grid(row = 4, column = 0, padx = 10, pady = 10)


two = Button(allpad, text = "  2  ", command = lambda :screen(2), bg= "#eeeff4")
two.grid(row = 4, column = 1, padx = 10, pady = 10)


thr = Button(allpad, text = "  3  ", command = lambda :screen(3), bg= "#eeeff4")
thr.grid(row = 4, column = 2, padx = 10, pady = 10)


mul = Button(allpad, text = "  *  ", command = lambda: operator("*"), bg= "#eeeff4")
mul.grid(row = 4, column = 3, padx = 10, pady = 10)


#################################################################

zer = Button(allpad, text = "  0  ", command = lambda :screen(0), bg= "#eeeff4")
zer.grid(row = 5, column = 0, padx = 10, pady = 10)


dot = Button(allpad, text = "  .  ", bg="#eeeff4", command  = lambda: dec("."))
dot.grid(row = 5, column = 1, padx = 10, pady = 10)


neg = Button(allpad, text = " +/- ", bg= "#eeeff4", command = negative_returner)
neg.grid(row = 5, column = 2, padx = 10, pady = 10)


div = Button(allpad, text = "  /  ", command = lambda: operator("/"), bg= "#eeeff4")
div.grid(row = 5, column = 3, padx = 10, pady = 10)




t.mainloop()


































