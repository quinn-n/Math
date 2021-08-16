#!/usr/bin/env python3
import math
import sys

argc = len(sys.argv)

if argc == 5:
    y1Mult = 1
    y2Mult = 1

    m1 = float(sys.argv[1])
    b1 = float(sys.argv[2])

    m2 = float(sys.argv[3])
    b2 = float(sys.argv[4])

elif argc == 7:
    y1Mult = float(sys.argv[1])
    m1 = float(sys.argv[2])
    b1 = float(sys.argv[3])

    y2Mult = float(sys.argv[4])
    m2 = float(sys.argv[5])
    b2 = float(sys.argv[6])

else:
    print("Usage: " + sys.argv[0] + " <[y1 mult]> <first m value> <first b value> <[y2 mult]> <second m value> <second b value>")
    sys.exit()

m1 /= y1Mult
b1 /= y1Mult

m2 /= y2Mult
b2 /= y2Mult

newM = m1 - m2
newB = b1 - b2

x = (newB / -1.) / newM

y = m1 * x + b1

x = str(x)
y = str(y)

print("POI is: (" + x + ", " + y + ")")
