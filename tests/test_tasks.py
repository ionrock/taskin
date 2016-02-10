from mock import Mock
from taskin import task


def add(x):
    return x + 1


class TestFlow(object):

    def test_uses_iterator_with_callables(self):

        def tasks():
            for i in range(3):
                yield add

        assert task.Flow(tasks(), 1)() == 4

    def test_use_single_task(self):
        assert task.Flow(lambda x: x, 'foo')() == 'foo'


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
        def args(data):
            for i in range(3):
                yield (data, i)

        self.task = task.MapTask(add, args, self.pool)
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

    def test_no_else(self):
        mytask = task.IfTask(self.check, lambda x: 'a')
        assert mytask(True) == 'a'


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
