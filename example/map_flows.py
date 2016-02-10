from taskin import task


def get_servers(data):
    return [
        'foo.example.com',
        'bar.example.com',
    ]


def create_something(data):
    servers, name = data
    for server in servers:
        print('Creating: https://%s/%s' % (server, name))


def main():
    flow = [
        get_servers,
        task.MapTask(create_something, args=xrange(10))
    ]
    task.do_flow(flow)


if __name__ == '__main__':
    main()
