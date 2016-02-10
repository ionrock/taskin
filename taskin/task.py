import multiprocessing
import multiprocessing.dummy
from multiprocessing import cpu_count


def do_flow(flow, result=None):
    if callable(flow):
        return flow(result)

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

    def __init__(self, task, args=None, pool=None):
        self.args = args
        self.task = task
        self.pool = pool or ThreadPool()

    def iter_input(self, data):
        if self.args:
            for args in self.args:
                if not isinstance(args, (tuple, list)):
                    args = [args]
                yield tuple([data] + args)

        elif not isinstance(data, basestring):
            for item in data:
                yield item
        else:
            yield data

    def __call__(self, data):
        return self.pool.map(self.task, self.iter_input(data))


class IfTask(object):

    def __init__(self, check, a, else_case=None):
        self.check = check
        self.a = a
        self.b = else_case

    def flow(self, *args, **kw):
        return do_flow(*args, **kw)

    def __call__(self, data):
        if self.check(data):
            return self.flow(self.a, data)
        else:
            if self.b:
                return self.flow(self.b, data)
            else:
                return data


class DispatchTask(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher


    def __call__(self, data):
        task = self.dispatcher(data)
        return task(data)
