'''formulas for fast calculations'''


def range_sum_int(start: int, end: int, divisor: int = 1) -> int:
    '''returns the sum of all integers in the range [start, end] that are divisible by the divisor'''
    calc_start = (min(start, end) + divisor - 1) // divisor
    calc_end = max(start, end) // divisor
    return ((calc_start + calc_end) * (calc_end - calc_start + 1) // 2) * divisor


def sum_of_squares(n: int) -> int:
    '''returns the sum of squares for the numbers 1 to n'''
    if n < 0:
        raise ValueError
    return n * (n + 1) * (2 * n + 1) // 6
