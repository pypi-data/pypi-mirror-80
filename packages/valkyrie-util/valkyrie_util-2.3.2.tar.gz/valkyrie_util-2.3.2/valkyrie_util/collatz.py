'''utility functions related to the collatz sequence'''

from typing import Dict, Generator


def next_collatz(n: int) -> int:
    '''returns the next number in the collatz sequence'''
    if n < 1:
        raise ValueError
    return n // 2 if n % 2 == 0 else n * 3 + 1


def collatz_iterator(n: int) -> Generator[int, None, None]:
    '''iterates through the collatz sequence from n to 1'''
    if n < 1:
        raise ValueError
    while True:
        yield n
        if n == 1:
            break
        n = next_collatz(n)


class _collatz:
    '''internal memory for finding collatz length'''
    __known_lengths: Dict[int, int] = {1: 1}

    @staticmethod
    def get_length(n: int) -> int:
        '''returns the length of collatz sequence of n'''
        if n in _collatz.__known_lengths:
            return _collatz.__known_lengths[n]
        length = 1 + _collatz.get_length(next_collatz(n))
        _collatz.__known_lengths[n] = length
        return length


def collatz_length(n: int) -> int:
    '''returns the length of collatz sequence starting at 1'''
    if n < 1:
        raise ValueError
    return _collatz.get_length(n)
