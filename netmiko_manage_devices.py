from copy import deepcopy

import yaml
from netmiko import ConnectHandler


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


def netmiko_connect(host, commands):
    hostname = list(host)[0]
    host = host.get(hostname)
    net_connect = ConnectHandler(**host)
    for comm in commands:
        print('{0} {1} : command - {2} {0}'.format('=' * 20, hostname, comm))
        output = net_connect.send_command(comm)
        print(output)
    net_connect.disconnect()


def main():
    commands = [
        'sh clock',
        'sh ip int br',
        'sh run | e !'
    ]

    for host in parse_inventory_file():
        netmiko_connect(host, commands)


if __name__ == "__main__":
    main()
