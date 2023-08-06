'''utility generators and functions related to triangle numbers'''

from typing import Generator


def triangle_num_iterator(n: int = 1) -> Generator[int, None, None]:
    '''iterates through the triangle numbers, starting at the nth one'''
    if n < 0:
        raise ValueError
    triangle_number = nth_triangle_number(n)
    while True:
        yield triangle_number
        n += 1
        triangle_number += n


def nth_triangle_number(n: int) -> int:
    '''returns the nth triangle number'''
    if n < 0:
        raise ValueError
    return n * (n + 1) // 2
