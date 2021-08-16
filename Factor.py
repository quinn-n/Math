#!/usr/bin/env python3
"""
If you're reading this, I'm sorry. This is one of the first things I've written in python years ago and it's really shitty, but it works.
I even named a loop after a line number at one point. That didn't work out immediately after I changed any of the code before the loop.
I'm not planning on making large changes anytime soon because I like to look back to where I started.
(Regrettably) written by happylego91
I have no idea when this was 'finalized'. Late 2017ish I think.
Jan. 11th 2020 - Added source header
"""
import sys
import math

maxFactorCheck = 100000
#see which variables we have been given
if len(sys.argv) == 3:
    firstNum = float(sys.argv[1])
    secondNum = 0.
    thirdNum = float(sys.argv[2])
    variableName = "x" #make sure we have a variable name
elif len(sys.argv) == 4:
    firstNum = float(sys.argv[1])
    secondNum = float(sys.argv[2])
    thirdNum = float(sys.argv[3])
    variableName = "x" #make sure we have a variable name
elif len(sys.argv) == 5:
    firstNum = float(sys.argv[1])
    secondNum = float(sys.argv[2])
    thirdNum = float(sys.argv[3])
    variableName = sys.argv[4]
else: #if an invalid number of arguments were given, print errors.
    print("Usage: FactorFloat.py <a> [b] <c> [variable name]")
    print("ax^2 + bx + c variable")
    print("Like Factor.py, but with more support for decimals.")
    print("Example: FactorFloat.py 1 3 2 f")
    print("Or: FactorFloat.py 1 3 2")
    sys.exit()

#here we add the first part that has support for decimal numbers.
oldFirstNum = firstNum
oldSecondNum = secondNum
oldThirdNum = thirdNum
if firstNum.is_integer() and secondNum.is_integer() and thirdNum.is_integer():
    decimal = False
    print("No decimals found.")
    multiplier = 1
else:
    decimal = True
    print("Decimals found.")
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

print("found a: "+str(firstNum)+" found b: "+str(secondNum)+" found c: "+str(thirdNum))
print("Looping through 1 - "+str(floor))

firstSetNums = []
secondSetNums = []
#get the combination(s) of two numbers that add to b and multiply to ac.
for loopNum in range(1, int(floor+1)): 
#we have to add 1 to floor to make it play well with range()
    cacheNum = multiplied/loopNum #store a number we're working with in cacheNum
    if secondNum == loopNum+cacheNum:
        print("first number: "+str(cacheNum)+" second number: "+str(loopNum))
        firstSetNums.append(cacheNum)
        secondSetNums.append(loopNum)
    elif secondNum == cacheNum-loopNum or secondNum == loopNum-cacheNum:
        print("first number: "+str(cacheNum)+" second number: "+str(loopNum/-1))
        firstSetNums.append(cacheNum)
        secondSetNums.append(loopNum/-1)
    elif secondNum == (loopNum+cacheNum)/-1:
        print("first number: "+str(cacheNum/-1)+" second number: "+str(loopNum/-1))
        firstSetNums.append(cacheNum/-1)
        secondSetNums.append(loopNum/-1)
try: #make sure that the equation has been factored. If it has not, it is not factorable (at least with this script)
    if firstSetNums == None or secondSetNums == None:
        print("Equation not factorable.")
        sys.exit()
except:
    print("Equation not factorable.")
    sys.exit()

#equation:     firstNum(x^2)+firstSetNum*x+secondSetNum*x+thirdNum

def lCM(num1,num2,max=1000): #finds the lowest common multiple, checking up to max
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

finalFactors = []
for loopCount87 in range(len(firstSetNums)): #we can use both firstSetNums or secondSetNums here, they should both be the same length.
    firstSetNum = firstSetNums[loopCount87]
    secondSetNum = secondSetNums[loopCount87]
    firstBracketMult = lCM(firstNum,firstSetNum,maxFactorCheck) #get numbers that multiply into the brackets.
    secondBracketMult = lCM(thirdNum,secondSetNum,maxFactorCheck)
    backwards = False
    if firstBracketMult == None or secondBracketMult == None: #check to see if our SetNums work in the other positions, if they did not work in the first
        firstBracketMult = lCM(firstNum,secondSetNum,maxFactorCheck)
        secondBracketMult = lCM(thirdNum,firstSetNum,maxFactorCheck)
        backwards = True
    if firstBracketMult == None or secondBracketMult == None:
        print("Error: either your equation is not factorable or something is coded wrong. However it is more likely that something is coded wrong than your factoring thing. You might want to double check.")
        sys.exit()

    #this portion is all about us getting the final revolution of the factored equation and presenting it the right way.
    #get the first versions of our first & second brackets.
    firstBracket = "("+str(float(firstNum/firstBracketMult))+variableName+"+"+str(float(firstSetNum/firstBracketMult))+")"
    secondBracket = "("+str(float(secondSetNum/secondBracketMult))+variableName+"+"+str(float(thirdNum/secondBracketMult))+")"
    firstAndSecondEqual = True
    if firstBracket != secondBracket: #check if our first bracket is equal to our second bracket
        firstAndSecondEqual = False
        if secondBracket == "("+str(float(firstNum/firstBracketMult/-1))+variableName+"+"+str(float(firstSetNum/firstBracketMult/-1))+")":
#check if the second bracket is equal to the first bracket with the intigers flipped.
            firstBracket = "("+str(float(firstNum/firstBracketMult/-1))+ variableName + "+"+str(float(firstSetNum/firstBracketMult/-1))+")"
            firstBracketMult = firstBracketMult/-1
            firstAndSecondEqual = True

    if not firstAndSecondEqual: #if our brackets aren't the same, we can print them with
        if not backwards: #store what we will print in an array finalFactors, in case we want to do something with it later.
            finalFactors.append(str(float(firstBracketMult/multiplier))+variableName+firstBracket+"+"+str(secondBracketMult)+secondBracket)
        elif backwards:
            finalFactors.append(str(float(firstBracketMult/multiplier))+variableName+"("+str(float(firstNum/firstBracket))+variableName+"+"+str(float(secondSetNum/firstBracket))+")+"+str(secondBracketMult)+"("+str(float(firstSetNum/secondBracketMult))+variableName+"+"+str(float(thirdNum/secondBracketMult)))
    else: #if our brackets are the same, we can factor further.
        if lCM(firstBracketMult,secondBracketMult) != 1: #if the numbers in our first bracket can be factored, let it be so.
            commonMultiple = lCM(firstBracketMult,secondBracketMult)
            finalFactors.append(str(commonMultiple/multiplier)+"("+str(firstBracketMult/commonMultiple)+variableName+"+"+str(secondBracketMult/commonMultiple)+")"+firstBracket)
        else:
            if multiplier == 1: #if our multiplier is 1, we do not need to print a fraction in front of the rest of the equation.
                finalFactors.append("("+str(firstBracketMult)+variableName+"+"+str(secondBracketMult)+")"+firstBracket) #we can use any bracket here; so long as it matches whichever multiplier got divided by 1. They should be the same.
            else:
                finalFactors.append("1/"+str(multiplier)+"("+str(firstBracketMult)+variableName+"+"+str(secondBracketMult)+")"+firstBracket) #we can use any bracket here; so long as it matches whichever multiplier got divided by -1. They should be the same.

print("Factor(s):")
for finalFactor in finalFactors: #loop through all our final factors
    print(finalFactor)
