#Script to used to create archive area on hosts for napalm
import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_validate
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password

def validate_test(task):
    task.run(task=napalm_validate, src=f"validate_{task.host}.yaml")
results = nr.run(task=validate_test)
print_result(results)