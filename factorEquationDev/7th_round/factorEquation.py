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

class term:
    def __init__(self):
        self.vars = []
        self.sub_terms = []
        self.num = 1.
        self.powers = []
        self.operator = "+"
        self.owner_term = -1
        self.power = 1
        #TODO: self.imaginary_num
    def num_terms(self):
        return len(self.sub_terms)
    def num_vars(self):
        return len(self.vars)
    def num_powers(self):
        return len(self.powers)

    def __add__(self, other):
        if type(other) != term:
            if type(other) == int or type(other) == float:
                new_other = term()
                new_other.num = other
                other = copy.deepcopy(new_other)
                del new_other
            else:
                return
        self_terms_string = self.get_subterms_string()
        other_terms_string = other.get_subterm_string()
        self_vars = self.vars
        other_vars = other.vars
        self_powers = self.powers
        other_powers = other.powers
        if self_terms_string == other_terms_string and self_vars == other_vars and self_powers == other_powers:
            self.num += other.num
    def __sub__(self, other):
        if type(other) != term:
            if type(other) == int or type(other) == float:
                new_other = term()
                new_other.num = other
                other = copy.deepcopy(new_other)
                del new_other
            else:
                return
        self_terms_string = self.get_subterms_string()
        other_terms_string = other.get_subterm_string()
        self_vars = self.vars
        other_vars = other.vars
        self_powers = self.powers
        other_powers = other.powers
        if self_terms_string == other_terms_string and self_vars == other_vars and self_powers == other_powers:
            self.num -= other.num
    def __mul__(self, other):
        if type(other) != term:
            if type(other) == int or type(other) == float:
                new_other = term()
                new_other.num = other
                other = copy.deepcopy(new_other)
                del new_other
            else:
                return
        #NOTE: left off here

    def all_terms_have_var(self, var):
        has_var = []
        for term in self.sub_terms:
            has_var.append(False)
            for i in range(term.num_vars()):
                if term.vars[i] == var:
                    has_var[-1] = True
        for i in has_var:
            if not i:
                return False
        return True

    def set_sub_term_owners(self): #recursively setup the ownership variable so we can perform recursive operations on the class.
        for i in range(len(self.sub_terms)):
            self.sub_terms[i].set_sub_term_owners()
            self.sub_terms[i].owner_term = self
    def has_var(self, var):
        for array_var in self.vars:
            if array_var == var:
                return True
        return False

    def get_location_for_var(self, var):
        return get_idx(self.vars, var)

    def get_power_for_var(self, var):
        location = self.get_location_for_var(var)
        return self.powers[location]

    def get_sub_term_pos(self, subTerm):
        for st in range(self.num_terms()):
            if self.sub_terms[st] == subTerm:
                return st
        print("Warning: Didn't get a subTerm pos. Function: get_sub_term_pos")
        return None

    def get_location_for_term(self, term):
        location = self.sub_terms.index(term)
        return location

    def get_same_subterms(self, other):
        same_subterms = []
        for self_term_num in range(self.num_terms()):
            for other_term_num in range(other.num_terms()):
                if self.sub_terms[self_term_num] == other.sub_terms[other_term_num]:
                    if not contains(same_subterms, self.subterms[self_term_num]):
                        same_subterms.append(self.sub_terms[self_term_num])
        return same_subterms

    def can_perform_ops(self, other):
        #NOTE: need to check vars, powers, subterms, termpowers and ownerterm.
        #check if we have the same vars
        if self.num_vars() != other.num_vars():
            return False
        num_vars = self.num_vars()
        for i in range(num_vars):
            if not self.has_var(other.vars[i]):
                return False
        #check powers
        for var in self.vars:
            if self.get_power_for_var(var) != other.get_power_for_var(var):
                return False
        for sub_term in self.sub_terms:
            if not other.has_subterm(sub_term):
                return False

    def print_term(self):
        out_str = self.operator
        out_str += str(self.num)
        num_vars = self.num_vars()
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
        same_vars = get_same_vars(self, other)
        for var in same_vars:
            self_pwr_loc = self.get_location_for_var(var)
            self_pwr = self.get_power_for_var(var)
            other_pwr = other.get_power_for_var(var)
            min_pwr = get_min_num([self_pwr, other_pwr])
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
            self_pwr = self.sub_terms[self_term_loc].power
            other_pwr = other.sub_terms[other_term_loc].power
            min_pwr = get_min_num([self_pwr, other_pwr])
            self.sub_terms[self_term_loc].power -= min_pwr
            if self.sub_terms[self_term_loc] == 0:
                del self.sub_terms[self_term_loc]
        del same_subterms

    def __eq__(self, other):
        if type(other) != term:
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

    def remove_extra_layers(self):
        for i in range(self.num_terms()):
            self.sub_terms[i].remove_extra_layers()
        #check if term has no vars and it's num is 1.
        if type(self.owner_term) == type(-1):
            print("owner_term is -1.")
            return
        elif type(self.owner_term.owner_term) == type(-1):
            print("owner of owner_term is -1.")
            return
        if self.owner_term.vars == [] and self.owner_term.num == 1:
            self.owner_term.owner_term.sub_terms = self.owner_term.sub_terms

    def convert_extra_floats(self, recursive = True):
        if recursive:
            for i in range(self.num_terms()):
                self.sub_terms[i].convert_extra_floats()
        if is_int(self.num):
            self.num = int(self.num)

    def update_operator(self, recursive = False): #if num < 0 and operator is +, set operator to - and flip self.num
        if recursive:
            for i in range(self.num_terms()):
                self.sub_terms[i].update_operator(recursive = True)
        if self.num < 0 and self.operator == "+":
            self.num = flip(self.num)
            self.operator = "-"
        elif self.num < 0 and self.operator == "-":
            self.num = flip(self.num)
            self.operator = "+"

    def is_perfect_square(self):
        if is_int(math.sqrt(self.num)):
            return False
        #check vars
        for i in range(self.num_vars()):
            if not is_int(self.powers[i] / 2):
                return False
        return True

    #TODO: Recursive function to collect like terms.
    def dev_factor(self):
        self.common_factor(recursive = True)
        self.factor_trinomial(recursive = True)
        self.update_operator(recursive = True)
        self.common_factor(recursive = True)
        self.remove_extra_layers()

    def debug_factor(self):
        self.common_factor(recursive = True)
        print("after first common factor:")
        print(self.get_bracket_string())
        self.factor_trinomial(recursive = True)
        print("after factor_trinomial:")
        print(self.get_bracket_string())
        self.update_operator(recursive = True)
        print("after update_operator:")
        print(self.get_bracket_string())
        self.common_factor(recursive = True)
        print("after second common_factor:")
        print(self.get_bracket_string())
        self.convert_extra_floats()

    def is_negative(self):
        self.update_operator()
        if self.operator == "-" or self.num < 0:
            return True

    def factor(self):
        self.common_factor(recursive = True)
        self.factor_trinomial(recursive = True)
        self.update_operator(recursive = True)
        self.common_factor(recursive = True)
        self.convert_extra_floats()

    #NOTE: Two identical terms multiplied by each other will not yet reduce properly.
    def common_factor(self, recursive = False):
        #recursion
        if recursive:
            for i in range(self.num_terms()):
                self.sub_terms[i].common_factor(recursive = True)

        #if two of the same subTerms are multiplied together, take out one and add one to the other one's power.
        num_terms = self.num_terms()
        i = 0
        while i < self.num_terms():
            if i + 1 >= num_terms: #we can't get the index of term + 1 if it's outside the scope of self.sub_terms.
                break
            if self.sub_terms[i] == self.sub_terms[i + 1] and self.sub_terms[i + 1].operator == "*":
                print("Got two terms multiplied by each other.")
                self.sub_terms[i].power += 1
                del self.sub_terms[i + 1]
            else:
                i += 1

        same_term_pos = []
        #find a term whose subterms are equal to another term's and that's not the same term
        for i in range(self.num_terms()):
            for n in range(self.num_terms()):
                if i != n:
                    term_i = self.sub_terms[i]
                    term_n = self.sub_terms[n]
                    if term_i.has_same_subterms(term_n):
        #find if there's already an array in same_term_pos that contains a location of said term.
                        has_found = False
                        for term_pos_i in range(len(same_term_pos)):
                            term_pos = same_term_pos[term_pos_i]
                            pos = term_pos[0]
                            search_term = self.sub_terms[pos]
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
        for i in range(self.num_terms()):
            self.sub_terms[i].to_del = False
        #loop same_term_pos
        n_same_terms = len(same_term_pos)
        if n_same_terms > 0:
            for same_terms in same_term_pos:
                pos = same_terms[0]
        del n_same_terms
        for i in range(len(same_term_pos)):
            #get the term in common. Save it for later.
            term_pos = same_term_pos[i][0]
            term_in_common = copy.deepcopy(self.sub_terms[term_pos])
            term_in_common.num = 1.
            term_in_common.operator = "*"
            term_in_common.vars = []
            term_in_common.to_del = False

            #get all the terms multiplied to the central term. Add them all to their own term.
            multiplied_term = term()
            multiplied_term.to_del = False
            for n in range(len(same_term_pos[i])):
                same_term = self.sub_terms[same_term_pos[i][n]]
                multiplied_term.sub_terms.append(same_term)
                self.sub_terms[same_term_pos[i][n]].to_del = True
            #remove the subTerms from multiplied_term's subterms since they've been factored out.
            for n in range(multiplied_term.num_terms()):
                multiplied_term.sub_terms[n].sub_terms = []
            self.sub_terms.append(multiplied_term)
            self.sub_terms.append(term_in_common)
        #delete subTerms marked for deletion.
        i = 0
        while i < self.num_terms():
            if self.sub_terms[i].to_del:
                del self.sub_terms[i]
            else:
                del self.sub_terms[i].to_del
                i += 1

        #do variables and numbers
        powers = {}
        vars = {}
        var_locs = {}
        #find the variables and their respective locations.
        for term1 in range(self.num_terms()):
            for term2 in range(self.num_terms()):
                if term1 != term2:
                    for vars2 in range(self.sub_terms[term2].num_vars()):
                        if self.sub_terms[term1].has_var(self.sub_terms[term2].vars[vars2]):
                            var = self.sub_terms[term2].vars[vars2]
                            power = self.sub_terms[term2].powers[vars2]
                            if var in vars:
                                vars[var] += 1
                            else:
                                vars[var] = 1
                            if not contains(var_locs, var):
                                var_locs[var] = []
                            if not contains(var_locs[var], [term2, vars2]):
                                var_locs[var].append([term2, vars2])
                                #subterm no., var pos
                            if var in powers:
                                powers[var] = get_min_num([powers[var], power])
                            else:
                                powers[var] = power
        #filter out the variables that not every subterm in the term has
        vars_to_del = []
        for var in vars:
            if not self.all_terms_have_var(var):
                vars_to_del.append(var)
        for var in vars_to_del:
            del var_locs[var]

        #subtract the powers and delete the power and it's respective variable if the power is zero.
        for var in var_locs:
            var_loc_arr = var_locs[var]
            self.vars.append(var)
            self.powers.append(powers[var])
            for var_loc in var_loc_arr:
                min_power = powers[var]
                #subtract the minimum power from the term's power.
                print(var_loc[0])
                print(var_loc[1])
                self.sub_terms[var_loc[0]].powers[var_loc[1]] -= min_power
                #if the term's power equals zero, delete the power and the variable.
                if self.sub_terms[var_loc[0]].powers[var_loc[1]] == 0:
                    del self.sub_terms[var_loc[0]].powers[var_loc[1]]
                    del self.sub_terms[var_loc[0]].vars[var_loc[1]]
        #finally, factor the numbers.
        lcm = get_lcm(self)
        for i in range(self.num_terms()):
            self.sub_terms[i].num /= lcm
        self.num *= lcm

    def factor_trinomial(self, recursive = False):
        #recursion
        if recursive:
            for term_num in range(self.num_terms()):
                self.sub_terms[term_num].factor_trinomial()

        #we can't factor it as a trinomial if we don't have 2 or 3 num_terms.
        if self.num_terms() != 3 and self.num_terms() != 2:
            return None
        if self.num_terms() == 3:
            a = self.sub_terms[0]
            b = self.sub_terms[1]
            c = self.sub_terms[2]
        elif self.num_terms() == 2:
            a = self.sub_terms[0]
            b = term()
            b.num = 1.
            c = self.sub_terms[1]
            #check if all subTerm's vars are squared.
            if not a.is_perfect_square() or not b.is_perfect_square():
                return

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
        first_bracket_mult.vars = get_same_vars(a, first_b_replacement)
        second_bracket_mult = term()
        second_bracket_mult.num = get_lcm_from_nums([second_b_replacement.num, c.num])
        second_bracket_mult.vars = get_same_vars(second_b_replacement, c)
        #pull out the negatives if need be.
        if a.is_negative() and first_b_replacement.is_negative():
            first_bracket_mult.num = flip(first_bracket_mult.num)
        if second_b_replacement.is_negative() and c.is_negative():
            second_bracket_mult.num = flip(second_bracket_mult.num)

        #remove the extra vars & their respective powers from the terms in the brackets.
        for var in first_bracket_mult.vars:
            #subtract the lowest of the powers from the powers.
            a_power_location = a.get_location_for_var(var)
            a_power = a.get_power_for_var(var)
            first_b_replacement_power_location = first_b_replacement.get_location_for_var(var)
            first_b_replacement_power = first_b_replacement.get_power_for_var(var)
            lowest_power = get_min_num([a_power, first_b_replacement_power])
            first_bracket_mult.powers.append(lowest_power)

            del a_power
            del first_b_replacement_power
            del a_power_location
            del first_b_replacement_power_location

        for var in second_bracket_mult.vars:
            #subtract the lowest of the powers from the powers
            second_b_replacement_power_location = second_b_replacement.get_location_for_var(var)
            second_b_replacement_power = second_b_replacement.get_power_for_var(var)
            cPowerLocation = c.get_location_for_var(var)
            cPower = c.get_power_for_var(var)
            min_power = getMinPower([second_b_replacement_power, cPower])
            second_bracket_mult.powers.append(min_power)

            del cPower
            del second_b_replacement_power
            del cPowerLocation
            del second_b_replacement_power_location
        #divide nums by bracket multipliers.
        a.div(first_bracket_mult)
        first_b_replacement.div(first_bracket_mult)
        second_b_replacement.div(second_bracket_mult)
        c.div(second_bracket_mult)

        self.sub_terms = [first_bracket_mult, second_bracket_mult]
        self.sub_terms[0].sub_terms = [a, first_b_replacement]
        self.sub_terms[1].sub_terms = [second_b_replacement, c]

    def print_tree(self, depthNum = 0): #print out the tree of terms. Useful for debug purposes.
        tab_string = ""
        for i in range(depthNum):
            tab_string += "    "
        #print own values
        out_string = tab_string + self.operator + str(self.num)
        for varNum in range(self.num_vars()):
            out_string += str(self.vars[varNum]) + "^" + str(self.powers[varNum])
        print(out_string)
        #call kids' recursive functions.
        for term in range(self.num_terms()):
            self.sub_terms[term].print_tree(depthNum + 1)

    def print_brackets(self, recursive = False):
        bracket_string = self.operator + str(self.num)
        for i in range(self.num_vars()):
            var = self.vars[i]
            power = self.powers[i]
            bracket_string += var
            if power != 1:
                bracket_string += "^" + str(power)
        if self.num_terms() > 0: #we don't need brackets around every single term (eg. ((3x) + (3))) -- it would be annoyng.
            bracket_string += "("
        print(bracket_string, end="")
        #recursion
        if recursive:
            for i in range(self.num_terms()):
                self.sub_terms[i].print_brackets(recursive = True)
        if self.num_terms() > 0: #we don't need brackets around every single term (eg. ((3x) + (3))) -- it would be annoyng.
            if type(self.owner_term) != type(-1): #we only want a newline after we've printed out all the terms.
                print(")", end="")
            elif type(self.owner_term) == type(-1): #we only want a newline after we've printed out all the terms.
                print(")", end="")

    def get_bracket_string(self):
        if self.num == 1 and (self.vars != [] or self.sub_terms != []):
            bracket_string = self.operator
        else:
            bracket_string = self.operator + str(self.num)
        for i in range(self.num_vars()):
            var = self.vars[i]
            power = self.powers[i]
            bracket_string += var
            if power != 1:
                bracket_string += "^" + str(power)
        if self.num_terms() > 0: #we don't need brackets around every single term (eg. ((3x) + (3))) -- it would be annoyng.
            bracket_string += "("
        #recursion
        for i in range(self.num_terms()):
            bracket_string += self.sub_terms[i].get_bracket_string()
        if self.num_terms() > 0: #we don't need brackets around every single term (eg. ((3x) + (3))) -- it would be annoyng.
            bracket_string += ")"
        #NOTE: bracket powers haven't been implemented yet.
        if self.power != 1:
            bracket_string += "^" + str(self.power)
        return bracket_string

    def get_subterm_string(self):
        bracket_string = self.get_bracket_string()
        bracket_pos = bracket_string.index("(")
        bracket_string = bracket_string[bracket_pos:]
        return bracket_string

