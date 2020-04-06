from copy import deepcopy
import asyncio

import yaml
import netdev


def parse_inventory_file(yaml_file = 'devices/devices.yml', inventory = 'all'):
    with open(yaml_file) as f:
        raw = yaml.load(f.read(), Loader=yaml.BaseLoader)
    raw = deepcopy(raw[inventory])
    for device in raw['devices']:
        host = {}
        hostname = device.pop('hostname')
        host[hostname] = deepcopy(raw['vars'])
        host[hostname].update(device)
        yield host


async def netmiko_connect(host, commands):
    hostname = list(host)[0]
    host = host.get(hostname)

    async with netdev.create(**host) as ios:
        for comm in commands:
            print('{0} {1} : command - {2} {0}'.format('=' * 20, hostname, comm))
            output = await ios.send_command(comm)
            print(output)


async def main():
    commands = [
        'sh clock',
        'sh ip int br',
        'sh run | e !'
    ]

    tasks = [netmiko_connect(host, commands) for host in parse_inventory_file()]
    await asyncio.wait(tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
