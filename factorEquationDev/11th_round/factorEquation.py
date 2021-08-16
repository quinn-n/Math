#!/usr/bin/env python
"""
Written and maintained by happylego91. https://gitlab.com/happylego91

"""
from sys import argv
import math
import copy
import term

maxLcm = 1000

chars = "abcdefghijklmnopqrstuvwxyz"
nums = range(10)
operators = "+-*/"

if len(argv) < 2:
    print("Usage: "+argv[0]+" <equation>")
    print("Factors an equation. Hopefully. That's the plan anyways.")
    print("Example: '(3x+3)' should return 3(x+1)")
    exit()

def get_type(char):
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

def flip(num):
    """multiply a number by -1 and return the result"""
    return num * -1

def contains(array, search):
    """returns true if search is in array."""
    for element in array:
        if element == search:
            return True
    return False

def get_num_at_pos(equation, pos): #gets the number after a position. Useful for finding the number after an operation (eg. ^, +, /)
    """returns the number after position pos."""
    start_pos = pos
    equation_len = len(equation)

    str_num = ""
    element_type = get_type(equation[pos])
    while (element_type == "num" or element_type == ".") and pos < equation_len:
        str_num += equation[pos]
        pos += 1
        if pos < equation_len:
            element_type = get_type(equation[pos])

    return float(str_num), pos - start_pos

def is_int(num):
    """returns true if num is a whole number."""
    if num % 1 == 0:
        return True
    else:
        return False

def is_in(string, char):
    """returns true if char is in string."""
    strLen = len(string)
    for i in range(strLen):
        if string[i] == char:
            return True
    return False

def get_idx(array, search):
    """returns the index of search in array."""
    for i in range(len(array)):
        if array[i] == search:
            return i
    return None

def get_lcm(term): #get the lowest common multiple
    """returns the lowest common multiple in term's subterms."""
    #TODO: add support for variables & powers
    num_terms = term.num_terms()
    if num_terms > 0:
        for multiple in range(maxLcm,0,-1):
            works = True
            for term_num in range(num_terms):
                if not is_int(term.sub_terms[term_num].num / multiple):
                    works = False
            if works:
                return multiple
    return 1

def get_lcm_from_nums(nums):
    """returns the lowest common multiple from an array of numbers."""
    for multiple in range(maxLcm, 0, -1):
        works = True
        for num in nums:
            if not is_int(num / multiple):
                works = False
        if works:
            return multiple
    return 1

def get_min_num(array):
    """returns the smallest number from an array of numbers."""
    min_num = array[0]
    for element in array:
        if element < min_num:
            min_num = element
    return min_num

def get_same_vars(term1,term2):#returns vars
    """returns the same vars between term1 and term2."""
    term_1_var_len = len(term1.vars)
    term_2_var_len = len(term2.vars)
    same_vars = []
    for t1 in range(term_1_var_len):
        for t2 in range(term_2_var_len):
            if term1.vars[t1] == term2.vars[t2]:
                same_vars.append(term1.vars[t1])
                #sameVars -- [var, power, location in term 1, location in term 2]
    return same_vars

def is_term_power(location):
    """returns true if the power at location belongs to a term."""
    if get_type(raw_equation[location-1]) == ")":
        return True

def remove_duplicates(array):
    """returns a new array that is like array but without any duplicate elements."""
    new_array = []
    for element in array:
        if not contains(new_array, element):
            new_array.append(element)
    return new_array

terms = term.term()
terms.operator = "+"
current_bracket = 0
current_num = 0
raw_equation = argv[1]

#generate term tree
equation_len = len(raw_equation)
equation_num = 0
term_num = 0

while equation_num < equation_len:
    equation_element = raw_equation[equation_num]
    equation_type = get_type(equation_element)
#    print("Checking element "+str(equation_num) + " which is of type " + equation_type)
    if equation_type == "(": #go down a level of recursion
        terms.sub_terms.append(term.term())
        terms.sub_terms[-1].owner_term = terms
        terms = terms.sub_terms[-1]
        termnum = 0
    elif equation_type == ")": #come back up a level of recursion
        terms = terms.owner_term
    elif equation_type == "num":
        terms.owner_term.has_run_startup = True
        if(terms.num == 1):
            terms.num, num_length = get_num_at_pos(raw_equation, equation_num)
            equation_num += num_length - 1
    elif equation_type == "var":
        terms.vars.append(equation_element)
        terms.powers.append(1)
        terms.owner_term.has_run_startup = True
    elif equation_type == "^":
        if not is_term_power(equation_num): #tell the difference between a power acting on an entire term or just a power acting on a variable.
            terms.powers[-1], num_length = get_num_at_pos(raw_equation, equation_num + 1)
        else:
            terms.sub_terms[-1].power, num_length = get_num_at_pos(raw_equation, equation_num + 1)
        equation_num += num_length
    elif equation_type == "operator":
        #Go to the next term.
        if terms.owner_term.has_run_startup:
            print("running startup on " + equation_element)
            #term_pos = terms.owner_term.get_location_for_term.term(terms)
            terms = terms.owner_term
            terms.sub_terms.append(term.term())
            terms.sub_terms[-1].owner_term = terms
            terms = terms.sub_terms[-1]
        else:
            terms.owner_term.has_run_startup = True
        terms.operator = equation_element
    equation_num += 1

#TODO: Get operations to perform from argv

print("Got terms: " + terms.get_bracket_string())

terms.set_sub_term_owners()
#terms.debug_factor()
#terms.factor()
terms.dev_factor()
print(terms.get_bracket_string())
print("after div with subterms:")
#terms.div_with_subterms(2)
terms.update_operator(recursive = True)
print("final result:")
print(terms.get_bracket_string())