def flip(num):
    return num / -1

def contains(array, search):
    for element in array:
        if element == search:
            return True
    return False

def get_num_at_pos(equation, pos): #gets the number after a position. Useful for finding the number after an operation (eg. ^, +, /)
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
    if num % 1 == 0:
        return True
    else:
        return False

def is_in(string, char):
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

def get_lcm(term): #get the lowest common multiple
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
    for multiple in range(maxLcm, 0, -1):
        works = True
        for num in nums:
            if not is_int(num / multiple):
                works = False
        if works:
            return multiple
    return 1

def get_min_num(array):
    min_num = array[0]
    for element in array:
        if element < min_num:
            min_num = element
    return min_num

def get_same_vars(term1,term2):#returns vars & the smallest powers.
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
    if get_type(raw_equation[location-1]) == ")":
        return True

def remove_duplicates(array):
    new_array = []
    for element in array:
        if not contains(new_array, element):
            new_array.append(element)
    return new_array

terms = term()
terms.operator = "+"
current_bracket = 0
current_num = 0
raw_equation = argv[1]

#generate term tree
equation_len = len(raw_equation)
equation_num = 0
term_obj_num = 0

while equation_num < equation_len:
    equation_element = raw_equation[equation_num]
    equation_type = get_type(equation_element)
