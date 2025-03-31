from functools import reduce
from collections import deque
import itertools
import ast

taps = ()

def lfsr(seed, taps, loop):

    sr, xor = seed, 0

    i = 0
    while i <= loop:
        for t in taps:
            xor += int(sr[t-1])
        if xor%2 == 0.0: # get the remainder after the integer division. The % is called the modulo operator.
            xor = 0
        else:
            xor = 1
        length = len(sr)
        sr, xor = str(xor) + sr[:-1], 0 # get everything except the last index (slicing)
        print(i+1, " | ", sr, " | ", sr[length-1])
        i += 1

seed = input("Enter any seed (eg: 0110 or 01101):\t ")
taps = ast.literal_eval(input('Initialize taps, separate by comma (eg: 1,4 or 1,3,4): '))
loop = int(input("How many iterations of the lfsr: "))

print(lfsr(seed, taps, loop))
