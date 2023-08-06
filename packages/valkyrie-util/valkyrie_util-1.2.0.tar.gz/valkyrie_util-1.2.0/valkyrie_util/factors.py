'''utility functions for operations related to factors/divisors'''

from typing import Dict, List


def combine_factorizations(factorizations: List[Dict[int, int]]) -> Dict[int, int]:
    '''combines all factorizations into one, equivalent to multiplying all products of each factorization'''
    new_factorization = {}
    for fact in factorizations:
        for base, exponent in fact.items():
            if base in new_factorization:
                new_factorization[base] += exponent
                if new_factorization[base] == 0:
                    del new_factorization[base]
            else:
                new_factorization[base] = exponent
    return new_factorization
