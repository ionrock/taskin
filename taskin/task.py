import abc


def do_flow(flow, result=None):
    for item in flow:
        print(item, result)
        result = item(result)
    return result


class MapTask(object):

    def __init__(self, args, task):
        self.args = args
        self.task = task
        self.pool = Pool(cpu_count())

    def iter_input(self, input):
        for args in self.args:
            if not isinstance(args, (tuple, list)):
                args = [args]
            yield tuple([input] + args)


    def __call__(self, input):
        return self.pool.map(self.task, self.iter_input(input))


class IfTask(object):

    def __init__(self, check, a, b):
        self.check = check
        self.a = a
        self.b = b

    def __call__(self, input):
        if check(input):
            return do_flow(self.a, input)
        return do_flow(self.b, input)
