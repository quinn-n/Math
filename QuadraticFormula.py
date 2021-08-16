#!/usr/bin/env python
#TODO: Add support for imaginary numbers.
import sys
import math
if len(sys.argv) < 4: #make sure we got all our variables
    print("Usage: "+sys.argv[0]+" <a> <b> <c>")
    print("Finds the value of the variable using a quadratic equation.")
    sys.exit()
#store our inputs in easier to remember variables.
a = float(sys.argv[1])
b = float(sys.argv[2])
c = float(sys.argv[3])
#Here we add support for decimal inputs. (multiply them by increments of 10 until they are whole numbers)
multiplier = 1
oldA = a
oldB = b
oldC = c
if not a.is_integer() or not b.is_integer() or not c.is_integer(): #we do not need to re-divide these numbers at the end, as the denominator is a number divided by an integer.
    print("Decimals detected in input. Rectifying.")
    while not a.is_integer() or not b.is_integer() or not c.is_integer():
        multiplier = multiplier*10
        a = oldA*multiplier
        b = oldB*multiplier
        c = oldC*multiplier
print("Got a: "+str(a))
print("Got b: "+str(b))
print("Got c: "+str(c))
#plug our variables into both the sub & add versions of the equation.
if b*b-4*a*c < 0: #math.sqrt won't work with negative numbers, so we need to work around it.
    print("Square rooted part is negative. Problem is not solvable.")
    squareRoot = math.sqrt((b*b-4*a*c)/-1)
    negative = True
else:
    print("Square rooted part is positive.")
    squareRoot = math.sqrt(b*b-4*a*c)
    negative = False
#Plug the square root into the rest of the equation. If it would be a messy output, we also include a version where it hasn't been square rooted yet. That part comes later.
addEquations = []
subEquations = []
if not negative:
    addEquations.append(((b/-1)+squareRoot)/(2*a))
    subEquations.append(((b/-1)-squareRoot)/(2*a))
else:
    divider = 2*a
    addEquations.append("("+str((b/-1)/multiplier)+"+√"+str((b*b-4*a*c)/multiplier)+")/("+str(divider/multiplier)+")")
    subEquations.append("("+str((b/-1)/multiplier)+"-√"+str((b*b-4*a*c)/multiplier)+")/("+str(divider/multiplier)+")")

#print our results.
for readableOutputLoop in range(len(addEquations)): #this is where we check & insert another answer if squareRoot is an ugly number (has a decimal)
    addEquation = addEquations[readableOutputLoop]
    subEquation = subEquations[readableOutputLoop]
    if type(addEquation) != str and type(subEquation) != str: #we can't check if a string is an integer.
        if not addEquation.is_integer() or not subEquation.is_integer():
            divider = 2*a
            addEquations.append("("+str((b/-1)/multiplier)+"+√"+str((b*b-4*a*c)/multiplier)+")/("+str(divider/multiplier)+")")
            subEquations.append("("+str(b/-1)+"-√"+str((b*b-4*a*c))+")/("+str(divider)+")")

for printLoop in range(len(addEquations)): #Loop through all the equations to print them all out.

    addEquation = addEquations[printLoop]
    subEquation = subEquations[printLoop]

    print("x = "+str(subEquation)+", "+str(addEquation))
