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
        self.power = 1
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
        return get_idx(self.vars, var)

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
            self_term_loc = self.get_location_for_term(same_subterm)
            other_term_loc = other.get_location_for_term(same_subterm)
            self_pwr = self.subTerms[self_term_loc].power
            other_pwr = other.subTerms[other_term_loc].power
            min_pwr = getMinNum([self_pwr, other_pwr])
            self.subTerms[self_term_loc].power -= min_pwr
            if self.subTerms[self_term_loc] == 0:
                del self.subTerms[self_term_loc]
        del same_subterms

    def __eq__(self, other):
        if type(other) != term:
            print("Type is not term.")
            return False
        self_bracket_str = self.get_bracket_string()
        other_bracket_str = other.get_bracket_string()
        if self.get_bracket_string() == other.get_bracket_string():
            return True
        else:
            return False

    def has_same_subterms(self, other):
        try: #we need the try except statements in case there is no (.
            self_bracket_str = self.get_bracket_string()
            other_bracket_str = other.get_bracket_string()
            first_bracket_pos = self_bracket_str.index("(")
            self_bracket_str = self_bracket_str[first_bracket_pos:]
            first_bracket_pos = other_bracket_str.index("(")
            other_bracket_str = other_bracket_str[first_bracket_pos:]
        except:
            return False
        if self_bracket_str == other_bracket_str:
            return True
        else:
            return False

    def update_operator(self, recursive = False): #if num < 0 and operator is +, set operator to - and flip self.num
        if recursive:
            for i in range(self.numTerms()):
                self.subTerms[i].update_operator(recursive = True)
        if self.num < 0 and self.operator == "+":
            self.num = flip(self.num)
            self.operator = "-"

    #TODO: Recursive function to collect like terms.

    def factor(self):
        self.commonFactor(recursive = True)
        self.factorTrinomial(recursive = True)
        self.update_operator(recursive = True)
        self.commonFactor(recursive = True)

    #NOTE: Two identical terms multiplied by each other will not yet reduce properly.
    def commonFactor(self, recursive = False):
        #recursion
        if recursive:
            for i in range(self.numTerms()):
                self.subTerms[i].commonFactor(recursive = True)

        #if two of the same subTerms are multiplied together, take out one and add one to the other one's power.
        numTerms = self.numTerms()
        for i in range(self.numTerms()):
            if i + 1 != numTerms: #we can't get the index of term + 1 if it's outside the scope of self.subTerms.
                if self.subTerms[i] == self.subTerms[i + 1] and self.subTerms[i + 1].operator == "*":
                    print("Got two terms multiplied by each other.")
                    self.subTerms[i].power += 1
                    del self.subTerms[i + 1]

        same_term_pos = []
        #find a term whose subterms are equal to another term's and that's not the same term
        for i in range(self.numTerms()):
            for n in range(self.numTerms()):
                if i != n:
                    term_i = self.subTerms[i]
                    term_n = self.subTerms[n]
                    if term_i.has_same_subterms(term_n):
        #find if there's already an array in same_term_pos that contains a location of said term.
                        has_found = False
                        for term_pos_i in range(len(same_term_pos)):
                            term_pos = same_term_pos[term_pos_i]
                            pos = term_pos[0]
                            search_term = self.subTerms[pos]
                            if search_term == term_i:
        #if there is, append it to the respective position of same_term_pos
                                same_term_pos[term_pos_i].append(i)
                                same_term_pos[term_pos_i].append(n)
                                has_found = True

        #else, append a new array
                        if not has_found:
                            same_term_pos.append([i, n])

        #remove duplicates from array.
        for i in range(len(same_term_pos)):
            for n in range(len(same_term_pos)):
                same_term_pos[i] = remove_duplicates(same_term_pos[i])
                same_term_pos[i].sort()
        same_term_pos = remove_duplicates(same_term_pos)
        #setup to_del on all subterms so we can keep track of which ones we need to delete later.
        for i in range(self.numTerms()):
            self.subTerms[i].to_del = False
        #loop same_term_pos
        n_same_terms = len(same_term_pos)
        if n_same_terms > 0:
            print("got " + str(n_same_terms) + " same terms.")
            for same_terms in same_term_pos:
                pos = same_terms[0]
                print("same subterm: " + self.subTerms[pos].get_subterm_string())
        del n_same_terms
        for i in range(len(same_term_pos)):
            #get the term in common. Save it for later.
            term_pos = same_term_pos[i][0]
            term_in_common = copy.deepcopy(self.subTerms[term_pos])
            term_in_common.num = 1.
            term_in_common.operator = "*"
            term_in_common.vars = []
            term_in_common.to_del = False

            #get all the terms multiplied to the central term. Add them all to their own term.
            multiplied_term = term()
            multiplied_term.to_del = False
            for n in range(len(same_term_pos[i])):
                same_term = self.subTerms[same_term_pos[i][n]]
                multiplied_term.subTerms.append(same_term)
                self.subTerms[same_term_pos[i][n]].to_del = True
            #NOTE: Left off trying to finish the following pseudocode.
            #remove the subTerms from multiplied_term's subterms since they've been factored out.
            for n in range(multiplied_term.numTerms()):
                multiplied_term.subTerms[n].subTerms = []
            self.subTerms.append(multiplied_term)
            self.subTerms.append(term_in_common)
        #delete subTerms marked for deletion.
        i = 0
        while i < self.numTerms():
            if self.subTerms[i].to_del:
                del self.subTerms[i]
            else:
                del self.subTerms[i].to_del
                i += 1

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
        for i in range(self.numTerms()):
            self.subTerms[i].num /= lcm
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
        #divide nums by bracket multipliers.
        a.div(first_bracket_mult)
        first_b_replacement.div(first_bracket_mult)
        second_b_replacement.div(second_bracket_mult)
        c.div(second_bracket_mult)

        self.subTerms = [first_bracket_mult, second_bracket_mult]
        self.subTerms[0].subTerms = [a, first_b_replacement]
        self.subTerms[1].subTerms = [second_b_replacement, c]
        print("Done factoring trinomial.")

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

    def get_bracket_string(self):
        if self.num == 1 and (self.vars != [] or self.subTerms != []):
            bracketString = self.operator
        else:
            bracketString = self.operator + str(self.num)
        for i in range(self.numVars()):
            var = self.vars[i]
            power = self.powers[i]
            bracketString += var
            if power != 1:
                bracketString += "^" + str(power)
        if self.numTerms() > 0: #we don't need brackets around every single term (eg. ((3x) + (3))) -- it would be annoyng.
            bracketString += "("
        #recursion
        for i in range(self.numTerms()):
            bracketString += self.subTerms[i].get_bracket_string()
        if self.numTerms() > 0: #we don't need brackets around every single term (eg. ((3x) + (3))) -- it would be annoyng.
            bracketString += ")"
        return bracketString

    def get_subterm_string(self):
        bracket_string = self.get_bracket_string()
        bracket_pos = bracket_string.index("(")
        bracket_string = bracket_string[bracket_pos:]
        return bracket_string

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

