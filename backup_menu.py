import sys
import time
from rich import print as rprint

def quit():
    rprint("The menu will now wait...")
    time.sleep(2)
    sys.exit()

def menu():
    rprint("*****Exiting Main Menu*****")
    time.sleep(1)

choice = input("""
        A: Run script to backup all hosts running configs to backup-directory
        B: Run script to backup "show run", "show version" & "show ip int brief" to date/times stamped folders in archive-directory
        C: Run script to create archive folder in flash on all hosts for saving gold image
        D: Run script to save running configuration as gold image on flash on all hosts in host file
        E: Run script to rollback to gold image on flash on all hosts in host file
        Q: Quit the programme

        Please make a selection from above menu, you will then be prompted to enter your password
""")
if choice == "A" or choice == "a":
    import napback
elif choice == "B" or choice == "b":
    import backup_runverip
elif choice == "C" or choice == "c":
    import napalm_pusharch
elif choice == "D" or choice == "d":
    import savegoldimagetoflash
elif choice == "D" or choice == "d":
    import rollbacktogoldimpage
elif choice == "Q" or choice == "q":
    menu()
else:
    rprint("Error you must enter a valid option from the Menu")

menu