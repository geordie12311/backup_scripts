#script is going to use replace vrf function
#in napalm_task script and use naplam_configure
import getpass
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure
from napalm_task import replace_vrf

nr = InitNornir(config_file="config.yaml")

password = getpass.getpass()
nr.inventory.defaults.password = password
def replace_feature(task):

    config = replace_vrf(task)
    task.run(task=napalm_configure, configuration=config, replace=True)


result = nr.run(task=replace_feature)
print_result(result)