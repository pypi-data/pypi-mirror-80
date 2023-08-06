
import tkinter as tk
from tkinter import *
import TkOffice
from TkOffice import *
import numpy
import base64
import io
import os
import numpy as np
import webbrowser
import random
import re
import platform
import PIL
from PIL import ImageTk,Image


#New
#Here is a langauge written in tk.tk

#New_Supported Class
#package_is_C#
class Card(tk.Frame):

    bdcolor = "#a0a0a0"
    hoverbdcolor ="#ABD7EB"
    hovercolor = "#eff"
    ori = ""
    bd = 2
    com = None
    __ani = True
    
    def command(self, event):
        try:
            return self.com()
        except:pass
    
    #hover effect

    def addWidgetTo(self , widgetx):
        self.__widget.append(widgetx)


    def __hover( self, event):

        self.configure(bg = self.hoverbdcolor)
        self.fbox.configure(bg = self.hovercolor)
        self.functionframe.configure(bg = self.hovercolor)
        self.contentframe.configure(bg = self.hovercolor)

        if len(self.__widget) >0:
            for i in self.__widget:
                i.configure(bg= self.hovercolor)


    def __unhover( self, event):

        self.configure(bg = self.bdcolor)
        self.fbox.configure(bg = self.ori)
        self.functionframe.configure(bg = self.ori)
        self.contentframe.configure(bg = self.ori)
        if len(self.__widget) >0:
            for i in self.__widget:
                i.configure(bg= self.ori)
    
    def __check_ups(self):

        if len(self.__widget) >0:
            for i in self.__widget:
                i.bind("<Button-1>" , self.command)
        self.after(1000 , self.__check_ups)


    def __init__(self, master ,**kw):
        self.__widget = []

        try:
            self.bdcolor = kw['bdcolor']
            kw.pop('bdcolor')
        except:
            pass

        try:
            self.com = kw['command']
            kw.pop('command')
        except:
            pass



        try:
            self.hoverbdcolor = kw['activebdcolor']
            kw.pop('activebdcolor')
        except:
            pass



        try:
            self.bd = kw['bd']
            kw.pop('bd')


        except:
            pass	

        try:
            self.__ani = kw['animation']
            kw.pop('animation')
        except:pass



        tk.Frame.__init__(self, master)

        

        self.fbox = Frame(self , kw)
        self.fbox.pack(fill = BOTH , padx = self.bd, pady = self.bd, expand = 1)



        self.contentframe = Frame(self.fbox , bg = self.fbox['bg'])
        self.contentframe.pack(fill = BOTH , expand = 1)

        self.contentframe.bind("<Button-1>", self.command)


        self.functionframe = Frame(self.fbox, bg = self.fbox['bg'])
        self.functionframe.pack(fill = BOTH , expand = 1)
        self.functionframe.bind("<Button-1>", self.command)

        self.ori = self.fbox['bg']
        
        if self.__ani:
            self.after(1000 , self.__check_ups)
            self.fbox.bind('<Enter>', self.__hover)
            self.fbox.bind('<Leave>', self.__unhover)


        self.configure(bg = self.bdcolor)


    def rebuild(self, **kw):

        try:
            self.bdcolor = kw['bdcolor']
            kw.pop('bdcolor')
        except:
            pass

        try:
            self.com = kw['command']
            kw.pop('command')
        except:
            pass



        try:
            self.hoverbdcolor = kw['activebdcolor']
            kw.pop('activebdcolor')
        except:
            pass



        try:
            self.bd = kw['bd']
            kw.pop('bd')


        except:
            pass    

        try:
            self.animation = kw['animation']
            kw.pop('animation')
        
        except:pass
        
        self.fbox.configure(kw)
        self.functionframe.configure(kw)
        self.contentframe.configure(kw)
