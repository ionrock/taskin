from taskin import Flow, MapReduceTask


def add(x):
    return x + 1


class TestFlow(object):

    def test_uses_iterator_with_callables(self):

        def tasks():
            for i in range(3):
                yield add

        assert Flow(tasks(), 1)() == 4

    def test_use_single_task(self):
        assert Flow(lambda x: x, 'foo')() == 'foo'


class TestMapReduceFlow(object):

    def test_create_mr(self):

        def find(state):
            for item in state['things']:
                yield {'item': item}

        def func(state):
            state['item'] = state['item'] + 1
            return state

        def reducer(new_state, old_state):
            old_state.update(new_state)
            return old_state

        mrflow = MapReduceTask(
            find, func, reducer
        )

        assert mrflow
