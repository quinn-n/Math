#!/usr/bin/env python
"""
Written and maintained by happylego91. https://gitlab.com/happylego91

"""
from sys import argv
import math
import copy

maxLcm = 1000

chars = "abcdefghijklmnopqrstuvwxyz"
nums = range(10)
operators = "+-*/"

if len(argv) < 2:
    print("Usage: "+argv[0]+" <equation>")
    print("Factors an equation. Hopefully. That's the plan anyways.")
    print("Example: '(3x+3)' should return 3(x+1)")
    exit()

def getType(char):
    for c in chars:
        if char == c:
            return "var"
    for num in nums:
        if char == str(num):
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

class term:
    def __init__(self):
        self.vars = []
        self.subTerms = []
        self.num = 1.
        self.powers = []
        self.operator = "+"
        self.ownerTerm = -1
        self.termPowers = [1]
        #TODO: self.imaginary_num
    def numTerms(self):
        return len(self.subTerms)
    def numVars(self):
        return len(self.vars)
    def numPowers(self):
        return len(self.powers)

    def allTermsHaveVar(self, var):
        hasVar = []
        for term in self.subTerms:
            hasVar.append(False)
            for i in range(term.numVars()):
                if term.vars[i] == var:
                    hasVar[-1] = True
        for i in hasVar:
            if not i:
                return False
        return True

    def setSubTermOwners(self): #recursively setup the ownership variable so we can perform recursive operations on the class.
        for i in range(len(self.subTerms)):
            self.subTerms[i].setSubTermOwners()
            self.subTerms[i].ownerTerm = self
    def hasVar(self, var):
        for arrayVar in self.vars:
            if arrayVar == var:
                return True
        return False

    def getLocationForVar(self, var):
        return getLocation(self.vars, var)

    def getPowerForVar(self, var):
        location = self.getLocationForVar(var)
        return self.powers[location]

    def getSubTermPos(self, subTerm):
        for st in range(self.numTerms()):
            if self.subTerms[st] == subTerm:
                return st
        print("Warning: Didn't get a subTerm pos. Function: getSubTermPos")
        return None

    def getPowerForTerm(self, term):
        location = self.subTerms.index(term)
        return self.termPowers[location]

    def get_location_for_term(self, term):
        location = self.subTerms.index(term)
        return location

    def get_power_for_term(self, term):
        location = self.get_location_for_term(term)
        return self.termPowers[location]

    def get_same_subterms(self, other):
        same_subterms = []
        for self_term_num in range(self.numTerms()):
            for other_term_num in range(other.numTerms()):
                if self.subTerms[self_term_num] == other.subTerms[other_term_num]:
                    if not contains(same_subterms, self.subterms[self_term_num]):
                        same_subterms.append(self.subTerms[self_term_num])
        return same_subterms

    def can_perform_ops(self, other):
        #NOTE: need to check vars, powers, subterms, termpowers and ownerterm.
        #check if we have the same vars
        if self.numVars() != other.numVars():
            return False
        num_vars = self.numVars()
        for i in range(num_vars):
            if not self.hasVar(other.vars[i]):
                return False
        #check powers
        for var in self.vars:
            if self.getPowerForVar(var) != other.getPowerForVar(var):
                return False
        for sub_term in self.subTerms:
            if not other.has_subterm(sub_term):
                return False

    def print_term(self):
        out_str = self.operator
        out_str += str(self.num)
        num_vars = self.numVars()
        for i in range(num_vars):
            out_str += self.vars[i]
            if self.powers[i] != 1:
                out_str += "^" + str(self.powers[i])
        print(out_str)

    def has_subterm(self, term):
        try:
            self.subTerms.index(term)
            print("got same subterm.")
            return True
        except:
            print("got different subterm.")
            return False

    def has_same_subterms(self, other):
        if self.numTerms() != other.numTerms():
            return False
        for term_num in range(other.numTerms()):
            if not self.has_subterm(other.subTerms[term_num]):
                return False
        return True

    #TODO: function to reduce fractions.

    def div(self, other):
        if type(other) != type(self):
            return
        #div num
        self.num /= other.num

        #divide powers
        same_vars = getSameVars(self, other)
        for var in same_vars:
            self_pwr_loc = self.getLocationForVar(var)
            self_pwr = self.getPowerForVar(var)
            other_pwr = other.getPowerForVar(var)
            min_pwr = getMinNum([self_pwr, other_pwr])
            self.powers[self_pwr_loc] -= min_pwr
            #remove vars with powers equal to zero.
            if self.powers[self_pwr_loc] == 0:
                del self.powers[self_pwr_loc]
                del self.vars[self_pwr_loc]
        del same_vars

        #divide subterms
        same_subterms = self.get_same_subterms(other)
        for same_subterm in same_subterms:
            self_pwr = self.get_power_for_term(same_subterm)
            self_pwr_loc = self.get_location_for_term(same_subterm)
            other_pwr = other.get_power_for_term(same_subterm)
            min_pwr = getMinNum([self_pwr, other_pwr])
            self.termPowers -= min_pwr
            if self.termPowers[self_pwr_loc] == 0:
                del self.termPowers[self_pwr_loc]
                del self.subTerms[self_pwr_loc]
        del same_subterms

    def __eq__(self, other):
        if type(other) != term:
            print("Type is not term.")
            return False

        selfTerms = self.numTerms()
        otherTerms = other.numTerms()
        if selfTerms != otherTerms:
            return False
            print("length of subTerms is different.")
        del otherTerms

        #recursion
        for i in range(selfTerms):
            #NOTE: Maybe we can just check the arrays against each other? Or use self.has_subterm.
            #NOTE: LEFT OFF HERE
            if not self.has_subterm(other.subTerms[i]):
