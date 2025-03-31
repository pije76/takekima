# import numpy as np
# from pylfsr import LFSR
from functools import reduce
from collections import deque
import itertools
import ast

# seed = ""
taps = ()

def lfsr(seed, taps, loop):
    # print("seed", seed)

    # for j in range(0, loop):
    sr, xor = seed, 0
    # if sr == 1:
    # while 1:
    # while True:
    i = 0
    while i <= loop:
        for t in taps:
            xor += int(sr[t-1])
        if xor%2 == 0.0: # get the remainder after the integer division. The % is called the modulo operator.
            xor = 0
            # print("xor", xor)
        else:
            xor = 1
            # print("xor", xor)
        length = len(sr)
        # print("length", length)
        sr, xor = str(xor) + sr[:-1], 0 # get everything except the last index (slicing)
        # print("sr", i+1, sr)
        # print("out", i+1, out)
        # print("xor", i+1, sr[:1])
        print(i+1, " | ", sr, " | ", sr[length-1])
        i += 1
        # length = len(sr)
        # print(length)
        # if sr == seed:
        #     break
        # print("Iteration", j+1, "of the seed is:\t", sr)

seed = input("Enter any seed (eg: 0110 or 01101):\t ")
taps = ast.literal_eval(input('Initialize taps, separate by comma (eg: 1,4 or 1,3,4): '))
loop = int(input("How many iterations of the lfsr: "))
print("seed", seed)
print(type(seed))
# emptytaps = taps
print("taps", taps)
print(type(taps))

# print(lfsr('0110', (1,4)))
print(lfsr(seed, taps, loop))
# input()
