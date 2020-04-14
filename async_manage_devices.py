from copy import deepcopy
import asyncio

import yaml
import netdev


def parse_inventory_file(yaml_file = 'devices/devices.yml', inventory = 'all'):
    with open(yaml_file) as f:
        raw = yaml.load(f, Loader=yaml.FullLoader)
    raw = deepcopy(raw[inventory])
    for device in raw['devices']:
        host = {}
        hostname = device.pop('hostname')
        host[hostname] = deepcopy(raw['vars'])
        host[hostname].update(device)
        yield host


async def async_connect(host, commands):
    hostname, host_connection_params = host.popitem()

    output = '\n{0} Start config device "{1}" {0}\n'.format('=' * 20, hostname)
    async with netdev.create(**host_connection_params) as ios:
        for comm in commands:
            output += '\n{0} Run command "{1}" {0}\n'.format('=' * 20, comm)
            output += await ios.send_command(comm)
    output += '\n{0} End config device "{1}" {0}\n'.format('=' * 20, hostname)

    print(output)


async def main():
    commands = [
        'sh clock',
        'sh ip int br',
        'sh run | e !'
    ]

    tasks = [asyncrm_connect(host, commands) for host in parse_inventory_file()]
    await asyncio.wait(tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
