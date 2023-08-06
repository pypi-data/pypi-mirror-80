'''utility generators and functions related to primes'''

from typing import Generator, List


class _smart_sieve:
    '''internal sieve for prime functions

    functions will automatically use the sieve, and it will grow automatically'''

    __sieve: List[bool] = [False, False, True, True]
    __prime_list: List[int] = [2, 3]

    @staticmethod
    def __grow_sieve() -> None:
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
    def __calculate_next_prime() -> None:
        '''finds the next prime after the last prime in prime_list, and adds it to prime_list'''
        possible_prime = _smart_sieve.__prime_list[-1] + 1
        while True:
            if possible_prime >= len(_smart_sieve.__sieve):
                _smart_sieve.__grow_sieve()
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
            _smart_sieve.__calculate_next_prime()
        return _smart_sieve.__sieve[n]

    @staticmethod
    def nth_prime(n: int) -> int:
        '''uses the sieve's prime_list to return the nth prime'''
        while n > len(_smart_sieve.__prime_list):
            _smart_sieve.__calculate_next_prime()
        return _smart_sieve.__prime_list[n - 1]

    @staticmethod
    def get_current_sieve_size() -> int:
        '''returns the current size of the sieve, useful for optimizations'''
        return len(_smart_sieve.__sieve)


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
