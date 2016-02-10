import multiprocessing
import multiprocessing.dummy


class BasePool(object):
    def map(self, *args, **kw):
        return self.pool.map(*args, **kw)


class ThreadPool(BasePool):

    def __init__(self, size=20):
        self.size = size
        self.pool = multiprocessing.dummy.Pool(self.size)


class ProcessPool(BasePool):

    def __init__(self, size=None):
        self.size = size or multiprocessing.cpu_count()
        self.pool = multiprocessing.Pool(self.size)
