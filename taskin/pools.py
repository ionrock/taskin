import time
import multiprocessing

from concurrent import futures


class BasePool(object):
    def map(self, f, iterator):
        return self.executor.map(f, iterator)


class ProcessPool(BasePool):
    def __init__(self, size=None):
        self.size = size or multiprocessing.cpu_count()
        self.executor = futures.ProcessPoolExecutor(size)


class ThreadPool(BasePool):
    def __init__(self, size=None):
        self.size = size or 20
        self.executor = futures.ThreadPoolExecutor(self.size)
