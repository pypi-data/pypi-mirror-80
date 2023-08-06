'''utility functions for operations related to factors/divisors'''

from functools import reduce
from typing import Callable, Dict, List


def combine_factorizations(facts: List[Dict[int, int]]) -> Dict[int, int]:
    '''combines all factorizations into one, equivalent to multiplying all products of each factorization'''
    new_factorization = {}
    for fact in facts:
        for base, exponent in fact.items():
            if base in new_factorization:
                new_factorization[base] += exponent
                if new_factorization[base] == 0:
                    del new_factorization[base]
            else:
                new_factorization[base] = exponent
    return new_factorization


def factorization_product(fact: Dict[int, int]) -> int:
    '''returns the product which yields the input factorization'''
    power: Callable[[int, int], int] = lambda b, e: b ** e
    product: Callable[[int, int], int] = lambda x, y: x * y
    return reduce(product, [power(b, e) for b, e in fact.items()], 1)


def lcm_factorization(facts: List[Dict[int, int]]) -> Dict[int, int]:
    '''returns the least common multiple of all factorizations input'''
    new_factorization = {}
    for fact in facts:
        for base, exponent in fact.items():
            if base in new_factorization:
                new_factorization[base] = max(new_factorization[base], exponent)
                if new_factorization[base] == 0:
                    del new_factorization[base]
            else:
                new_factorization[base] = exponent
    return new_factorization
