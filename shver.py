from fileinput import filename
from click import command
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result



def show_cpu (task):
    r = task.run(task=netmiko_send_command, command_string="show processes cpu sorted | i CPU", use_textfsm=True)
    task.host["show_cpu"] = r.result
    return r

nr = InitNornir(config_file="config.yaml")
result = nr.run(task=show_cpu)
print_result(result)
