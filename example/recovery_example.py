from taskin import MapReduceTask, Flow
from pprint import pprint
import random


def reducer(new, old):
    return {'new': new, 'old': old}


def find_targets_and_nameservers(state):
    state['targets'] = [
        'ns1.foo.com',
        'ns2.foo.com',
    ]

    state['nameservers'] = [
        'ns1.bar.com',
        'ns2.bar.com',
        'ns3.bar.com',
        'ns4.bar.com',
    ]

    return state


def find_errored_zones(state):
    state['zones'] = [
        'poo.com.',
        'pee.net.',
        'poop.digital.',
    ]
    return state


def find_targets(state):
    for target in state['targets']:
        yield {'zone': state['zone'], 'target': target}


def create_zone_on_target(state):
    print('created %s on: %s' % (state['zone'], state['target']))
    return {
        'zone': state['zone'],
        'created': random.choice([True, False]),
        'target': state['target']
    }


def create_reducer(new, state):
    state['creates'] = new
    return state


def verification_reducer(new, state):
    state['verification'] = new
    return state


def find_ns(state):
    for nameserver in state['nameservers']:
        yield {'zone': state['zone'], 'ns': nameserver}


def verify_zone_on_ns(state):
    print('%s found on %s' % (state['zone'], state['ns']))
    return {
        'zone': state['zone'],
        'verified': random.choice([True, False]),
        'nameserver': state['ns']
    }


def find_create_errors(state):
    for zone in state['zones']:
        state['zone'] = zone
        yield state


def create_status_reducer(new, state):
    for i, item in enumerate(new):
        state['create_status_%s' % i] = item
    return state


create_flow = Flow([
    find_targets_and_nameservers,
    MapReduceTask(find_targets, create_zone_on_target, create_reducer),
    MapReduceTask(find_ns, verify_zone_on_ns, verification_reducer)
])

recovery_flow = Flow([
    find_errored_zones,
    MapReduceTask(
        find_create_errors,
        create_flow,
        create_status_reducer
    )
])

pprint(recovery_flow({'zone': 'example.net.'}))
