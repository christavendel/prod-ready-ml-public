import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/sleep/{seconds}")
def sleep_for(seconds: int):
    time.sleep(seconds)
    return "Awake!"


import asyncio


@app.get("/sleepio/{seconds}")
async def sleep_for(seconds: int):
    print("Going to bed")
    for s in range(seconds + 1):
        await asyncio.sleep(1)
        print(f"zz {s}")
    return "Awake!"
