#!/usr/bin/env python3
'''Function task_wait_n'''
import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    ''' The code is nearly identical to wait_n except
    task_wait_random is being called'''
    delays = []
    i = 0
    tasks = []
    for i in range(n):
        tasks.append(task_wait_random(max_delay))
    for task in asyncio.as_completed(tasks):
        delayed = await task
        delays.append(delayed)
    return delays
