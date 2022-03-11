import yaml
from pprint import pprint

target_dict = { 'get_facts': { 'fqdn': 'R1.gh-lab.com',
                 'hostname': 'R1',
                 'interface_list': [ 'GigabitEthernet0/0',
                                     'GigabitEthernet0/1',
                                     'GigabitEthernet0/2',
                                     'GigabitEthernet0/3',
                                     'Loopback0'],
                 'model': 'IOSv',
                 'os_version': 'IOSv Software (VIOS-ADVENTERPRISEK9-M), '
                               'Version 15.7(3)M3, RELEASE SOFTWARE (fc2)',
                 'serial_number': '9X0MYJHM9SOTZ6WJXVFCU',
                 'uptime': 20280,
                 'vendor': 'Cisco'}}

filename = "validate_R1.yaml"
with open(filename, "w") as f:
    output = yaml.dump(target_dict, f, default_flow_style=False)