import asyncio
import threading
import time


async def hello(delay):
    # while True:
    count = 0
    while count < 10:
        print("Hello", count)
        count += 1
        await asyncio.sleep(delay)


async def process_work():
    await hello(2)
    print("Done")


def go():
    print("Start go")
    asyncio.run(process_work())
    print("End - process_work")


if __name__ == "__main__":
    print("[+] Start process worker")
    th = threading.Thread(target=go)
    th.start()

    print("[+] Running other tasks below")

    # Other can do work here
    count = 0
    while count < 10:
        print("Main work", count)
        count += 1
        time.sleep(1)

    print("[+] Done main work")
