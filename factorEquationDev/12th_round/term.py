#!/usr/bin/env python
"""
Written and maintained by happylego91. https://gitlab.com/happylego91

"""
import math
import copy

#maxLcm = 1000

chars = "abcdefghijklmnopqrstuvwxyz"
nums = range(10)
operators = "+-*/"
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
    """term is used to perform mathematical operations on variables you don't know.
    Ex. 3x + x = 4x"""
    def __init__(self, num=1):
        self.vars = []
        self.sub_terms = []
        self.powers = []
        self.operator = "+"
        if num < 0:
            num *= -1
            self.operator = "-"
        self.num = float(num)
        self.owner_term = -1
        self.power = 1
        self.has_run_startup = False
        #TODO: self.imaginary_num
    def num_terms(self):
        """returns the number of subterms self has."""
        return len(self.sub_terms)
    def num_vars(self):
        """returns the number of variables self has."""
        return len(self.vars)
    def num_powers(self):
        """returns the number of powers self has. Should be equal to num_vars."""
        return len(self.powers)

    def __add__(self, other):
        """add two terms."""
        if type(other) != term:
            if type(other) == int or type(other) == float:
                new_other = term()
                new_other.num = other
                other = copy.deepcopy(new_other)
                del new_other
            else:
                return
        self_terms_string = self.get_subterm_string()
        other_terms_string = other.get_subterm_string()
        self_vars = self.vars
        other_vars = other.vars
        self_powers = self.powers
        other_powers = other.powers
        if self_terms_string == other_terms_string and self_vars == other_vars and self_powers == other_powers:
            self.num += other.num
    def __sub__(self, other):
        """subtract other from self."""
        if type(other) != term:
            if type(other) == int or type(other) == float:
                new_other = term()
                new_other.num = other
                other = copy.deepcopy(new_other)
                del new_other
            else:
                return
        self_terms_string = self.get_subterm_string()
        other_terms_string = other.get_subterm_string()
        self_vars = self.vars
        other_vars = other.vars
        self_powers = self.powers
        other_powers = other.powers
        if self_terms_string == other_terms_string and self_vars == other_vars and self_powers == other_powers:
            self.num -= other.num
    def __mul__(self, other):
        """multiply self by other."""
        if type(other) != term:
            if type(other) == int or type(other) == float:
                new_other = term()
                new_other.num = other
                other = copy.deepcopy(new_other)
                del new_other
            else:
                return
        #NOTE: left off here
        same_vars = self.get_same_vars(other)
        #add powers
        new_term = copy.deepcopy(self)
        for var in same_vars:
            same_vars_arr = same_vars[var]
            self_pwr_loc = self.get_location_for_var(var)
            self_pwr = self.powers[self_pwr_loc]
            other_pwr_loc = other.get_location_for_var(var)
            other_pwr = other.powers[other_pwr_loc]
            new_term.powers[self_pwr_loc] = self_pwr + other_pwr
        #add vars that aren't in both terms
        for var in other.vars:
            if not contains(same_vars, var):
                new_term.vars.append(var)
                new_term.powers.append(1)

        new_term.num *= other.num
        return new_term

    #check for vars with a power of zero and remove them.
    def remove_zero_powers(self):
        """remove all vars with a power of zero."""
        i = 0
        while i < self.num_vars():
            if self.powers[i] == 0:
                del self.vars[i]
                del self.powers[i]
            else:
                i += 1

    def remove_zero_power_terms(self):
        """remove all subterms with a power of zero."""
        i = 0
        while i < self.num_terms():
            if self.sub_terms[i].power == 0 and (self.sub_terms.operator == "+" or self.sub_terms.operator == "-"):
                del self.sub_terms[i]
            else:
                i += 1

    def invert_operator(self):
        """if self.operator is + or -, invert it and return True. Else, return False."""
        if self.operator == "+":
            self.operator = "-"
            return True
        elif self.operator == "-":
            self.operator = "+"
            return True
        return False

    def __truediv__(self, other, whole_fraction=False):
        """divide self by other.

        May return a numerator and denominator if whole_fraction is false."""
        numerator = copy.deepcopy(self)
        denominator = copy.deepcopy(other)
        if whole_fraction:
            lcm_term = term()
            lcm_term.sub_terms[0] = numerator
            lcm_term.sub_terms[1] = denominator
            lcm = get_lcm(lcm_term)
            del lcm_term
            numerator.num /= lcm
            denominator.num /= lcm
        else:
            print("dividing num by " + str(denominator.num) + " with operator " + denominator.operator)
            #if our denominator is negative, invert the sign on the numerator and denominator.
            #NOTE: numerator's operator is not being inverted properly.
            if denominator.operator == "-":
                print("inverting numerator operator.")
                numerator.invert_operator()
                denominator.invert_operator()
            numerator.num /= denominator.num
            denominator.num = 1.
        #reduce vars
        same_vars = numerator.get_same_vars(denominator)
        for var in same_vars:
            numerator_pwr_loc = numerator.get_location_for_var(var)
            denominator_pwr_loc = denominator.get_location_for_var(var)
            numerator_pwr = numerator.powers[numerator_pwr_loc]
            denominator_pwr = denominator.powers[denominator_pwr]
            min_pwr = get_min_num([numerator_pwr, denominator_pwr])
            numerator.powers[numerator_pwr_loc] -= min_pwr
            denominator.powers[denominator_pwr_loc] -= min_pwr
        #check for vars with a power of 0 and remove them.
        numerator.remove_zero_powers()
        denominator.remove_zero_powers()
        #reduce terms
        same_terms = numerator.get_same_subterms(denominator)
        for term in same_terms:
            numerator_pos = numerator.get_location_for_term(term)
            denominator_pos = denominator.get_location_for_term(term)
            numerator_pwr = numerator.subs[numerator_pos].power
            denominator_pwr = denominator.sub_terms[denominator_pos].power
            min_pwr = get_min_num([numerator_pwr, denominator_pwr])
            numerator.sub_terms[numerator_pos].power -= min_pwr
            denominator.sub_terms[denominator_pos].power -= min_pwr
        del same_terms
        numerator.remove_zero_power_terms()
        denominator.remove_zero_power_terms()
        numerator.update_operator(recursive = True)
        denominator.update_operator(recursive = True)
        if denominator.operator == "-":
            numerator.invert_operator()
            denominator.invert_operator()
        print("truediv returning " + numerator.get_bracket_string() + ", " + denominator.get_bracket_string())
        return numerator, denominator

    def div_with_subterms(self, other):
        """recursively divide self and it's subterms by other."""
        #check if other is a term.
        if type(other) != term:
            #if other is a number, we can still divide by it.
            if type(other) == int or type(other) == float:
                other = term(other)
                other.update_operator()
            else:
                return
        cache_term, _ = self / other
        print("cache_term: " + cache_term.get_bracket_string())
        #copy all the values over from cache_term to self
        self.vars = copy.deepcopy(cache_term.vars)
        self.num = cache_term.num
        self.powers = copy.deepcopy(cache_term.powers)
        self.operator = cache_term.operator
        #print out the root term for debugging purposes
        print("Root term: " + self.debug_get_root_term_string())
        del cache_term

        #recursion
        for i in range(self.num_terms()):
            self.sub_terms[i].div_with_subterms(other)

    def perform_operation(self, other):
        if other.operator == "+":
            return self + other
        elif other.operator == "-":
            return self - other
        elif other.operator == "*":
            return self * other
        elif other.operator == "/":
            return self / other

    def all_terms_have_var(self, var):
        """check if all the subterms have the variable var."""
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

    def set_sub_term_owners(self):
        """recursively setup the ownership variable so we can perform recursive operations on the class."""
        for i in range(len(self.sub_terms)):
            self.sub_terms[i].owner_term = self
            self.sub_terms[i].set_sub_term_owners()
    def has_var(self, var):
        """check if self.vars contains var"""
        for array_var in self.vars:
            if array_var == var:
                return True
        return False

    def get_location_for_var(self, var):
        """returns the location of var in self.vars"""
        return get_idx(self.vars, var)

    def get_power_for_var(self, var):
        """get the power for a variable var."""
        location = self.get_location_for_var(var)
        return self.powers[location]

    def get_sub_term_pos(self, sub_term):
        """get the position of subTerm in self.sub_terms"""
        for st in range(self.num_terms()):
            if self.sub_terms[st] == sub_term:
                return st
        print("Warning: Didn't get a subTerm pos. Function: get_sub_term_pos")
        return None

    def get_location_for_term(self, term):
        """returns the location for the sub_term term."""
        for i in range(self.num_terms()):
            if self.sub_terms[i] == term:
                print("get_location_for_term returning " + str(i))
                return i

    def get_same_subterms(self, other):
        """get the same subterms between the two terms self and other.

        returns an array that looks like [terms]"""
        same_subterms = []
        #loop over all our subterms
        for self_term_num in range(self.num_terms()):
            #loop over all other's subterms
            for other_term_num in range(other.num_terms()):
                if self.sub_terms[self_term_num] == other.sub_terms[other_term_num]:
                    print("got same subterms.")
                    if not contains(same_subterms, self.sub_terms[self_term_num]):
                        same_subterms.append(self.sub_terms[self_term_num])
                else:
                    print("get_same_subterms calling div_with_subterms...")
                    other.div_with_subterms(-1)
                    print("div_with_subterms done being called for the first time from get_same_subterms.")
                    if self.sub_terms[self_term_num] == other.sub_terms[other_term_num]:
                        print("got same subterms (-1)")
                        if not contains(same_subterms, self.sub_terms[self_term_num]):
                            same_subterms.append(self.sub_terms[self_term_num])
                    else:
                        other.div_with_subterms(-1)
        return same_subterms

    def can_perform_ops(self, other):
        """returns true if we can perform operations on self and other."""
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
        """depricated (hopefully). Use __truediv__."""
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
        #print("__eq__ checking " + self.get_bracket_string() + " against " + self.get_bracket_string())
        if self.get_bracket_string() == other.get_bracket_string():
            return True
        else:
            return False
    def eq_after_invert(self, other):
        self_cache = copy.deepcopy(self)
        self_cache.div_with_subterms(-1)
        if self_cache.get_bracket_string() == other.get_bracket_string():
            return True
        else:
            return False


    def has_same_subterms(self, other):
        """returns true if self has the same subterms as other."""
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

    def get_same_vars(self, other): #returns a dict full of arrays that contain the positions of the vars.
        vars = {}
        for i in range(self.num_vars()):
            self_var = self.vars[i]
            for n in range(other.num_vars()):
                other_var = other.vars[n]
                if other_var == self_var:
                    if not contains(vars, self_var):
                        vars[self_var] = [i, n]
                    else:
                        vars[self_var].append(n)
        return vars
    def get_same_vars_in_subterms(self):
        vars = {}
        for i in range(self.num_terms()):
            for n in range(self.num_terms()):
                if i != n:
                    termi = self.sub_terms[i]
                    termn = self.sub_terms[n]
                    for var in termi.vars:
                        if termn.has_var(var):
                            if contains(vars, var):
                                vars[var].append(n)
                            else:
                                vars[var] = [i, n]
        for var in vars:
            vars[var] = remove_duplicates(vars[var])
        return vars

    #TODO: Recursive function to collect like terms.
    def dev_factor(self):
        self.update_operator(recursive = True)
        self.common_factor(recursive = True)
        print("after first common_factor: ")
        self.set_sub_term_owners()
        print(self.get_bracket_string())
        self.factor_trinomial(recursive = True)
        print("after factor_trinomial: ")
        self.set_sub_term_owners()
        print(self.get_bracket_string())
        self.set_sub_term_owners()
        self.update_operator(recursive = True)
        self.common_factor(recursive = True)

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
        self.remove_extra_layers()
        print("after remove_extra_layers:")
        print(self.get_bracket_string())

    def is_negative(self):
        """returns true if self is negative."""
        self.update_operator()
        if self.operator == "-" or self.num < 0:
            return True

    def factor(self):
        """factor self. Calls the functions that work. (most of the time)

        calls common_factor, then factor_trinomial, then update_operator,
        then common_factor, then convert_extra_floats."""
        self.common_factor(recursive=True)
        self.factor_trinomial(recursive=True)
        self.update_operator(recursive=True)
        self.common_factor(recursive=True)
        self.convert_extra_floats()

    #NOTE: Two identical terms multiplied by each other will not yet reduce properly.
    def common_factor(self, recursive=False):
        """factor out common terms and vars."""
        #recursion
        if recursive:
            for i in range(self.num_terms()):
                self.sub_terms[i].common_factor(recursive=True)

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
        #find a term whose subterms are equal to another's
        for i in range(self.num_terms()):
            for n in range(self.num_terms()):
                if i != n:
                    term_i = copy.deepcopy(self.sub_terms[i])
                    term_n = copy.deepcopy(self.sub_terms[n])
                    if term_i.has_same_subterms(term_n):
                        #find if there's already an array in same_term_pos that contains a location of said term.
                        print("Got same subterms between term " + term_i.get_bracket_string() + " and " + term_n.get_bracket_string())
                        has_found = False
                        for term_pos_i in range(len(same_term_pos)):
                            term_pos = same_term_pos[term_pos_i]
                            pos = term_pos[0]
                            search_term = self.sub_terms[pos]
                            if search_term == term_i:
                                #if there is, append it to the respective position of same_term_pos
                                print("has_found is true.")
                                same_term_pos[term_pos_i].append(i)
                                same_term_pos[term_pos_i].append(n)
                                has_found = True
                            #else, append a new array.
                        if not has_found:
                            print("has_found is false. Appending new array.")
                            same_term_pos.append([i, n])
                    #check term_n / -1
                    else:
                        term_n.div_with_subterms(-1)
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
                                print("has_found is false. Appending new array.")
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
            term_in_common.powers = []
            term_in_common.to_del = False
            print("term_in_common: " + term_in_common.get_bracket_string())

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
        min_powers = {}
        vars = self.get_same_vars_in_subterms()
        #remove the vars that not every subterm has.
        vars_to_del = []
        for var in vars:
            for i in range(self.num_terms()):
                if not self.sub_terms[i].has_var(var):
                    vars_to_del.append(var)
        remove_duplicates(vars_to_del)
        for var in vars_to_del:
            del vars[var]
        del vars_to_del
        #find the smallest power per variable.
        for var in vars:
            terms_with_var = vars[var]
            powers = []
            for i in terms_with_var:
                pwr = self.sub_terms[i].get_power_for_var(var)
                powers.append(pwr)
            min_pwr = get_min_num(powers)
            min_powers[var] = min_pwr
        #subtract the powers for each variable from the minimum power for said variable, if said term contains variable.
        for i in range(self.num_terms()):
            for var in min_powers:
                min_pwr = min_powers[var]
                pwr_loc = self.sub_terms[i].get_location_for_var(var)
                if pwr_loc != None:
                    self.sub_terms[i].powers[pwr_loc] -= min_pwr
        #remove vars with power of zero.
        for i in range(self.num_terms()):
            self.sub_terms[i].remove_zero_powers()
