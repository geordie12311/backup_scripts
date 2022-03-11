#Script to used to create archive area on hosts for napalm
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password

def arch(task):
    task.run(task=send_configs_from_file, file="napalm-archive.txt")

results = nr.run(task=arch)
print_result(results)