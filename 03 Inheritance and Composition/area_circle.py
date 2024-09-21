# Original Version that failes the tests.
# import math
# def area_circle(r):
#     return math.pi * r ** 2

import math
# Revision 1
def area_circle(r):
    if r < 0:
        raise ValueError("Radius cannot be negative.")
    if not isinstance(r, (int,float)):
        raise TypeError("Radius must be int or float.")
    return math.pi * r ** 2

