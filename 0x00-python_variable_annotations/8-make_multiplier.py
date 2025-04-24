#!/usr/bin/env python3
'''Function make_multiplier'''
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''returns a function that multiplies a float by multiplier'''
    def multiply(x: float) -> float:
        if callable(multiply):
            return x * multiplier
    return multiply
