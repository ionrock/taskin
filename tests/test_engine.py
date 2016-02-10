from taskin import Flow


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
