# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 11:00:00 2023

@author: jhutchison

"""

# %% Packages
""" Third party and local imports """

import itertools
import math
import pathlib

from fractions import Fraction
from functools import reduce
from operator import mul  # or mul=lambda x,y: x*y


# %% Functions
""" Define functions """


def nCr(n, r):
    f = math.factorial
    return f(n) // f(r) // f(n - r)


def nCk(n, k):
    return int(reduce(mul, (Fraction(n - i, i + 1) for i in range(k)), 1))


# %% Variables
""" Set script (global) variables """

path_data = pathlib.Path("data/")


# %% Main
""" Display task data """

if __name__ == "__main__":
    print(list(itertools.combinations("abcd", 2)))
    print(["".join(x) for x in itertools.combinations("abcd", 2)])

    # Custom Function
    print(nCr(7, 5))

    print(math.comb(7, 5))

    for n in range(17):
        print(" ".join("%5d" % nCk(n, k) for k in range(n + 1)).center(100))


# %%
