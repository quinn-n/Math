#!/usr/bin/env python
# evalRange.py
# Evaluates a function for a range of values with it's variables
# eg. f(x) = 3x with x from 0 to 10
# Written by happylego91
# 1.0 - May 22nd 2019

import progutil
from sys import argv
from time import sleep
import copy
from string import ascii_letters
from string import whitespace
import math

HELP_MSG = "Usage: evalRange <function str>"
NUMS = "0123456789"

class Variable:
    """A simple class to store information about a variable"""
    def __init__(self, char: str, start=0, end=0, increment=1):
        self.char = char
        self.start = start
        self.end = end
        self.increment = 1
        self.cur_val = start
    def ask_vals(self):
        """Asks the user to provide a start and end value for the variable"""
        #For start and end, query the user for it's value.
        #If the user does not provide a value, continue with
        #the default.
        startstr = input(self.char + " start (leave blank for default) = ")
        try:
            self.start = float(startstr)
            self.cur_val = self.start
        except:
            ""
        endstr = input(self.char + " end = ")
        try:
            self.end = float(endstr)
        except:
            ""
        incrementstr = input(self.char + " increment (leave blank for default) = ")
        try:
            self.increment = float(incrementstr)
        except:
            return
    def tick(self):
        """Ticks over the variable to the next value"""
        self.cur_val += self.increment
    def reset(self):
        """Resets the variable to it's start value"""
        self.cur_val = self.start
    def print(self, end="\n"):
        """Prints out a variable"""
        print(self.char + " = " + str(self.cur_val), end=end)

class Result:
    """Stores information based on a result"""
    def __init__(self, result, equ: str):
        self.result = result
        self.equ = equ
    def print(self):
        """Prints out the result"""
        print(self.equ + " = " + str(self.result))

class EvalFunc:
    """Stores information based on an evaluation function"""
    def __init__(self, char, func, left=False, right=False):
        self.char = char
        self.func = func
        self.left = left
        self.right = right

def list_to_string(arr: list):
    """Adds all the elements in arr to a string"""
    outstr = ""
    for e in arr:
        outstr += str(e)
    return outstr

def get_num_start(equation, pos):
    """Returns the start position of a number in equation"""
    while pos >= 0 and equation[pos] in NUMS or equation[pos] == ".":
        pos -= 1
    return pos + 1

def get_num_end(equation, pos):
    """Returns the end position of a number in equation"""
    equation_len = len(equation)
    while equation[pos] in NUMS or equation[pos] == ".":
        pos += 1
        if pos >= equation_len:
            break
    return pos - 1

def get_num_at_pos(equation, pos): #gets the number after a position. Useful for finding the number after an operation (eg. ^, +, /)
    """returns the number after position pos"""
    #Get the start and end char positions of the number.
    start_pos = get_num_start(equation, pos)
    end_pos = get_num_end(equation, pos)
    num_str = equation[start_pos:end_pos + 1]
    return float(num_str)

def replace_ints_with_floats(string: str):
    """Replaces all the integers in a string with floats
    Literally just adds a .0 onto numbers that aren't floats"""
    #Iterate over every char in string
    #If the char's in a number, get that number as a string
    #If that number's string doesn't have a decimal, add a .0 to the end of it
    i = 0
    while i < len(string):
        char = string[i]
        if char in NUMS:
            start = get_num_start(string, i)
            end = get_num_end(string, i)
            numstr = string[start:end + 1]
            if not "." in numstr:
                string = string.replace(numstr, numstr + ".0")
            #Continue from the end of the number
            i = get_num_end(string, i)
        i += 1
    return string

def permutation(n, r):
    """Evaluates a permutation"""
    return n ** r

def combination(n, r):
    """Evaluates a combination"""
    return math.factorial(n) / (math.factorial(r) * math.factorial(n - r))

def str_sub(string: str, val, pos: int, eval_func: EvalFunc):
    """Replaces a function in str with it's value
    Written to be used in better_eval"""
    replace_str = ""
    if eval_func.left and eval_func.right:
        leftstr = get_bracket_str(string, pos - 1)
        rightstr = get_bracket_str(string, pos + 1)
        replace_str = leftstr + eval_func.char + rightstr
        counter_reset = len(leftstr)
    elif eval_func.left:
        leftstr = get_bracket_str(string, pos - 1)
        replace_str = leftstr + eval_func.char
        counter_reset = len(leftstr)
    else:
        rightstr = get_bracket_str(string, pos + 1)
        replace_str = eval_func.char + rightstr
        counter_reset = 0
    #How far back the counter needs to be set
    return string.replace(replace_str, str(val)), counter_reset

def remove_whitespace(string: str):
    """Removes all the whitespace characters from a string"""
    outstr = ""
    for c in string:
        if not c in whitespace:
            outstr += c
    return outstr

def remove_chars(string: str, chars: str):
    """Removes all characters in chars"""
    outstr = ""
    for c in string:
        if not c in chars:
            outstr += c
    return outstr

eval_funcs = {"C": EvalFunc("C", combination, left=True, right=True),
    "P": EvalFunc("P", permutation, left=True, right=True),
    "!": EvalFunc("!", math.factorial, left=True, right=False)}

VARS = remove_chars(ascii_letters, list_to_string(list(eval_funcs.keys())))

