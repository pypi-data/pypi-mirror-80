'''utility generators and functions related to primes'''

from typing import Dict, Generator, List
from valkyrie_util.factors import combine_factorizations


class _smart_sieve:
    '''internal sieve for prime functions

    functions will automatically use the sieve, and it will grow automatically'''

    __sieve: List[bool] = [False, False, True, True]
    __prime_list: List[int] = [2, 3]

    @staticmethod
    def growsieve() -> None:
        '''doubles the size of the sieve'''
        previous_length = len(_smart_sieve.__sieve)
        _smart_sieve.__sieve += [True] * previous_length
        for prime in _smart_sieve.__prime_list:
            if previous_length % prime == 0:
                starting_index = previous_length
            else:
                starting_index = previous_length + prime - (previous_length % prime)
            for multiple in range(starting_index, len(_smart_sieve.__sieve), prime):
                _smart_sieve.__sieve[multiple] = False

    @staticmethod
    def calculate_next_prime() -> None:
        '''finds the next prime after the last prime in prime_list, and adds it to prime_list'''
        possible_prime = _smart_sieve.__prime_list[-1] + 1
        while True:
            if possible_prime >= len(_smart_sieve.__sieve):
                _smart_sieve.growsieve()
            if _smart_sieve.__sieve[possible_prime]:
                _smart_sieve.__prime_list.append(possible_prime)
                for multiple in range(possible_prime * possible_prime, len(_smart_sieve.__sieve), possible_prime):
                    _smart_sieve.__sieve[multiple] = False
                break
            possible_prime += 1

    @staticmethod
    def is_prime(n: int) -> bool:
        '''uses the sieve to check if n is prime'''
        while n > _smart_sieve.__prime_list[-1]:
            _smart_sieve.calculate_next_prime()
        return _smart_sieve.__sieve[n]

    @staticmethod
    def nth_prime(n: int) -> int:
        '''uses the sieve's prime_list to return the nth prime'''
        while n > len(_smart_sieve.__prime_list):
            _smart_sieve.calculate_next_prime()
        return _smart_sieve.__prime_list[n - 1]

    @staticmethod
    def get_current_sieve_size() -> int:
        '''returns the current size of the sieve, useful for optimizations'''
        return len(_smart_sieve.__sieve)


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


def prime_iterator() -> Generator[int, None, None]:
    '''iterates through all primes starting at 2'''
    n = 1
    while True:
        yield _smart_sieve.nth_prime(n)
        n += 1


def is_prime(n: int) -> bool:
    '''checks if n is prime'''
    if n < 2:
        return False
    if n < _smart_sieve.get_current_sieve_size():
        return _smart_sieve.is_prime(n)
    # faster to check divisibility up to the sqrt of n
    sqrt = int(n ** 0.5)
    for prime in prime_iterator():
        if prime > sqrt:
            break
        if n % prime == 0:
            return False
    return True


def nth_prime(n: int) -> int:
    '''returns the nth_prime'''
    if n < 1:
        raise ValueError
    return _smart_sieve.nth_prime(n)


def prime_factorization(n: int) -> Dict[int, int]:
    '''returns the prime factorization of n where the n equals the product of all keys ** value'''
    if n < 1:
        raise ValueError
    elif n == 1:
        return {}
    return _smart_factorization.get_prime_factors(n)
