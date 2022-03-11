import os
import pathlib
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.functions import print_result
from datetime import date
#Note importing write_files from nornir utils-plugins-tasks-files
#importing pathlib and date from datetime to date stamp files

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["USERNAME"]
nr.inventory.defaults.password = os.environ["PASSWORD"]
#above section is initialising nornir and using username / password exported in cli
my_list = []
user_input = input("Enter show commands and hit return twice when finished: ")
while user_input:
   my_list.append(user_input)
   user_input = input("Enter show commands and hit return twice when finished: ")
   if user_input == "\n":
       break
#above section is going to ask the user to input a set of commands at the prompt that will
#that will be used later in the script to run against the hosts and output the data to file
def backup_configurations(task):
    for cmd in my_list:
        folder = cmd.replace(" ", "-")
        folder = folder.strip("\n")
        config_dir = "config-archive"
        date_dir = config_dir + "/" + str(date.today())
        command_dir = date_dir + "/" + folder
        pathlib.Path(config_dir).mkdir(exist_ok=True)
        pathlib.Path(date_dir).mkdir(exist_ok=True)
        pathlib.Path(command_dir).mkdir(exist_ok=True)
#above section we are defining directories that will be date stamped and what they will contain
#we are also creating them using pathlib (i.e. if they don't exist the script will create the
# directory structure and each directory will be date stamped 
        r = task.run(task=send_command, command=cmd)
        task.run(
            task=write_file,
            content=r.result, 
            filename=str(command_dir + f"/{task.host}.txt"))
#above function is going to create an task called r which is going to use send_command to send
# the commands in cmds then we run a task to run the write_file command using the output from
# the r.result and write it to a file using the cmd name (example show run) and the host name in
# the backup-archive folders that will be date stamped
results = nr.run(name="Creating Backup Archives", task=backup_configurations)
print_result(results)
#finally we are creating a results object that is going to display a name Creating Backup Archives
#on the screen when the script runs and is going to save the output from the backup_configs task
#it it then going to print the results on the screen

