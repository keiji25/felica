import socket
import time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import asyncio

if __name__ == '__main__':
    elapsed_times = 0
    for _ in range(10):
        selector = DefaultSelector()
        stopped = False
        paths_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}
        start = time.time()
        for path in paths_todo:
            crawler = Crawler(path)
            crawler.fetch()
        loop()
        elapsed_time = time.time() - start
        elapsed_times += elapsed_time
        print(f"elapsed_time: {(elapsed_time):.2f}[sec]")
    print(f"mean_elapsed_time: {(elapsed_times/10):.2f}[sec]")