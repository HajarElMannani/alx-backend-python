#!/usr/bin/env python3
'''Function to_kv'''
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    '''Function that returns a tuple of string k, and the square
    of the int/float v.'''
    return (k, v**2)
