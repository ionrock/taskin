import multiprocessing
import multiprocessing.dummy
from multiprocessing import cpu_count


def do_flow(flow, result=None):
    for item in flow:
        print(item, result)
        result = item(result)
    return result


class BasePool(object):
    def map(self, *args, **kw):
        return self.pool.map(*args, **kw)


class ThreadPool(BasePool):

    def __init__(self, size=20):
        self.size = size
        self.pool = multiprocessing.dummy.Pool(self.size)


Pool = ThreadPool


class ProcessPool(BasePool):

    def __init__(self, size=None):
        self.size = size or cpu_count()
        self.pool = multiprocessing.Pool(self.size)


class MapTask(object):

    pool_types = [
        'thread', 'process'
    ]

    def __init__(self, args, task, pool):
        self.args = args
        self.task = task
        self.pool = pool

    def iter_input(self, input):
        for args in self.args:
            if not isinstance(args, (tuple, list)):
                args = [args]
            yield tuple([input] + args)

    def __call__(self, input):
        return self.pool.map(self.task, self.iter_input(input))


class IfTask(object):

    def __init__(self, check, a, b):
        self.check = check
        self.a = a
        self.b = b

    def flow(self, *args, **kw):
        return do_flow(*args, **kw)

    def __call__(self, input):
        if self.check(input):
            return self.flow(self.a, input)
        return self.flow(self.b, input)