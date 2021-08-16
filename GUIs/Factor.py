#!/usr/bin/env python
import sys
import math
from tkinter import *

maxFactorCheck = 5000

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
        self.bLabel = Label(self,text="b:")
        self.bLabel.grid(row=1,column=0)
        self.bInput = Entry(self)
        self.bInput.grid(row=1,column=1)
        self.cLabel = Label(self,text="c:")
        self.cLabel.grid(row=2,column=0)
        self.cInput = Entry(self)
        self.cInput.grid(row=2,column=1)

        self.button = Button(self,text="Factor")
        self.button.grid(row=1,column=2,sticky=W)
        self.button["command"] = self.factorFloat

        self.outputLabel = Label(self,text="Factor(s):")
        self.outputLabel.grid(row=3,column=0)
        self.output = Text(self,width=30,height=3)
        self.output.grid(row=4,column=0,columnspan=3)
    def lCM(self,num1,num2,max=500): #finds the lowest common multiple, checking up to max
        num1 = float(num1)
        num2 = float(num2)
        for loop in range(int(float((max+1)/-1)),0): #we have to add 1 to make it play nicely with range(), and flip it to make sure we get the largest value possible.
            loop = loop/-1
            if num1%loop == 0 and num2%loop == 0:
                lcm = loop
                break
        try:
            return float(lcm)
        except:
            return None
    def factorFloat(self):
        self.output.delete(0.0,END)
        firstNum = float(self.aInput.get())
        secondNum = float(self.bInput.get())
        thirdNum = float(self.cInput.get())
        oldFirstNum = firstNum
        oldSecondNum = secondNum
        oldThirdNum = thirdNum
        if firstNum.is_integer() and secondNum.is_integer() and thirdNum.is_integer():
            decimal = False
            multiplier = 1
        else:
            decimal = True
            multiplier = 10
        while decimal: #if one of our numbers is a decimal, multiply it by 10, then 100, then 1000 & so on until there is no decimal.
            firstNum = oldFirstNum*multiplier
            secondNum = oldSecondNum*multiplier
            thirdNum = oldThirdNum*multiplier
            if firstNum.is_integer() and secondNum.is_integer() and thirdNum.is_integer():
                decimal = False
            else:
                multiplier = multiplier*10
        
        multiplied = firstNum*thirdNum
        
        negative = False
        if multiplied < 0: #we can't find the square root of a negative number!
            multiplied = multiplied/-1
            negative = True
        
        sqrt = math.sqrt(multiplied) #find the square root
        floor = float(math.floor(sqrt)) 
        #round down to the nearest int
        
        if negative: #flip the number back around if it was negative
            multiplied = multiplied/-1
        
        firstSetNums = []
        secondSetNums = []
        #get the combination(s) of two numbers that add to b and multiply to ac.
        for loopNum in range(1, int(floor+1)): 
        #we have to add 1 to floor to make it play well with range()
            cacheNum = multiplied/loopNum #store a number we're working with in cacheNum
            if secondNum == loopNum+cacheNum:
                firstSetNums.append(cacheNum)
                secondSetNums.append(loopNum)
            elif secondNum == cacheNum-loopNum or secondNum == loopNum-cacheNum:
                firstSetNums.append(cacheNum)
                secondSetNums.append(loopNum/-1)
            elif secondNum == (loopNum+cacheNum)/-1:
                firstSetNums.append(cacheNum/-1)
                secondSetNums.append(loopNum/-1)
        try: #make sure that the equation has been factored. If it has not, it is not factorable (at least with this script)
            if firstSetNums == None or secondSetNums == None:
                self.output.insert(0.0,"Equation not factorable.")
                sys.exit()
        except:
            self.output.insert(0.0,"Equation not factorable.")
            sys.exit()
        
    #equation:     firstNum(x^2)+firstSetNum*x+secondSetNum*x+thirdNum
        
    
        finalFactors = []
        #find bracket multipliers
        for i in range(len(firstSetNums)): #we can use both firstSetNums or secondSetNums here, they should both be the same length.
            firstSetNum = firstSetNums[i]
            secondSetNum = secondSetNums[i]
            firstBracketMult = self.lCM(firstNum,firstSetNum,maxFactorCheck) #get numbers that multiply into the brackets.
            secondBracketMult = self.lCM(thirdNum,secondSetNum,maxFactorCheck)
            backwards = False
            if firstBracketMult == None or secondBracketMult == None: #check to see if our SetNums work in the other positions, if they did not work in the first
                firstBracketMult = self.lCM(firstNum,secondSetNum,maxFactorCheck)
                secondBracketMult = self.lCM(thirdNum,firstSetNum,maxFactorCheck)
                backwards = True
            if firstBracketMult == None or secondBracketMult == None:
