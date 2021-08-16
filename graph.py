#!/usr/bin/env python
"""
graph.py
Graphs equations
Written by happylego91
Oct. 19 2019
"""

from sys import argv

import matplotlib.pyplot as plt
import numpy as np

import progutil

HELP_MSG = """Usage: graph.py <equation(s)> [-sen]
-s - start x
-e - end x
-n - number of points
Graphs 2d equations"""

#Default start, end and number of points
DEFAULT_START = -10
DEFAULT_END = 10
DEFAULT_PONTS = 1000

#Verify inputs
if not progutil.check_inputs(argv, 2, HELP_MSG):
    exit(1)

args = progutil.parse_inputs(argv, guaranteed=["s", "e", "n"], default=None)

#Set start
if args["s"] == None:
    start = DEFAULT_START
else:
    start = int(args["s"])

#Set end
if args["e"] == None:
    end = DEFAULT_END
else:
    end = int(args["e"])

#Set number of points
if args["n"] == None:
    points = DEFAULT_PONTS
else:
    points = int(args["n"])

n_fcns = len(argv) - 1

plt.title("Functions")

plt.xlabel("x")
plt.ylabel("f(y)")

x = np.linspace(start, end, points)

#Add functions to plot
for i in range(n_fcns):
    fcn = argv[i + 1]
    #Break when we get to the arguments
    if fcn[0] == "-":
        break
    plt.plot(x, eval(fcn), label=fcn)

plt.legend()

plt.show()