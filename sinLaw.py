#!/usr/bin/env python3.6
import math
import sys
if len(sys.argv) < 4:
    print("Usage: "+sys.argv[0]+" <a> <A> <b> <B>")
    print("a/sinA = b/sinB")
    print("Enter the data you have (which should be 3 arguments).")
    print('Leave the one to find out as an empty string - ex. ""')
    sys.exit()
a = sys.argv[1]
A = sys.argv[2]
b = sys.argv[3]
B = sys.argv[4]
for argumentNum in range(len(sys.argv)):
    if sys.argv[argumentNum] == "":
        argumentToFind = argumentNum
        break
if argumentToFind == 1:#find a
    A = math.radians(float(A))#the math library only likes radians
    b = float(b)
    B = math.radians(float(B))
    solution = (b*math.sin(A))/math.sin(B)
elif argumentToFind == 2:#find A
    a = float(a)
    b = float(b)
    B = math.radians(float(B))
    solution = math.degrees(math.asin((a*math.sin(B))/b))
elif argumentToFind == 3:#find b
    a = float(a)
    A = math.radians(float(A))
    B = math.radians(float(B))
    solution = (a*math.sin(B))/math.sin(A)
elif argumentToFind == 4:#find B
    a = float(a)
    A = math.radians(float(A))
    b = float(b)
    solution = math.degrees(math.asin((b*math.sin(A))/a))
print(str(solution))
