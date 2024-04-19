from calendar import c
from distutils.command.config import config
from unittest import result
from click import command
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command,netmiko_send_config
from nornir_utils.plugins.functions import print_result, print_title
from nornir.core.filter import F

nr = InitNornir(config_file = "config.yml")

def config(push):
    push.run(task = netmiko_send_config, config_file = "push.txt")
    push.run(task = netmiko_send_command, command_string = "sh run")
    push.run(task = netmiko_send_command, command_string = "wr")

devices = nr.filter(F(groups__any=["CORESW1, ACCESSSW1", "access_switch"]))

results = devices.run(task = config)

print_title("Deploying config")
print_result(results)