def get_closing_bracket(eqn: str, open_pos: int):
    """Returns the position of the closing bracket in an equation"""
    bracket_lvl = 1
    eqnlen = len(eqn)
    i = 1
    while i + open_pos < eqnlen and bracket_lvl > 0:
        char = eqn[i + open_pos]
        if char == "(":
            bracket_lvl += 1
        elif char == ")":
            bracket_lvl -= 1
        i += 1
    return open_pos + i - 1

def get_opening_bracket(eqn: str, end_pos: int):
    """Returns the position of the opening bracket in an equation"""
    bracket_lvl = 1
    i = end_pos
    while i >= 0 and bracket_lvl > 0:
        char = eqn[i]
        if char == ")":
            bracket_lvl += 1
        elif char == "(":
            bracket_lvl -= 1
        i -= 1
    return i + 1

def get_bracket_str(eqn: str, bracket_pos: int):
    """Returns a string with the contents of a bracket in an equation
    bracket_pos must be the position of either the opening or closing bracket in the equation
    Retuns the number as a string if no bracket is found"""
    if eqn[bracket_pos] == "(":
        open_pos = bracket_pos
        end_pos = get_closing_bracket(eqn, open_pos)
    elif eqn[bracket_pos] == ")":
        open_pos = get_opening_bracket(eqn, bracket_pos)
        end_pos = bracket_pos
    else:
        return str(get_num_at_pos(eqn, bracket_pos))
    bracket_eqn = eqn[open_pos:end_pos + 1]
    return bracket_eqn

def eval_bracket(eqn: str, bracket_pos: int):
    """Evaluates a bracket in a string.
    Returns the number at open_pos if no bracket is found"""
    bracket_eqn = get_bracket_str(eqn, bracket_pos)
    #Cut off the outer brackets to prevent a recursion loop
    if bracket_eqn[0] == "(":
        bracket_eqn = bracket_eqn[1:-1]

    return better_eval(bracket_eqn)

def better_eval(string: str):
    """Like eval(), but evaluates combinations, permutations, factorials, etc."""
    eval_chars = list(eval_funcs.keys())
    i = 0
    #Iterate over every char in the string
    #When we encounter a function, check if it needs left and right variables
    #Find the respective variables, and call the function with them
    #Then insert the returned value back into the string and reset the counter because the string's length has changed
    while i < len(string):
        char = string[i]
        if char in eval_chars:
            eval_func = eval_funcs[char]
            if eval_func.left and eval_func.right:
                left = eval_bracket(string, i - 1)
                right = eval_bracket(string, i + 1)
                result = eval_func.func(left, right)
                string, counter_reset = str_sub(string, result, i, eval_func)
                i -= counter_reset
            elif eval_func.left:
                left = eval_bracket(string, i - 1)
                result = eval_func.func(left)
                string, counter_reset = str_sub(string, result, i, eval_func)
                i -= counter_reset
            elif eval_func.right:
                right = eval_bracket(string, i + 1)
                result = eval_func.func(right)
                string, counter_reset = str_sub(string, result, i, eval_func)
                i -= counter_reset
        i += 1
    result = eval(string)
    return result

def print_results(results: list):
    """Prints out all results in a list"""
    for res in results:
        res.print()

def swap_str(string, pos1, pos2):
    """Swaps two chars in a string"""
    cache = string[pos1]
    string[pos1] = string[pos2]
    string[pos2] = cache

def has_var(variables: list, c: str):
    """Returns true if vars has a variable c"""
    for var in variables:
        if var.char == c:
            return True
    return False

def find_vars(string: str):
    """Returns all the variables in an equation"""
    equ_vars = []
    for c in string:
        if c in VARS and not has_var(equ_vars, c):
            equ_vars.append(Variable(c))
    return equ_vars

def get_vars(equ_vars):
    """Gets a value for each variable from the user"""
    for v in equ_vars:
        v.ask_vals()

def find_var(variables, search):
    """Returns the index of the variable with the char search"""
    for i in range(len(variables)):
        if variables[i].char == search:
            return i

def substitute_vars(string: str, equ_vars: list):
    """Substitutes variables into a function string"""
    outstr = string
    for var in equ_vars:
        outstr = outstr.replace(var.char, str(float(var.cur_val)))
    return outstr

def tick_vars(equ_vars: list):
    """Ticks over all the variables in an array
    Returns false if the variables have all been ticked over"""
    cur_tick = len(equ_vars) - 1
    while cur_tick >= 0:
        equ_vars[cur_tick].tick()
        if equ_vars[cur_tick].cur_val > equ_vars[cur_tick].end:
            equ_vars[cur_tick].reset()
            cur_tick -= 1
        else:
            return True
    return False

def varstodict(equ_vars: list):
    """Converts a list of variables to a dict"""
    out_vars = {}
    for var in equ_vars:
        out_vars[var.char] = var.cur_val
    return out_vars

def run_equ(func, equ_vars: list):
    """Runs an equation with the given variable ranges
    Returns a list of the results"""
    results = []
    continuing = True
    while continuing:
        #Run variables
        result_str = substitute_vars(func, equ_vars)
        result = better_eval(remove_whitespace(result_str))
        results.append(Result(result, result_str))
        #Tick variables
        continuing = tick_vars(equ_vars)
    return results

#Verify inputs
if not progutil.check_inputs(argv, 2, HELP_MSG):
    exit(1)

func = replace_ints_with_floats(argv[1])
variables = find_vars(func)
get_vars(variables)
results = run_equ(func, variables)
print("Got results:")
print_results(results)