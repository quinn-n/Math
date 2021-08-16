#!/usr/bin/env python
import math
from tkinter import *
class application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()
    def create_widgets(self):
        self.aLabel = Label(self,text="a:")
        self.aLabel.grid(row=0,column=0)
        self.aInput = Entry(self)
        self.aInput.grid(row=0,column=1)
        self.ALabel = Label(self,text="A:")
        self.ALabel.grid(row=1,column=0)
        self.AInput = Entry(self)
        self.AInput.grid(row=1,column=1)
        self.bLabel = Label(self,text="b:")
        self.bLabel.grid(row=2,column=0)
        self.bInput = Entry(self)
        self.bInput.grid(row=2,column=1)
        self.BLabel = Label(self,text="B:")
        self.BLabel.grid(row=3,column=0)
        self.BInput = Entry(self)
        self.BInput.grid(row=3,column=1)

        self.button = Button(self,text="solve")
        self.button["command"] = self.sinLaw
        self.button.grid(row=2,column=2)

        self.outputLabel = Label(self,text="output:")
        self.outputLabel.grid(row=4,column=0)
        self.output = Text(self,width=30,height=1)
        self.output.grid(row=5,column=0,columnspan=3)

    def sinLaw(self):
        self.output.delete(0.0,END)
        a = self.aInput.get()
        A = self.AInput.get()
        b = self.bInput.get()
        B = self.BInput.get()
        if a == "":
            argumentToFind = 1
        elif A == "":
            argumentToFind = 2
        elif b == "":
            argumentToFind = 3
        elif B == "":
            argumentToFind = 4
        if argumentToFind == 1:#find a
            A = math.radians(float(A))#the math library only likes radians
            b = float(b)
            B = math.radians(float(B))
            solution = (b*math.sin(A))/math.sin(B)
        elif argumentToFind == 2:#find A
            a = float(a)
            b = float(b)
            B = math.radians(float(B))
            solution = math.degrees(math.asin((a*math.sin(B))/b))
        elif argumentToFind == 3:#find b
            a = float(a)
            A = math.radians(float(A))
            B = math.radians(float(B))
            solution = (a*math.sin(B))/math.sin(A)
        elif argumentToFind == 4:#find B
            a = float(a)
            A = math.radians(float(A))
            b = float(b)
            solution = math.degrees(math.asin((b*math.sin(A))/a))
        self.output.insert(0.0,str(solution))
root = Tk()
app = application(root)
root.geometry("350x150")
root.title("sine law")
root.mainloop()