#            if not self.subTerms[i] == other.subTerms[i]:
                print("does not have subterm.")
                return False
            else:
                print("has subterm.")

        #check num
        if self.num != other.num:
            print("num is different.")
            print(str(self.num) + " vs. " + str(other.num))
            return False

        #check vars (we have to do this the complex way because they could be in a weird order eg. 3xy vs 3yx)
        if self.numVars() != other.numVars():
            print("number of vars is different.")
            return False
        for i in range(self.numVars()):
            if not contains(self.vars, other.vars[i]):
                print("self does not have a var that other has.")
                return False

        #check powers
        for i in range(self.numVars()):
            var = self.vars[i]
            otherPwr = other.getPowerForVar(var)
            selfPwr = self.getPowerForVar(var)
            if otherPwr != selfPwr:
                print("powers for var is different.")
                return False

        #check termPowers (getPowerForTerm is risky.)
        for i in range(self.numTerms()):
            selfPwr = self.getPowerForTerm(self.subTerms[i])
            otherPwr = other.getPowerForTerm(other.subTerms[i])
            if selfPwr != otherPwr:
                print("Power for term is different.")
                return False

    #TODO: Recursive function to collect like terms.

    def factor(self):
        for term in range(self.numTerms()):
            self.subTerms[term].factor()
        self.commonFactor()
        self.factorTrinomial()
        self.commonFactor()

    def commonFactor(self, recursive = False):
        #recursion
        if recursive:
            for term in range(self.numTerms()):
                self.subTerms[term].commonFactor(recursive = True)
        print("trying to factor")
        self.printBrackets(recursive = True)
        print()

        #if two of the same subTerms are multiplied together, take out one and add one to the other one's power.
        numTerms = self.numTerms()
        for term in range(self.numTerms()):
            if numTerms != term + 1: #we can't get the index of term + 1 if it's outside the scope of self.subTerms.
                if self.subTerms[term] == self.subTerms[term + 1] and self.subTerms[term + 1].operator == "*":
                    print("Got two terms multiplied by each other.")
                    self.termPowers[term] += 1
                    del self.subTerms[term + 1]
                    del self.termPowers[term + 1]
        #get all the remaining terms that are the same
        sameTermsDict = {}
        for term1 in range(self.numTerms()):
            for term2 in range(self.numTerms()):
                if term1 != term2:
                    if self.subTerms[term1] == self.subTerms[term2]:
                        print("Got same subTerms.")
                        #put terms in the right spots (hopefully)
                        if not contains(sameTermsDict, term2): #if sameTermsDict[term2] has term1 in it, we don't need to add it.
                            if contains(sameTermsDict, term1):
                                if not contains(sameTermsDict[term1], term2): #if sameTermsDict[term1] exists already, we need to append to it not re-assign it
                                    sameTermsDict[term1] = [term2]
                                else:
                                    sameTermsDict[term1].append(term2)
                            else:
                                sameTermsDict[term1] = [term2]
                        else:
                            if not contains(sameTermsDict[term2], term1):
                                sameTermsDict[term2].append(term1)
        print("num sameTerms: " + str(len(sameTermsDict)))
        if len(sameTermsDict) > 0: #we don't want to mess with self if none of the subTerms are the same.

            firstTerm = term()
            secondTerm = term()

            for term1 in sameTermsDict:
                firstTerm.subTerms.append(self.subTerms[term1])
                for term2 in range(len(sameTermsDict[term1])):
                    if self.subTerms[term1] == self.subTerms[term2]:
                        secondTerm.subTerms.append(self.subTerms[term2])
            del self.subTerms[:]
            self.subTerms.append(firstTerm, secondTerm)

        #do variables and numbers
        powers = {}
        vars = {}
        varLocs = {}
        #find the variables and their respective locations.
        for term1 in range(self.numTerms()):
            for term2 in range(self.numTerms()):
                if term1 != term2:
                    for vars2 in range(self.subTerms[term2].numVars()):
                        if self.subTerms[term1].hasVar(self.subTerms[term2].vars[vars2]):
                            var = self.subTerms[term2].vars[vars2]
                            power = self.subTerms[term2].powers[vars2]
                            if var in vars:
                                vars[var] += 1
                            else:
                                vars[var] = 1
                            if not contains(varLocs, var):
                                varLocs[var] = []
                            if not contains(varLocs[var], [term2, vars2]):
                                varLocs[var].append([term2, vars2])
                                #subterm no., var pos
                            if var in powers:
                                powers[var] = getMinNum([powers[var], power])
                            else:
                                powers[var] = power
        #filter out the variables that not every subterm in the term has
        varsToDel = []
        for var in vars:
            if not self.allTermsHaveVar(var):
                varsToDel.append(var)
        for var in varsToDel:
            del varLocs[var]

        #subtract the powers and delete the power and it's respective variable if the power is zero.
        for var in varLocs:
            varLocArr = varLocs[var]
            self.vars.append(var)
            self.powers.append(powers[var])
            for varLoc in varLocArr:
                minPower = powers[var]
                #subtract the minimum power from the term's power.
                self.subTerms[varLoc[0]].powers[varLoc[1]] -= minPower
                #if the term's power equals zero, delete the power and the variable.
                if self.subTerms[varLoc[0]].powers[varLoc[1]] == 0:
                    del self.subTerms[varLoc[0]].powers[varLoc[1]]
                    del self.subTerms[varLoc[0]].vars[varLoc[1]]
        #finally, factor the numbers.
        lcm = getLcm(self)
        for term in range(self.numTerms()):
            self.subTerms[term].num /= lcm
        self.num *= lcm

    def factorTrinomial(self, recursive = False):
        #recursion
        if recursive:
            for termNum in range(self.numTerms()):
                self.subTerms[termNum].factorTrinomial()

        #we can't factor it as a trinomial if we don't have 2 or 3 numTerms.
        if self.numTerms() != 3 and self.numTerms() != 2:
            return None
        if self.numTerms() == 3:
            a = self.subTerms[0]
            b = self.subTerms[1]
            c = self.subTerms[2]
        elif self.numTerms() == 2:
            a = self.subTerms[0]
            b = term()
            b.num = 1.
            c = self.subTerms[1]

        #get the two numbers that add to b and multiply to a * c.
        multiplied = a.num * c.num
        negative = False #we can't find the square root of a negative number.
        if multiplied < 0:
            negative = True
            multiplied = flip(multiplied)

        sqrt = math.floor(math.sqrt(multiplied))
        if negative:
            multiplied = flip(multiplied)
        first_b_replacement = copy.deepcopy(b)
        second_b_replacement = copy.deepcopy(b)
        for i in range(1, sqrt + 1):
            cache = multiplied / i
            if cache + i == b.num:
                first_b_replacement.num = i
                second_b_replacement.num = cache
                break
            elif flip(cache) + i == b.num:
                first_b_replacement.num = i
                second_b_replacement.num = flip(cache)
                break
            elif cache + flip(i) == b.num:
                first_b_replacement.num = flip(i)
                second_b_replacement.num = cache
                break
            elif flip(cache) + flip(i) == b.num:
                first_b_replacement.num = flip(i)
                second_b_replacement.num = flip(cache)
                break
        #equation currently looks like: "a + first_b_replacement + second_b_replacement + c"
        first_bracket_mult = term()
        first_bracket_mult.num = get_lcm_from_nums([a.num, first_b_replacement.num])
        first_bracket_mult.vars = getSameVars(a, first_b_replacement)
        second_bracket_mult = term()
        second_bracket_mult.num = get_lcm_from_nums([second_b_replacement.num, c.num])
        second_bracket_mult.vars = getSameVars(second_b_replacement, c)

        #remove the extra vars & their respective powers from the terms in the brackets.
        for var in first_bracket_mult.vars:
            #subtract the lowest of the powers from the powers.
            a_power_location = a.getLocationForVar(var)
            a_power = a.getPowerForVar(var)
            first_b_replacement_power_location = first_b_replacement.getLocationForVar(var)
            first_b_replacement_power = first_b_replacement.getPowerForVar(var)
            lowest_power = getMinNum([a_power, first_b_replacement_power])
            first_bracket_mult.powers.append(lowest_power)

            del a_power
            del first_b_replacement_power
            del a_power_location
            del first_b_replacement_power_location

        for var in second_bracket_mult.vars:
            #subtract the lowest of the powers from the powers
            second_b_replacementPowerLocation = second_b_replacement.getLocationForVar(var)
            second_b_replacementPower = second_b_replacement.getPowerForVar(var)
            cPowerLocation = c.getLocationForVar(var)
            cPower = c.getPowerForVar(var)
            minPower = getMinPower([second_b_replacementPower, cPower])
            second_bracket_mult.powers.append(minPower)

            del cPower
            del second_b_replacementPower
            del cPowerLocation
            del second_b_replacementPowerLocation
        print("first bracket mult vars: " + str(first_bracket_mult.vars))
        print("second bracket mult vars: " + str(second_bracket_mult.vars))
        #divide nums by bracket multipliers.
        a.div(first_bracket_mult)
        first_b_replacement.div(first_bracket_mult)
        second_b_replacement.div(second_bracket_mult)
        c.div(second_bracket_mult)

        #TODO: Add termPowers to new subTerms.
        self.subTerms = [first_bracket_mult, second_bracket_mult]
        self.subTerms[0].subTerms = [a, first_b_replacement]
        self.subTerms[0].termPowers = [1, 1]
        self.subTerms[1].subTerms = [second_b_replacement, c]
        self.subTerms[1].termPowers = [1, 1]
        self.termPowers = [1, 1]

    def printTree(self, depthNum = 0): #print out the tree of terms. Useful for debug purposes.
        tabString = ""
        for i in range(depthNum):
            tabString += "    "
        #print own values
        outString = tabString + self.operator + str(self.num)
        for varNum in range(self.numVars()):
            outString += str(self.vars[varNum]) + "^" + str(self.powers[varNum])
        print(outString)
