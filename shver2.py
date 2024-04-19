from fileinput import filename
from click import command
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

def show_log (task):
    r = task.run(task=netmiko_send_command, command_string="sh run | i logging host", use_textfsm=True)
    task.host["show_log"] = r.result
    return r

nr = InitNornir(config_file="config.yaml")
result = nr.run(task=show_log)
print_result(result)