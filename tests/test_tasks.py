from mock import Mock
from taskin.task import do_flow
from taskin.task import ProcessPool, cpu_count
from taskin.task import ThreadPool
from taskin.task import BasePool
from taskin.task import MapTask
from taskin.task import IfTask



def add(x):
    return x + 1


class TestDoFlow(object):

    def test_uses_iterator_with_callables(self):

        def tasks():
            for i in range(3):
                yield add

        assert do_flow(tasks(), 1) == 4


class TestPools(object):

    def test_process_pool(object):
        pool = ProcessPool(5)

        assert pool.size == 5
        assert hasattr(pool, 'map')
        assert isinstance(pool, BasePool)

    def test_thread_pool(object):
        pool = ThreadPool(5)

        assert pool.size == 5
        assert hasattr(pool, 'map')
        assert isinstance(pool, BasePool)



class TestMapTask(object):

    def setup(self):
        self.args = range(3)
        self.pool = Mock()
        self.task = MapTask(self.args, add, self.pool)

    def test_iter_input(self):
        iter_input = self.task.iter_input('foo')

        assert list(iter_input) == [
            ('foo', 0),
            ('foo', 1),
            ('foo', 2),
        ]

    def test_calls_map_on_pool(self):
        self.task.iter_input = Mock()

        self.task('foo')

        self.pool.map.assert_called_with(add, self.task.iter_input())

    def test_map_task_uses_thread_pool_default(self):
        task = MapTask(self.args, add)

        assert isinstance(task.pool, ThreadPool)


class TestIfTask(object):

    def check(self, input):
        return input

    def setup(self):
        self.a, self.b = Mock(), Mock()
        self.task = IfTask(self.check, self.a, self.b)
        self.task.flow = Mock()

    def test_true_returns_a(self):
        self.task(True)
        self.task.flow.assert_called_with(self.a, True)

    def test_false_returns_b(self):
        self.task(False)
        self.task.flow.assert_called_with(self.b, False)
