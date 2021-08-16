#!/usr/bin/env python3
import sys

nums = [0,1,2,3,4,5,6,7,8,9]
chars="abcdefghijklmnopqrstuvwxyz"

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <equation>")
    sys.exit()

def getType(char):
    if char == "(":
        return "openBracket"
    elif char == ")":
        return "closedBracket"
    elif char == "^":
        return "power"
    elif char == "*" or char == "/" or char == "+" or char == "-":
        return "operation"

    for var in chars:
        if char == var:
            return "var"
    for num in nums:
        if int(char) == num:
            return "num"
    return None

strEquation = sys.argv[1]
#find the location of the variables
vars = []
varLetters = []
equation = ""
for char in strEquation:
    elementType = getType(char)
    if elementType == None:
        print("Warning: Unknown char"+char+". Continuing...")
    else:
        if elementType != "var":
            if elementType != "power":
                equation += char
            else:
                equation += "**"
        else:
            vars.append(0)
            varLetters.append(char)
            equation += "V"
while True:
    #get variables
    numVars = len(vars)
    for i in range(numVars):
        vars[i] = (float(input("Please enter value for "+varLetters[i]+" ("+str([i])+")\n>> ")))
    #substitute variables into equation
    evalEquation = ""
    numVars = 0
    for e in equation:
        if e == "V":
            evalEquation += str(vars[numVars])
            numVars += 1
        else:
            evalEquation += e

    result = eval(evalEquation)
    print("Result: "+str(result))