#        print("termPowers: " + str(self.termPowers) + ", num of termPowers: " + str(len(self.termPowers)))
        #call kids' recursive functions.
        for term in range(self.numTerms()):
            self.subTerms[term].printTree(depthNum + 1)
#            print("Trying to access term power: " + str(term) + " out of " + str(len(self.termPowers)))
#            print(tabString + "^" + str(self.termPowers[term]))

    def printBrackets(self, recursive = False):
        bracketString = self.operator + str(self.num)
        for i in range(self.numVars()):
            var = self.vars[i]
            power = self.powers[i]
            bracketString += var
            if power != 1:
                bracketString += "^" + str(power)
        if self.numTerms() > 0: #we don't need brackets around every single term (eg. ((3x) + (3))) -- it would be annoyng.
            bracketString += "("
        print(bracketString, end="")
        #recursion
        if recursive:
            for i in range(self.numTerms()):
                self.subTerms[i].printBrackets(recursive = True)
        if self.numTerms() > 0: #we don't need brackets around every single term (eg. ((3x) + (3))) -- it would be annoyng.
            if type(self.ownerTerm) != type(-1): #we only want a newline after we've printed out all the terms.
                print(")", end="")
            elif type(self.ownerTerm) == type(-1): #we only want a newline after we've printed out all the terms.
                print(")", end="")