#        vars[x] = subterms with var
        for var in vars:
            subterms_with_var = vars[var]
            var_locs[var] = []
            for term_num in subterms_with_var:
                var_pos = self.sub_terms[term_num].get_location_for_var(var)
                var_locs[var].append([term_num, var_pos])
        #now add vars and powers to self's terms and powers.
        for var in min_powers:
            min_pwr = min_powers[var]
            if self.has_var(var):
                pwr_loc = self.get_location_for_var(var)
                self.powers[pwr_loc] += min_pwr
            else:
                self.vars.append(var)
                self.powers.append(min_pwr)
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
            min_power = get_min_num([second_b_replacement_power, cPower])
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

    def debug_get_root_term_string(self):
        current_term = self
        while current_term.owner_term != -1:
            current_term = current_term.owner_term
        return current_term.get_bracket_string()

    def get_root_term(self):
        """Returns the root term object.

        Ie. the term object at the root of the tree."""
        current_term = self
        while current_term.owner_term != -1:
            current_term = current_term.owner_term
        return current_term

    def get_bracket_string(self):
        """get the term self as a string."""
        #if num is a 1 and it isn't alone, we don't have to add it to the string.
        if self.num == 1 and (self.vars != [] or self.sub_terms != []):
            bracket_string = self.operator
        else:
            bracket_string = self.operator + str(self.num)
        #bracket_string = self.operator + str(self.num)
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
        """Get the string for the subterms, ignoring self's num, operator and vars."""
        bracket_string = self.get_bracket_string()
        bracket_pos = bracket_string.index("(")
        bracket_string = bracket_string[bracket_pos:]
        return bracket_string

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
    #Get maxLcm from all the terms.
    max_lcm = 1
    for i in range(term.num_terms()):
        max_lcm *= term.sub_terms[i].num

    max_lcm = int(math.ceil(max_lcm))

    if num_terms > 0:
        for multiple in range(max_lcm, 0, -1):
            works = True
            for term_num in range(num_terms):
                if not is_int(term.sub_terms[term_num].num / multiple):
                    works = False
            if works:
                return multiple
    return 1

