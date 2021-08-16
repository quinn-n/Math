#!/usr/bin/env python3
from sys import argv
maxLcm = 1000
#import math

chars = "abcdefghijklmnopqrstuvwxyz"
nums = range(10)
operators = "+-*/"

if len(argv) < 2:*
    print("Usage: "+argv[0]+" <equation>")
    print("Factors an equation. Hopefully. That's the plan anyways.")
    exit()

def getType(char):
    for c in chars:
        if char == c:
            return "var"
    for num in nums:
        if int(char) == num:
            return "num"
    if char == "(":
        return "("
    elif char == ")":
        return ")"
    elif char == "^":
        return "^"
    elif char == ".":
        return "."
    for op in operators:
        if char == op:
            return "operator"

def getNumAtPos(equation, pos): #gets the number after a position. Useful for finding the number after an operation (eg. ^, +, /)
    strNum = ""
    startPos = pos
    elementType = getType(equation[pos])
    while elementType == "num" or elementType == ".":
        strNum += equation[pos]
    return float(strNum), pos - startPos

def hasVar(term,num): #return true if said term has a variable.
    if term["vars"][num] == "":
        return True
    else:
        return False

def isInt(num):
    if num % 1 == 0:
        return True
    else:
        return False

def isIn(string, char):
    strLen = len(string)
    for i in range(strLen):
        if string[i] == char:
            return True
    return False

def getLcm(terms): #get the lowest common multiple
    numTerms = len(terms)
    lcm = 0
    for multiple in range(maxLcm,0,-1):
        works = True
        for termNum in range(numTerms):
            for currentNum in range(termNums[0]["nums"]):
                if not isInt(terms[termNum]["nums"][currentNum] / multiple):
                    works = False
        if works:
            return multiple

def commonFactor(terms,termNum):
    numNums = len(terms[termNum]["nums"])
    termMultipliers = []
    
    i = 0
    while i < numNums:
        while n < numNums:
            if n != i:
                if terms[termNum]["vars"][i]

terms = []
currentBracket = 0
currentNum = 0
rawEquation = argv[1:]

template = {"nums":[],"vars":[],"powers":[],"operators":[]}

equationLen = len(rawEquation)
equationNum = 0
while equationNum < equationLen:
    element = rawEquation[equationLen]
    elementType = getType(element)
    if elementType == "(": #setup terms with a new template & defaults.
        terms.append(template)
        currentNum = 0
        terms[equationNum]["nums"][currentNum] = 1
        terms[equationNum]["powers"][currentNum] = 1
        terms[equationNum]["vars"][currentNum] = ""
        terms[equationNum]["operators"][currentNum] = "+"
    elif elementType == ")":
        currentBracket += 1
    elif elementType == "^":
        power, numsSkipped = getNumAtPos(rawEquation, equationNum + 1)
        terms[currentBracket]["powers"][currentNum] = power
        equationNum += numsSkipped + 1
    elif elementType == "var":
        terms[currentBracket]["vars"][currentNum] += element
    elif elementType == "operator":
        terms[currentBracket]["operators"][currentNum] = element
        currentNum += 1
    elif elementType == "num":
        if terms[currentBracket]["nums"][currentNum] == 1:
            terms[currentBracket]["nums"][currentNum] = getNumAtPos(rawEquation, equationNum)
    equationNum += 1


