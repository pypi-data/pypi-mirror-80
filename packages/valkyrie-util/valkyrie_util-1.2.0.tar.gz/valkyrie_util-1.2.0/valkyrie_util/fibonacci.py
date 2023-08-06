'''utility generators and functions related to the fibonacci sequence'''

from typing import Generator


def fibonacci_iterator(a: int = 1, b: int = 1) -> Generator[int, None, None]:
    '''iterates through the fibonaccie sequence using starting values'''
    while True:
        yield a
        a, b = b, a + b
