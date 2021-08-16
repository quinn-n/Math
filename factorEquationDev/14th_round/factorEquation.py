#!/usr/bin/env python
"""
Written and maintained by happylego91. https://gitlab.com/happylego91

"""
from sys import argv
import term

if len(argv) < 2:
    print("Usage: "+argv[0]+" <equation>")
    print("Factors an equation. Hopefully. That's the plan anyways.")
    print("Example: '(3x+3)' should return 3(x+1)")
    exit()

#generate term tree
terms = term.get_term_from_string(argv[1])

#TODO: Get operations to perform from argv

print("Got terms: " + terms.get_bracket_string())

terms.set_sub_term_owners()
terms.debug_factor()
#terms.factor()
#terms.dev_factor()
print(terms.get_bracket_string())
terms.update_operator(recursive=True)
print("final result:")
print(terms.get_bracket_string())
