#Script to backup both running and startup configs 
#and can be used to restore from saved configs for other scripts
import getpass
import pathlib
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.functions import print_result
#importing getpass to prompt for password
#nornir and nornir naplam plugin
#pathlib to create directory

nr = InitNornir(config_file="config.yaml")

user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password

config_dir = "running_configs-directory"
startup_dir = "startup_configs-directory"

def backup_configs(task):
    config_result = task.run(task=napalm_get, getters=["config"])
    running_config = config_result.result["config"]["running"]
    pathlib.Path(config_dir).mkdir(exist_ok=True)
#using pathlib to create the backup-directory, 
#if the directory doesn't exist it will create it
    task.run(task=write_file, content=running_config, filename=f"running_configs-directory/{task.host}.txt")
#writing the running configuration from each host into host specific files in the backup directory

def startup_configs(task):
    config_result = task.run(task=napalm_get, getters=["config"])
    startup_config = config_result.result["config"]["startup"]
    pathlib.Path(startup_dir).mkdir(exist_ok=True)
#using pathlib to create the backup-directory, 
#if the directory doesn't exist it will create it
    task.run(task=write_file, content=startup_config, filename=f"startup_configs-directory/{task.host}.txt")

results_running = nr.run(task=backup_configs)
results_startup = nr.run(task=startup_configs)
print_result(results_running)
print_result(results_startup)