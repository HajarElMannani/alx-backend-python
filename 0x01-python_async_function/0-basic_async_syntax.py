#!/usr/bin/env python3
'''Funcion wait_random'''
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    '''Coroutine that waits for a random delay between 0 and
    max_delay (included and float value)
    seconds and eventually returns it'''
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
