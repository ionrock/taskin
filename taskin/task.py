import multiprocessing
import multiprocessing.dummy
from multiprocessing import cpu_count


def do_flow(flow, result=None):
    for item in flow:
        result = item(result)
    return result


class BasePool(object):
    def map(self, *args, **kw):
        return self.pool.map(*args, **kw)


class ThreadPool(BasePool):

    def __init__(self, size=20):
        self.size = size
        self.pool = multiprocessing.dummy.Pool(self.size)


class ProcessPool(BasePool):

    def __init__(self, size=None):
        self.size = size or cpu_count()
        self.pool = multiprocessing.Pool(self.size)


class MapTask(object):

    pool_types = [
        'thread', 'process'
    ]

    def __init__(self, args, task, pool=None):
        self.args = args
        self.task = task
        self.pool = pool or ThreadPool()

    def iter_input(self, data):
        for args in self.args:
            if not isinstance(args, (tuple, list)):
                args = [args]
            yield tuple([data] + args)

    def __call__(self, data):
        return self.pool.map(self.task, self.iter_input(data))


class IfTask(object):

    def __init__(self, check, a, b):
        self.check = check
        self.a = a
        self.b = b

    def flow(self, *args, **kw):
        return do_flow(*args, **kw)

    def __call__(self, data):
        if self.check(data):
            return self.flow(self.a, data)
        return self.flow(self.b, data)


class DispatchTask(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher


    def __call__(self, data):
        task = self.dispatcher(data)
        return task(data)
