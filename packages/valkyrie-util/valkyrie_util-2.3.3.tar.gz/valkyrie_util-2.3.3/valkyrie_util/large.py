'''operations for integers larger than typical data sizes'''

from typing import List


def __normalize(large_num: List[int]) -> List[int]:
    '''normalizes the large number by making empty lists [0] and removing leading zeros'''
    if large_num == []:
        return [0]
    normalized_num = large_num.copy()
    while len(normalized_num) > 1 and normalized_num[-1] == 0:
        normalized_num.pop()
    return normalized_num


def string_to_large_number(digit_string: str) -> List[int]:
    '''converts the string of digits to a large number format'''
    return __normalize([int(c) for c in digit_string[::-1]])


def large_number_to_string(large_num: List[int]) -> str:
    '''converts the large number to a string'''
    return str().join(str(n) for n in __normalize(large_num)[::-1])


def __carry_values(large_num: List[int], base: int = 10) -> List[int]:
    '''ensures that all values in the large number are less than the base by carrying the remainder to next value'''
    result, magnitude, remainder = [], 0, 0
    while remainder > 0 or magnitude < len(large_num):
        if magnitude < len(large_num):
            remainder += large_num[magnitude]
        result.append(remainder % base)
        remainder = remainder // base
        magnitude += 1
    return result


def large_number_sum(*large_nums: List[int]) -> List[int]:
    '''sums all large numbers in the input'''
    large_sum: List[int] = []
    for addend in large_nums:
        for magnitude in range(min(len(large_sum), len(addend))):
            large_sum[magnitude] += addend[magnitude]
        if len(addend) > len(large_sum):
            large_sum += addend[len(large_sum):]
    return __normalize(__carry_values(large_sum))


def large_number_multiply(large_num: List[int], multiplier: int) -> List[int]:
    '''returns large_num * multiplier in large number format'''
    if multiplier < 0:
        raise ValueError
    large_product = [n * multiplier for n in large_num]
    return __normalize(__carry_values(large_product))
