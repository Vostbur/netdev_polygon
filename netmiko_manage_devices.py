from copy import deepcopy

import yaml
from netmiko import ConnectHandler


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


def netmiko_connect(host, commands):
    net_connect = ConnectHandler(**host)

    output = ''
    for comm in commands:
        output += '\n{0} Run command "{1}" {0}\n'.format('=' * 20, comm)
        output += net_connect.send_command(comm)
    
    net_connect.disconnect()
    return output


def main():
    commands = [
        'sh clock',
        'sh ip int br',
        'sh run | e !'
    ]

    for host in parse_inventory_file():
        hostname, host_connection_data = host.popitem()
        result = '\n{0} Start config device "{1}" {0}\n'.format('=' * 20, hostname)
        result += netmiko_connect(host_connection_data, commands)
        result += '\n{0} End config device "{1}" {0}\n'.format('=' * 20, hostname)
        print(result)


if __name__ == "__main__":
    main()
