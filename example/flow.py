import subprocess

from pprint import pprint

from taskin import IfTask, MapTask, do_flow


def foo(data):
    return 1


def check(v):
    return v == 1


def bar(data):
    return 'bar'


def baz(data):
    return 'baz'


def finish(data):
    result = {}

    for i in data:
        zone, ips = i
        result[zone] = ips

    return result


def dig_it(zone):
    cmd = 'dig +short %s' % zone
    print('running: %s' % cmd.strip())

    ips = subprocess.check_output(cmd.split()).strip().split('\n')
    return (zone, ips)


myflow = [
    foo,
    IfTask(check, [bar], [baz]),
    MapTask(dig_it, [
        'ionrock.org',
        'google.com',
        'rackspace.com',
    ]),
    finish,
]


def main():
    results = do_flow(myflow, {})
    pprint(results)
    print('Done')

if __name__ == '__main__':
    main()
