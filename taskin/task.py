from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count


def do_flow(flow, result=None):
    for item in flow:
        print(item, result)
        result = item(result)
    return result


class PoolAPI(object):
    def map(self, *args, **kw):
        return self.pool.map(*args, **kw)


class ThreadPool(PoolAPI):

    def __init__(self, size=20):
        self.size = size
        self.pool = ThreadPool(self.size)


class ProcessPool(PoolAPI):

    def __init__(self, size=None):
        self.size = size or cpu_count()
        self.pool = ProcessPool(self.size)


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

    def __call__(self, input):
        if check(input):
            return do_flow(self.a, input)
        return do_flow(self.b, input)