def get_idx(array, search):
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

def remove_duplicates(array):
    newArray = []
    for element in array:
        if not contains(newArray, element):
            newArray.append(element)
    return newArray

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
            terms.subTerms[-1].power, numLength = getNumAtPos(rawEquation, equationNum + 1)
        equationNum += numLength
    elif equationType == "operator":
        #Go to the next term.
        terms = terms.ownerTerm
        terms.subTerms.append(term())
        terms.subTerms[-1].ownerTerm = terms
        terms = terms.subTerms[-1]
        terms.operator = equationElement
    equationNum += 1

#TODO: Get operations to perform from argv

terms.setSubTermOwners()
"""
terms.commonFactor(recursive = True)
terms.factorTrinomial(recursive = True)
terms.update_operator(recursive = True)
terms.commonFactor(recursive = True)
"""
terms.factor()
print(terms.get_bracket_string())

#NOTE: Legacy test code
"""
#run operations on term tree
terms.setSubTermOwners()
print("Old terms tree: ")
terms.printTree()
terms.commonFactor(recursive = True)
terms.factorTrinomial(recursive = True)
print("after factoring trinomial:")
print(terms.get_bracket_string())
terms.update_operator(recursive = True)
print("after updating operators:")
print(terms.get_bracket_string())
terms.commonFactor(recursive = True)
print("New terms tree: ")
terms.printTree()
print(terms.get_bracket_string())
"""