#    print("Checking element "+str(equation_num) + " which is of type " + equation_type)
    if equation_type == "(": #go down a level of recursion
        terms.sub_terms.append(term())
        terms.sub_terms[-1].owner_term = terms
        terms = terms.sub_terms[-1]
    elif equation_type == ")": #come back up a level of recursion
        terms = terms.owner_term
    elif equation_type == "num":
        if(terms.num == 1):
            terms.num, num_length = get_num_at_pos(raw_equation, equation_num)
            equation_num += num_length - 1
    elif equation_type == "var":
        terms.vars.append(equation_element)
        terms.powers.append(1)
    elif equation_type == "^":
        if not is_term_power(equation_num): #tell the difference between a power acting on an entire term or just a power acting on a variable.
            terms.powers[-1], num_length = get_num_at_pos(raw_equation, equation_num + 1)
        else:
            terms.sub_terms[-1].power, num_length = get_num_at_pos(raw_equation, equation_num + 1)
        equation_num += num_length
    elif equation_type == "operator":
        #Go to the next term.
        terms = terms.owner_term
        terms.sub_terms.append(term())
        terms.sub_terms[-1].owner_term = terms
        terms = terms.sub_terms[-1]
        terms.operator = equation_element
    equation_num += 1

#TODO: Get operations to perform from argv

terms.set_sub_term_owners()
terms.debug_factor()
#terms.factor()
#terms.dev_factor()
print(terms.get_bracket_string())