def containsIndex(array, idx):
    return (len(array) > idx)

def flip(num):
    return num / -1

def contains(array, search):
    for element in array:
        if element == search:
            return True
    return False

def getNumAtPos(equation, pos): #gets the number after a position. Useful for finding the number after an operation (eg. ^, +, /)
    startPos = pos
    equationLen = len(equation)

    strNum = ""
    elementType = getType(equation[pos])
    while (elementType == "num" or elementType == ".") and pos < equationLen:
        strNum += equation[pos]
        pos += 1
        if pos < equationLen:
            elementType = getType(equation[pos])

    return float(strNum), pos - startPos

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

def getLocation(array, search):
    for i in range(len(array)):
        if array[i] == search:
            return i
    return None

def getLcm(term): #get the lowest common multiple
    numTerms = term.numTerms()
    if numTerms > 0:
        for multiple in range(maxLcm,0,-1):
            works = True
            for termNum in range(numTerms):
                if not isInt(term.subTerms[termNum].num / multiple):
                    works = False
            if works:
                return multiple
    else:
        return 1

def get_lcm_from_nums(nums):
    for multiple in range(maxLcm, 0, -1):
        works = True
        for num in nums:
            if not isInt(num / multiple):
                works = False
            if works:
                return multiple

def getMinNum(array):
    minNum = array[0]
    for element in array:
        if element < minNum:
            minNum = element
    return minNum

