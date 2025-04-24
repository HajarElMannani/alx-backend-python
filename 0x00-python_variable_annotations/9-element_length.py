#!/usr/bin/env python3
'''Function element_length'''
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''Annotate this function'''
    return [(i, len(i)) for i in lst]
