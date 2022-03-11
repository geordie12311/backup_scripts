import logging
import re
import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir(config_file="config.yaml")

etx = chr(3)

#replace_ospf fucntion is going to find the ospf information in config and replace it with
#new config held in a jinja.2 template
def replace_ospf(task):
    data = task.run(
        task=load_yaml,
        file=f"./host_vars/{task.host}.yaml",
        severity_level=logging.DEBUG,
    )
    task.host["facts"] = data.result
#creating facts object to capture output of data result
    config = task.run(task=napalm_get, getters=["config"], severity_level=logging.DEBUG)
#using napalm getters to get the running config
    showrun = config.result["config"]["running"]
    pattern = re.compile("^router ospf([^!]+)", flags=re.I | re.M)
#using regular expression to pattern match the ! mark after router ospf. the I flag = case sensitive
#the M flag = multiplines
    routing_template = task.run(
        task=template_file,
        name="Buildling Routing Configuration",
        template="ospfreplace.j2",
        path="./templates",
        severity_level=logging.DEBUG,
    )
#Above create task to run jinja template file called opsfreplace.j2 and data contained in it
#will be used to build the new configuration
    template_to_load = routing_template.result
    newconfig = re.sub(pattern, template_to_load, showrun)
#newconfig object is going to substitute the ospf section captured from the running config
#with the new data held in the jinja.2 template
    final_config = newconfig.replace("^C", etx)
#this is going to use chr(3) which is associated to etx object to replace any ^C 
#which denotes end of text character normally used in Banners
    return final_config

#replace_vrf function is going to replace the vrf information in config with the new config
#saved in the jinja2 template
def replace_vrf(task):
    data = task.run(
        task=load_yaml,
        file=f"./host_vars/{task.host}.yaml",
        severity_level=logging.DEBUG,
    )
    task.host["facts"] = data.result
    config = task.run(task=napalm_get, getters=["config"], severity_level=logging.DEBUG)
    showrun = config.result["config"]["running"]
    pattern = re.compile("!\n!", flags=re.I | re.M)
    newchar = "`"
    newconfig = re.sub(pattern, newchar, showrun)
    vrfpattern = re.compile("vrf definition[^`]+", flags=re.I | re.M)
    load_template = task.run(
        task=template_file,
        name="Buildling Routing Configuration",
        template="vrf.j2",
        path="./templates",
        severity_level=logging.DEBUG

    )
    vrf_template = load_template.result
    vrf_config = re.sub(vrfpattern, vrf_template, newconfig)
    configuration = vrf_config.replace("`", "!")
    final_config = configuration.replace("^C", etx)

    return final_config