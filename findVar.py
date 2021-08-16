#!/usr/bin/env python
# Written by happylego91
#
# Finds the missing variable (does not work with powers (yet))
from sys import argv
import term

def main():
    #check that we have the equation
    if len(argv) != 2:
        print("Usage: " + argv[0] + " <equation>")
        print("Finds a variable in an equation.")
        exit()
    #help
    elif argv[1] == "-h" or argv[1] == "--help":
        print("Usage: " + argv[0] + " <equation>")
        print("Finds a variable in an equation.")
        exit()
    equation = argv[1]
    #split the equation
