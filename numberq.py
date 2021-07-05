#!/usr/bin/env python3
# Demo of producer-consumer model using the thread-safe queue

import threading
import queue
from threading import Thread
from queue import Queue
from time import sleep, time

q = Queue(maxsize=10)

def thread_print(*args):
    print(f'{threading.current_thread().name}: ', end='')
    print(*args)

def consumer(q, delay=0.1, timeout=2):
    while True:
        try:
            num = q.get(timeout=timeout)
            thread_print(f'{num} consumed')
            sleep(delay)
        except queue.Empty:
            thread_print(f'{num} exiting')
            return

def producer(q, delay=0.1, total=100):
    for x in range(total):
        thread_print(f'{x} produced')
        q.put(x)
        sleep(delay)

if __name__ == '__main__':
    nproducer = 2
    nconsumer = 5
    producers = [Thread(target=producer, args=(q,), name=f'prod_{i}') for i in range(nproducer)]
    consumers = [Thread(target=consumer, args=(q,), name=f'cons_{i}') for i in range(nconsumer)]
    for p in producers:
        p.start()
    for c in consumers:
        c.start()
    for p in producers:
        p.join()
    for c in consumers:
        c.join()
    