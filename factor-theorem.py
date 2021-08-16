#!/usr/bin/env python

"""
factor-theorem.py
Finds the first value for a that makes f(a) = 0
Written by happylego91
https://gitlab.com/happylego91
Written on Oct. 8th 2019
"""

from sys import argv

import progutil

ISINT_TOLERANCE = .00000001

HELP_MSG = """Usage: factor-theorem.py <polynomial> <constant>"""

def is_int(n: int):
    """Returns true if n is an integer"""
    return abs(n % 1) < ISINT_TOLERANCE

def get_factors(n: int):
    """Returns the possible factors for an integer"""
    factors = []
    for i in range(1, n + 1):
        if is_int(n / i):
            factors.append(i)
            factors.append(i * -1)
    return factors

#Verify inputs
if not progutil.check_inputs(argv, 3, HELP_MSG):
    exit(1)

poly = argv[1]
const = int(argv[2])

facts = get_factors(const)

zeros = []

#Run each factor looking for zeros
for x in facts:
    rem = eval(poly)
    print("Got remainder", rem, "for", x)
    if rem == 0:
        zeros.append(x)

#Print out the zeros
print("Got zeros:")
for zero in zeros:
    print("f(" + str(zero) + ") = 0")