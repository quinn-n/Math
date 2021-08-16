#!/usr/bin/env python
import math
import sys
if len(sys.argv) < 4:
    print("Usage: "+sys.argv[0]+" <c> <a> <b> <C>")
    print("Leave the one you want to find as an empty string.")
    print("Ex. "+sys.argv[0]+' 3 5 4 ""')
    sys.exit()
for argumentNum in range(len(sys.argv)):
    if sys.argv[argumentNum] == "" or sys.argv[argumentNum] == None:
        argumentToFind = argumentNum
        break
c = sys.argv[1]
a = sys.argv[2]
b = sys.argv[3]
C = sys.argv[4]
if argumentToFind == 1:#find c
    print("finding c...")
    a = float(a)
    b = float(b)
    C = math.radians(float(C))
    solution = math.sqrt(a*a+b*b-2*a*b*math.cos(C))
elif argumentToFind == 4:#find C
    print("finding C...")
    c = float(c)
    a = float(a)
    b = float(b)
    solution = math.degrees(math.acos((c*c-(a*a+b*b))/(-2*a*b)))
print(str(solution))
