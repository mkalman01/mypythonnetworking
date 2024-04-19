from fileinput import filename
from click import command
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import csv


def show_interface_status(task):
    r = task.run(task=netmiko_send_command, command_string="show interface status", use_textfsm=True, template_path="/home/testubuntu/Documents/switchingautomation/templates/show_interface_status.textfsm")
    task.host["interface_status"] = r.result
    return r

nr = InitNornir(config_file="config.yaml")
result = nr.run(task=show_interface_status)
print_result(result)

# # Write the result to a CSV file
# for host, host_data in result.items():
#     with open(f"{host}_interface_status.csv", "w", newline="") as f:
#         writer = csv.DictWriter(f, fieldnames=["host","interface", "status", "vlan"])
#         writer.writeheader()
#         for interface in host_data.result.result:
#         # for interface in host_data.result:
#             writer.writerow({
#                 "host": host,
#                 "interface": interface["port"],
#                 "interface": interface["name"],
#                 "status": interface["status"],
#                 "vlan": interface["vlan"],
#             })
