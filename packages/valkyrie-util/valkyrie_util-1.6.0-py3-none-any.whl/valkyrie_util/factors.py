'''utility functions for operations related to factors/divisors'''

from functools import reduce
from typing import Callable, Dict, List
from valkyrie_util.primes import nth_prime


class _smart_factorization:
    '''internal memory of factorizations,

    ensures no recalculations of factorizations'''

    known_factorizations: Dict[int, Dict[int, int]] = {1: {}}

    @staticmethod
    def get_prime_factors(n: int, last_prime_tested: int = 1) -> Dict[int, int]:
        '''recursively calculates factorizations'''
        if n in _smart_factorization.known_factorizations:
            return _smart_factorization.known_factorizations[n].copy()

        current_divisor = nth_prime(last_prime_tested)

        # add the prime to factorization if not already in
        if current_divisor not in _smart_factorization.known_factorizations:
            _smart_factorization.known_factorizations[current_divisor] = {current_divisor: 1}

        # can stop and conclude that n is prime if current_divisor ** 2 > n
        if current_divisor * current_divisor > n:
            _smart_factorization.known_factorizations[n] = {n: 1}
            return {n: 1}

        if n % current_divisor == 0:
            quotient = n // current_divisor
            quotient_fact = _smart_factorization.get_prime_factors(quotient, last_prime_tested)
            fact = combine_factorizations([{current_divisor: 1}, quotient_fact])
            _smart_factorization.known_factorizations[n] = fact
            return fact
        else:
            return _smart_factorization.get_prime_factors(n, last_prime_tested + 1)


def prime_factorization(n: int) -> Dict[int, int]:
    '''returns the prime factorization of n where the n equals the product of all keys ** value'''
    if n < 1:
        raise ValueError
    elif n == 1:
        return {}
    return _smart_factorization.get_prime_factors(n)


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


def divisor_count_factorization(fact: Dict[int, int]) -> int:
    '''returns the amount of divisors from a factorization'''
    product: Callable[[int, int], int] = lambda x, y: x * y
    return reduce(product, [e + 1 for b, e in fact.items()], 1)


def divisor_count(n: int) -> int:
    '''returns the amount of divisors for n'''
    return divisor_count_factorization(prime_factorization(n))


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
