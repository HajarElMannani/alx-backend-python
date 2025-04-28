#!/usr/bin/env python3
'''Function wait_n'''
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random
from typing import List

async def wait_n(n: int, max_delay: int) -> List:
    ''' You will spawn wait_random n times with the specified max_delay.
    wait_n should return the list of all the delays'''
    delays = []
    i = 0
    tasks = []
    for i in range(n):
        tasks.append(wait_random(max_delay))

    for task in asyncio.as_completed(tasks):
        delayed = await task
        delays.append(delayed)
    return delays
