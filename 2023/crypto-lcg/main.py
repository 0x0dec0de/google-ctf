from functools import reduce
from math import gcd
from data import dump


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0] * multiplier) % modulus
    return increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return multiplier


def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2 * t0 - t1 * t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return modulus


class LCG:
    # Xn = (a*Xn-1 + c) % n
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed


known_elements = dump
modulus = crack_unknown_modulus(known_elements)
multiplier = crack_unknown_multiplier(known_elements, modulus)
increment = crack_unknown_increment(known_elements, modulus, multiplier)

print('''Modulus: {}
Multiplier: {}
Increment: {}'''.format(modulus, multiplier, increment))

# if args.next is not None:
#     print('\nCalculating next values:')
#     lcg = LCG(known_elements[-1], multiplier, increment, modulus)
#     for _ in range(args.next):
#         print(lcg.next())