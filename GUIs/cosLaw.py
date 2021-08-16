#!/usr/bin/env python
import math
from tkinter import *

class application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()
    def create_widgets(self):
        self.cLabel = Label(self,text="c:")
        self.cLabel.grid(row=0,column=0)
        self.cInput = Entry(self)
        self.cInput.grid(row=0,column=1)
        self.aLabel = Label(self,text="a:")
        self.aLabel.grid(row=1,column=0)
        self.aInput = Entry(self)
        self.aInput.grid(row=1,column=1)
        self.bLabel = Label(self,text="b:")
        self.bLabel.grid(row=2,column=0)
        self.bInput = Entry(self)
        self.bInput.grid(row=2,column=1)
        self.CLabel = Label(self,text="C:")
        self.CLabel.grid(row=3,column=0)
        self.CInput = Entry(self)
        self.CInput.grid(row=3,column=1)

        self.button = Button(self,text="solve")
        self.button["command"] = self.cosLaw
        self.button.grid(row=2,column=2)

        self.output = Text(self,width=30,height=1)
        self.output.grid(row=4,column=0,columnspan=3)

    def cosLaw(self):
        self.output.delete(0.0,END)
        c = self.cInput.get()
        a = self.aInput.get()
        b = self.bInput.get()
        C = self.CInput.get()
        if c == "":
            argumentToFind = 1
        elif C == "":
            argumentToFind = 2
        if argumentToFind == 1:#find c
            print("finding c...")
            a = float(a)
            b = float(b)
            C = math.radians(float(C))
            solution = math.sqrt(a*a+b*b-2*a*b*math.cos(C))
        elif argumentToFind == 2:#find C
            print("finding C...")
            c = float(c)
            a = float(a)
            b = float(b)
            solution = math.degrees(math.acos((c*c-(a*a+b*b))/(-2*a*b)))
        self.output.insert(0.0,str(solution))
root = Tk()
app = application(root)
root.geometry("250x125")
root.title("cosine law")
root.mainloop()
