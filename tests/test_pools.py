from taskin import ProcessPool, ThreadPool, BasePool


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
