import multiprocessing
import multiprocessing.dummy
from multiprocessing import cpu_count

from pprint import pformat


class Flowable(object):

    def flow(self, flow, state=None):
        flow = Flow(flow, state)
        return flow()


class Flow(object):

    def __init__(self, flow, state=None):
        self.flow = flow
        self.state = state or {}

    def __call__(self, state=None):
        state = state or self.state
        if callable(self.flow):
            return self.flow(state)
        else:
            for task in self.flow:
                state = task(state)
            return state


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


class MapTask(Flowable):

    def __init__(self, task, args_iterator, pool=None):
        self.args = args_iterator
        self.task = task
        self.pool = pool or ThreadPool()

    def iter_input(self, data):
        for item in self.args(data):
            yield item

    def __call__(self, data):
        return self.pool.map(
            self.task, self.iter_input(data)
        )


class IfTask(Flowable):

    def __init__(self, check, a, else_case=None):
        self.check = check
        self.a = a
        self.b = else_case

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
        if not task:
            return data
        return task(data)


class ReduceTask(Flowable):

    def __init__(self, reducer, flow_or_task):
        self.reducer = reducer
        self.flow_or_task = flow_or_task

    def __call__(self, data):
        new_state = self.flow(self.flow_or_task, data)
        return self.reducer(new_state, data)
