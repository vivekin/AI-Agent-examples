import time

def task(name):
    print(f"{name} started")
    time.sleep(3)
    print(f"{name} completed")

start = time.time()

task("Task 1")
task("Task 2")

print("Total:", time.time() - start)

# Task 1 started
# Task 1 completed
# Task 2 started
# Task 2 completed
# Total: 6.005136728286743

# =======================================================

import asyncio
import time

async def task(name):
    print(f"{name} started")
    await asyncio.sleep(3)
    print(f"{name} completed")


async def main():
    start = time.time()

    await asyncio.gather(
        task("Task 1"),
        task("Task 2")
    )

    print("Total:", time.time() - start)


asyncio.run(main())

# Task 1 started
# Task 2 started
# Task 1 completed
# Task 2 completed
# Total: 3.015333652496338

# =======================================================