def get_lcm_from_nums(nums):
    """returns the lowest common multiple from an array of numbers."""
    #get max_lcm by multiplying all the nums together.
    max_lcm = 1
    for num in nums:
        max_lcm *= num
    max_lcm = int(math.ceil(max_lcm))
    #Go over all the numbers from max_lcm to 1, checking if each number works.
    for multiple in range(max_lcm, 0, -1):
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

def remove_duplicates(array):
    """returns a new array that is like array but without any duplicate elements."""
    new_array = []
    for element in array:
        if not contains(new_array, element):
            new_array.append(element)
    return new_array

def is_term_power(string, location):
    """returns true if the power at location belongs to a term."""
    if get_type(string[location-1]) == ")":
        return True

def get_term_from_string(string):
    """Gets a term object from a string. Eg. "(3x + 2)" will return a term with the subterms 3x and 2."""
    out_term = term()
    strlen = len(string)
    equation_num = 0
    term_num = 0
    #iterate over each char in the string.
    current_term = term()
    while equation_num < strlen:
        equation_element = string[equation_num]
        equation_type = get_type(equation_element)
        #go down a level of recursion
        if equation_type == "(":
            current_term.sub_terms.append(term())
            current_term.sub_terms[-1].owner_term = current_term
            current_term = current_term.sub_terms[-1]
            term_num = 0
        #come back up a level of recursion
        elif equation_type == ")":
            current_term = current_term.owner_term
        #set .num
        elif equation_type == "num":
            current_term.owner_term.has_run_startup = True
            if(current_term.num == 1):
                #we need to get the entire number and the length
                #of the number in case it's more than 1 didget - ie. 37
                current_term.num, num_length = get_num_at_pos(string, equation_num)
                #add to the element we're working on so we don't end up reading the same number multiple times
                equation_num += num_length - 1
        elif equation_type == "var":
            #append the var and a new power for it to the term
            current_term.vars.append(equation_element)
            current_term.powers.append(1)
            current_term.owner_term.has_run_startup = True
        elif equation_type == "^":
            #tell the difference between a power acting on a variable and a power acting on an entire term
            if not is_term_power(string, equation_num):
                current_term.powers[-1], num_length = get_num_at_pos(string, equation_num + 1)
            else:
                current_term.sub_terms[-1].power, num_length = get_num_at_pos(string, equation_num + 1)
            equation_num += num_length
        #Go to the next term
        elif equation_type == "operator":
            #if we've already added some data to the term, create a new term
            if current_term.owner_term.has_run_startup:
                print("Running startup on " + equation_element)
                current_term = current_term.owner_term
                current_term.sub_terms.append(term())
                current_term.sub_terms[-1].owner_term = current_term
                current_term = current_term.sub_terms[-1]
            #else, just change the operator of the current term.
            else:
                current_term.owner_term.has_run_startup = True
            current_term.operator = equation_element
        equation_num += 1
    out_term = copy.deepcopy(current_term.get_root_term())
    return out_term