#                print("Error: either your equation is not factorable or something is coded wrong. However it is more likely that something is coded wrong than your factoring thing. You might want to double check.")
                sys.exit()
        
            #this portion is all about us getting the final revolution of the factored equation and presenting it the right way.
            #get the first versions of our first & second brackets.
            firstBracket = "("+str(float(firstNum/firstBracketMult))+"x"+"+"+str(float(firstSetNum/firstBracketMult))+")"
            secondBracket = "("+str(float(secondSetNum/secondBracketMult))+"x"+"+"+str(float(thirdNum/secondBracketMult))+")"
            firstAndSecondEqual = True
            if firstBracket != secondBracket: #check if our first bracket is equal to our second bracket
                firstAndSecondEqual = False
                if secondBracket == "("+str(float(firstNum/firstBracketMult/-1))+"x+"+str(float(firstSetNum/firstBracketMult/-1))+")":
        #check if the second bracket is equal to the first bracket with the intigers flipped.
                    firstBracket = "("+str(float(firstNum/firstBracketMult/-1))+"x+"+str(float(firstSetNum/firstBracketMult/-1))+")"
                    firstBracketMult = firstBracketMult/-1
                    firstAndSecondEqual = True
        
            if not firstAndSecondEqual: #if our brackets aren't the same, we can print them with
                if not backwards: #store what we will print in an array finalFactors, in case we want to do something with it later.
                    finalFactors.append(str(float(firstBracketMult/multiplier))+"x"+firstBracket+"+"+str(secondBracketMult)+secondBracket)
                elif backwards:
                    finalFactors.append(str(float(firstBracketMult/multiplier))+"x"+"("+str(float(firstNum/firstBracket))+"x+"+str(float(secondSetNum/firstBracket))+")+"+str(secondBracket)+"("+str(float(firstSetNum/secondBracket))+"x+"+str(float(thirdNum/secondBracket)))
            else: #if our brackets are the same, we can factor further.
                if self.lCM(firstBracketMult,secondBracketMult) != 1: #if the numbers in our first bracket can be factored, let it be so.
                    commonMultiple = self.lCM(firstBracketMult,secondBracketMult)
                    finalFactors.append(str(commonMultiple/multiplier)+"("+str(firstBracketMult/commonMultiple)+"x"+"+"+str(secondBracketMult/commonMultiple)+")"+firstBracket)
                else:
                    if multiplier == 1: #if our multiplier is 1, we do not need to print a fraction in front of the rest of the equation.
                        finalFactors.append("("+str(firstBracketMult)+"x"+"+"+str(secondBracketMult)+")"+firstBracket) #we can use any bracket here; so long as it matches whichever multiplier got divided by 1. They should be the same.
                    else:
                        finalFactors.append("1/"+str(multiplier)+"("+str(firstBracketMult)+"x"+"+"+str(secondBracketMult)+")"+firstBracket) #we can use any bracket here; so long as it matches whichever multiplier got divided by -1. They should be the same.
        
        for finalFactor in finalFactors: #loop through all our final factors
            self.output.insert(0.0,finalFactor)

root = Tk()
app = application(root)
root.title("Factor")
root.geometry("350x150")
root.mainloop()
