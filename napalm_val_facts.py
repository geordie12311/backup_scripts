#Script to used to create archive area on hosts for napalm
import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password

def get_test(task):
    task.run(task=napalm_get, getters=["get_facts"])

results = nr.run(get_test)
print_result(results)

