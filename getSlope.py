#!/usr/bin/env python3
import sys

varLetters = "abcdefghijklmnopqrstuvwxyz"
knownVars = []
numVars = 0

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <equation> <[dx]>")
    print("Gets the slope at a position of a line (usually curved) on a graph.")
    sys.exit()

def isVar(char):
    for var in varLetters:
        if char == var:
            return True
            knownVars += char
    return False

def isIn(array, search):
    for element in array:
        if element == search:
            return True
    return False

def breakupEquation(equationStr):
    equation = ""
    numVars = 0
    for char in equationStr:
        if isVar(char):
            equation += "V"
#            numVars += 1
#            knownVars.append(char)
        elif char == "^":
            equation += "**"
        else:
            equation += char
    return equation

if len(sys.argv) > 2:
    dx = float(sys.argv[2])
else:
    dx = .001

equationStr = sys.argv[1]
equation = breakupEquation(equationStr)

point = float(input("What point (x) would you like to find the slope for?\n>> "))
finalY1Equation = ""
finalY2Equation = ""
for equ in equation:
    if equ == "V":
        finalY1Equation += str(point)
        finalY2Equation += str(point + dx)
    else:
        finalY1Equation += equ
        finalY2Equation += equ

y1 = eval(finalY1Equation)
y2 = eval(finalY2Equation)

slope = (y1-y2) / dx

print("Get rise: " + str(y1-y1) + ", and run: " + str(dx))

print("Got slope: "+str(slope))
