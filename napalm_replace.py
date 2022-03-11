#Script to use a previously saved configs in backup directory for the hosts to replace running
import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password

def replace_configs(task):
    task.run(task=napalm_configure, filename=f"backup-directory/{task.host}.txt", replace=True)

results = nr.run(task=replace_configs)
print_result(results)