def getSameVars(term1,term2):#returns vars & the smallest powers.
    term1VarLen = len(term1.vars)
    term2VarLen = len(term2.vars)
    same_vars = []
    for t1 in range(term1VarLen):
        for t2 in range(term2VarLen):
            if term1.vars[t1] == term2.vars[t2]:
                same_vars.append(term1.vars[t1])
                #sameVars -- [var, power, location in term 1, location in term 2]
    return same_vars

def isTermPower(location):
    if getType(rawEquation[location-1]) == ")":
        return True

terms = term()
terms.operator = "+"
currentBracket = 0
currentNum = 0
rawEquation = argv[1]

#generate term tree
equationLen = len(rawEquation)
equationNum = 0
termObjNum = 0

while equationNum < equationLen:
    equationElement = rawEquation[equationNum]
    equationType = getType(equationElement)
#    print("Checking element "+str(equationNum) + " which is of type " + equationType)
    if equationType == "(": #go down a level of recursion
        terms.subTerms.append(term())
        terms.subTerms[-1].ownerTerm = terms
        terms = terms.subTerms[-1]
    elif equationType == ")": #come back up a level of recursion
        terms = terms.ownerTerm
        terms.termPowers.append(1)
    elif equationType == "num":
        if(terms.num == 1):
            terms.num, numLength = getNumAtPos(rawEquation, equationNum)
            equationNum += numLength - 1
    elif equationType == "var":
        terms.vars.append(equationElement)
        terms.powers.append(1)
    elif equationType == "^":
        if not isTermPower(equationNum): #tell the difference between a power acting on an entire term or just a power acting on a variable.
            terms.powers[-1], numLength = getNumAtPos(rawEquation, equationNum + 1)
        else:
            terms.termPowers[-1], numLength = getNumAtPos(rawEquation, equationNum + 1)
        equationNum += numLength
    elif equationType == "operator":
        #Go to the next term.
        terms = terms.ownerTerm
        terms.subTerms.append(term())
        terms.subTerms[-1].ownerTerm = terms
        terms = terms.subTerms[-1]
        terms.operator = equationElement
    equationNum += 1

#run operations on term tree
"""
terms.setSubTermOwners()
print("Old terms tree: ")
terms.printTree()
terms.commonFactor(recursive = True)
terms.factorTrinomial(recursive = True)
terms.commonFactor(recursive = True)
print("New terms tree: ")
terms.printTree()
terms.printBrackets(recursive = True)
print()
"""
#NOTE: test
"""
terms.setSubTermOwners()
if terms.subTerms[0] == terms.subTerms[1]:
    print("equal.")
else:
    print("not equal.")
"""
terms.setSubTermOwners()
if terms.subTerms[0].has_subterm(terms.subTerms[1].subTerms[0]):
    print("true")
else:
    print("false")

term = terms.subTerms[1]
print("index: " + str(terms.subTerms.index(term)))
