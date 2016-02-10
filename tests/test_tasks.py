import pytest
from mock import Mock
from taskin import task


def add(x):
    return x + 1


class TestDoFlow(object):

    def test_uses_iterator_with_callables(self):

        def tasks():
            for i in range(3):
                yield add

        assert task.do_flow(tasks(), 1) == 4


class TestPools(object):

    def test_process_pool(object):
        pool = task.ProcessPool(5)

        assert pool.size == 5
        assert hasattr(pool, 'map')
        assert isinstance(pool, task.BasePool)

    def test_thread_pool(object):
        pool = task.ThreadPool(5)

        assert pool.size == 5
        assert hasattr(pool, 'map')
        assert isinstance(pool, task.BasePool)



class TestMapTask(object):

    def setup(self):
        self.args = range(3)
        self.pool = Mock()
        self.task = task.MapTask(add, self.args, self.pool)

    def test_iter_input(self):
        args = list(range(3))
        self.task = task.MapTask(add, args, self.pool)
        iter_input = self.task.iter_input('foo')

        assert list(iter_input) == [
            ('foo', 0),
            ('foo', 1),
            ('foo', 2),
        ]

    def test_iter_input_on_empty_args_iterates_on_input(self):
        self.task = task.MapTask(add, pool=self.pool)
        data = [0, 2, 3]
        assert list(self.task.iter_input(data)) == data

    def test_iter_input_does_not_iterate_on_string(self):
        self.task = task.MapTask(add, pool=self.pool)
        assert list(self.task.iter_input('foo')) == ['foo']

    def test_calls_map_on_pool(self):
        self.task.iter_input = Mock()

        self.task('foo')

        self.pool.map.assert_called_with(add, self.task.iter_input())

    def test_map_task_uses_thread_pool_default(self):
        tsk = task.MapTask(self.args, add)
        assert isinstance(tsk.pool, task.ThreadPool)


class TestIfTask(object):

    def check(self, data):
        return data

    def setup(self):
        self.a, self.b = Mock(), Mock()
        self.task = task.IfTask(self.check, self.a, self.b)
        self.task.flow = Mock()

    def test_true_returns_a(self):
        self.task(True)
        self.task.flow.assert_called_with(self.a, True)

    def test_false_returns_b(self):
        self.task(False)
        self.task.flow.assert_called_with(self.b, False)


class TestDispatchTask(object):

    def setup(self):

        def a(i):
            return 'a'

        def b(i):
            return 'b'

        def c(i):
            return 'c'

        def dispatcher(data):
            tasks = {
                'a': a,
                'b': b,
                'c': c,
            }

            return tasks.get(data)

        self.task = task.DispatchTask(dispatcher)

    def test_dispatch_to_key(self):
        assert self.task('a') == 'a'
        assert self.task('b') == 'b'
        assert self.task('c') == 'c'


    def test_dispatch_fail_to_dispatch(self):
        try:
            self.task('x')
        except:
            assert True
