#!/usr/bin/env python
""" Written by happylego91
Performs a log operation with a given x and base.

"""
from math import log
from sys import argv

if len(argv) < 2:
    print("Usage: log.py <power> <[base]>")
    exit()
elif argv[1] == "-h":
    print("Usage: log.py <power> <[base]>")
    exit()
power = float(argv[1])
base = 10
if len(argv) == 3:
    base = float(argv[2])

print(log(power, base))
