#!/usr/bin/env python3
'''Function wait_n'''
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int):
    ''' You will spawn wait_random n times with the specified max_delay.
    wait_n should return the list of all the delays'''
    delays = []
    i = 0
    for i in range(n):
        value = await wait_random(max_delay)
        delays.append(value)
    return delays
