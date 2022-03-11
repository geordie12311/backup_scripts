#Script to used to backup running configs to a backup directory
#backedup files can be used with other scripts to replace running configs using naplam_replace script
import pathlib
import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file

nr = InitNornir(config_file="config.yaml")

user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password

config_dir = "backup-directory"

def backup_configurations(task):
    config_result = task.run(task=napalm_get, getters=["config"])
    startup_config = config_result.result["config"]["running"]
    pathlib.Path(config_dir).mkdir(exist_ok=True)
    task.run(task=write_file, content=startup_config, filename=f"backup-directory/{task.host}.txt")

results = nr.run(task=backup_configurations)
print_result(results)