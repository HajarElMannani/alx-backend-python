#!/usr/bin/env python3
'''Function sum_list'''
from typing import List


def sum_list(input_list: List[float]) -> float:
    '''Function that takes a list input_list of floats as argument
    and returns their sum as a float'''
    summ = 0.0
    for number in input_list:
        summ = summ + number
    return summ
