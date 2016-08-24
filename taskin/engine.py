class Flowable(object):

    def flow(self, flow, state=None):
        return do_flow(flow, state)


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


def do_flow(flow, state):
    f = Flow(flow)
    return f(state)
