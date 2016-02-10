from taskin import task
import subprocess


def foo(data):
    return 1


def check(v):
    return v == 1


def bar(data):
    return 'bar'


def baz(data):
    return 'baz'


def finish(data):
    for i in data:
        print('%s, %s' % i)
    print('Done!')

    return data


def dig_it(data):
    data, zone = data
    cmd = 'dig +short %s' % zone
    print('running: %s' % cmd.strip())

    ip = subprocess.check_output(cmd.split()).strip()
    return (data, ip)


myflow = [
    foo,
    task.IfTask(check, [bar], [baz]),
    task.MapTask([
        'ionrock.org',
        'google.com',
        'rackspace.com',
    ], dig_it),
    finish,
]


def main():
    print(task.do_flow(myflow))


if __name__ == '__main__':

    main()
