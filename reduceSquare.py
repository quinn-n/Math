#!/usr/bin/env python3
from sys import argv

if len(argv) < 3:
    print("Usage: " + argv[0] + " <multiplier> <sqrt num>")
    exit()

def isInt(num):
    return (num % 1 == 0)

multiplier = float(argv[1])
num = float(argv[2])
power = 50
while power > 0:
    perfectSquare = power ** 2
    if isInt(num / perfectSquare):
        break
    power -= 1

print("Got perfectSquare: " + str(perfectSquare) + " and power: " + str(power))

multiplier *= power
num /= perfectSquare

print(str(multiplier) + " sqrt " + str(num))
