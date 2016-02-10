from taskin import task
import subprocess


def foo(input):
    return 1


def check(v):
    return v == 1


def bar(input):
    return 'bar'


def baz(input):
    return 'baz'


def finish(input):
    print('done: %s' % input)
    return input


def dig_it(input):
    input, zone = input
    cmd = 'dig +short %s' % zone
    print(cmd)
    ip = subprocess.check_output(cmd, shell=True).strip()
    return (input, ip)


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
