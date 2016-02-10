from taskin.task import do_flow


def add(x):
    return x + 1


class TestDoFlow(object):

    def test_uses_iterator_with_callables(self):

        def tasks():
            for i in range(3):
                yield add

        assert do_flow(tasks(), 1) == 4
